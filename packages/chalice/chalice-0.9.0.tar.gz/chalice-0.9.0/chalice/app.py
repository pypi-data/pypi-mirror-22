"""Chalice app and routing code."""
import re
import sys
import logging
import json
import traceback
import decimal
import warnings
import base64
from collections import Mapping

# Implementation note:  This file is intended to be a standalone file
# that gets copied into the lambda deployment package.  It has no dependencies
# on other parts of chalice so it can stay small and lightweight, with minimal
# startup overhead.


_PARAMS = re.compile(r'{\w+}')


def handle_decimals(obj):
    # Lambda will automatically serialize decimals so we need
    # to support that as well.
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    return obj


def error_response(message, error_code, http_status_code):
    body = {'Code': error_code, 'Message': message}
    response = Response(body=body, status_code=http_status_code)
    return response.to_dict()


def _matches_content_type(content_type, valid_content_types):
    if ';' in content_type:
        content_type = content_type.split(';', 1)[0].strip()
    return content_type in valid_content_types


class ChaliceError(Exception):
    pass


class ChaliceViewError(ChaliceError):
    STATUS_CODE = 500

    def __init__(self, msg=''):
        super(ChaliceViewError, self).__init__(
            self.__class__.__name__ + ': %s' % msg)


class BadRequestError(ChaliceViewError):
    STATUS_CODE = 400


class UnauthorizedError(ChaliceViewError):
    STATUS_CODE = 401


class ForbiddenError(ChaliceViewError):
    STATUS_CODE = 403


class NotFoundError(ChaliceViewError):
    STATUS_CODE = 404


class MethodNotAllowedError(ChaliceViewError):
    STATUS_CODE = 405


class ConflictError(ChaliceViewError):
    STATUS_CODE = 409


class TooManyRequestsError(ChaliceViewError):
    STATUS_CODE = 429


ALL_ERRORS = [
    ChaliceViewError,
    BadRequestError,
    NotFoundError,
    UnauthorizedError,
    ForbiddenError,
    ConflictError,
    TooManyRequestsError]


class CaseInsensitiveMapping(Mapping):
    """Case insensitive and read-only mapping."""

    def __init__(self, mapping):
        mapping = mapping or {}
        self._dict = {k.lower(): v for k, v in mapping.items()}

    def __getitem__(self, key):
        return self._dict[key.lower()]

    def __iter__(self):
        return iter(self._dict)

    def __len__(self):
        return len(self._dict)

    def __repr__(self):
        return 'CaseInsensitiveMapping(%s)' % repr(self._dict)


class Authorizer(object):
    name = ''

    def to_swagger(self):
        raise NotImplementedError("to_swagger")


class IAMAuthorizer(Authorizer):

    _AUTH_TYPE = 'aws_iam'

    def __init__(self):
        self.name = 'sigv4'

    def to_swagger(self):
        return {
            'in': 'header',
            'type': 'apiKey',
            'name': 'Authorization',
            'x-amazon-apigateway-authtype': 'awsSigv4',
        }


class CognitoUserPoolAuthorizer(Authorizer):

    _AUTH_TYPE = 'cognito_user_pools'

    def __init__(self, name, provider_arns, header='Authorization'):
        self.name = name
        self._header = header
        if not isinstance(provider_arns, list):
            # This class is used directly by users so we're
            # adding some validation to help them troubleshoot
            # potential issues.
            raise TypeError(
                "provider_arns should be a list of ARNs, received: %s"
                % provider_arns)
        self._provider_arns = provider_arns

    def to_swagger(self):
        return {
            'in': 'header',
            'type': 'apiKey',
            'name': self._header,
            'x-amazon-apigateway-authtype': self._AUTH_TYPE,
            'x-amazon-apigateway-authorizer': {
                'type': self._AUTH_TYPE,
                'providerARNs': self._provider_arns,
            }
        }


class CustomAuthorizer(Authorizer):

    _AUTH_TYPE = 'custom'

    def __init__(self, name, authorizer_uri, ttl_seconds=300,
                 header='Authorization'):
        self.name = name
        self._header = header
        self._authorizer_uri = authorizer_uri
        self._ttl_seconds = ttl_seconds

    def to_swagger(self):
        return {
            'in': 'header',
            'type': 'apiKey',
            'name': self._header,
            'x-amazon-apigateway-authtype': self._AUTH_TYPE,
            'x-amazon-apigateway-authorizer': {
                'type': 'token',
                'authorizerUri': self._authorizer_uri,
                'authorizerResultTtlInSeconds': self._ttl_seconds,
            }
        }


class CORSConfig(object):
    """A cors configuration to attach to a route."""

    _REQUIRED_HEADERS = ['Content-Type', 'X-Amz-Date', 'Authorization',
                         'X-Api-Key', 'X-Amz-Security-Token']

    def __init__(self, allow_origin='*', allow_headers=None,
                 expose_headers=None, max_age=None, allow_credentials=None):
        self.allow_origin = allow_origin

        if allow_headers is None:
            allow_headers = set(self._REQUIRED_HEADERS)
        else:
            allow_headers = set(allow_headers + self._REQUIRED_HEADERS)
        self._allow_headers = allow_headers

        if expose_headers is None:
            expose_headers = []
        self._expose_headers = expose_headers

        self._max_age = max_age
        self._allow_credentials = allow_credentials

    @property
    def allow_headers(self):
        return ','.join(sorted(self._allow_headers))

    def get_access_control_headers(self):
        headers = {
            'Access-Control-Allow-Origin': self.allow_origin,
            'Access-Control-Allow-Headers': self.allow_headers
        }
        if self._expose_headers:
            headers.update({
                'Access-Control-Expose-Headers': ','.join(self._expose_headers)
            })
        if self._max_age is not None:
            headers.update({
                'Access-Control-Max-Age': str(self._max_age)
            })
        if self._allow_credentials is True:
            headers.update({
                'Access-Control-Allow-Credentials': 'true'
            })

        return headers


class Request(object):
    """The current request from API gateway."""

    def __init__(self, query_params, headers, uri_params, method, body,
                 context, stage_vars, is_base64_encoded):
        self.query_params = query_params
        self.headers = CaseInsensitiveMapping(headers)
        self.uri_params = uri_params
        self.method = method
        self._is_base64_encoded = is_base64_encoded
        self._body = body
        #: The parsed JSON from the body.  This value should
        #: only be set if the Content-Type header is application/json,
        #: which is the default content type value in chalice.
        self._json_body = None
        self._raw_body = None
        self.context = context
        self.stage_vars = stage_vars

    def _base64decode(self, encoded):
        if not isinstance(encoded, bytes):
            encoded = encoded.encode('ascii')
        output = base64.b64decode(encoded)
        return output

    @property
    def raw_body(self):
        if self._raw_body is None:
            if self._is_base64_encoded:
                self._raw_body = self._base64decode(self._body)
            elif not isinstance(self._body, bytes):
                self._raw_body = self._body.encode('utf-8')
            else:
                self._raw_body = self._body
        return self._raw_body

    @property
    def json_body(self):
        if self.headers.get('content-type', '').startswith('application/json'):
            if self._json_body is None:
                self._json_body = json.loads(self.raw_body)
            return self._json_body

    def to_dict(self):
        copied = self.__dict__.copy()
        # We want the output of `to_dict()` to be
        # JSON serializable, so we need to remove the CaseInsensitive dict.
        copied['headers'] = dict(copied['headers'])
        return copied


class Response(object):
    def __init__(self, body, headers=None, status_code=200):
        self.body = body
        if headers is None:
            headers = {}
        self.headers = headers
        self.status_code = status_code

    def to_dict(self, binary_types=None):
        body = self.body
        if not isinstance(body, (str, bytes)):
            body = json.dumps(body, default=handle_decimals)
        response = {
            'headers': self.headers,
            'statusCode': self.status_code,
            'body': body
        }
        if binary_types is not None:
            self._b64encode_body_if_needed(response, binary_types)
        return response

    def _b64encode_body_if_needed(self, response_dict, binary_types):
        response_headers = CaseInsensitiveMapping(response_dict['headers'])
        content_type = response_headers.get('content-type', '')
        body = response_dict['body']

        if _matches_content_type(content_type, binary_types):
            if _matches_content_type(content_type, ['application/json']):
                # There's a special case when a user configures
                # ``application/json`` as a binary type.  The default
                # json serialization results in a string type, but for binary
                # content types we need a type bytes().  So we need to special
                # case this scenario and encode the JSON body to bytes().
                body = body.encode('utf-8')
            body = self._base64encode(body)
            response_dict['isBase64Encoded'] = True
        response_dict['body'] = body

    def _base64encode(self, data):
        if not isinstance(data, bytes):
            raise ValueError('Expected bytes type for body with binary '
                             'Content-Type. Got %s type body instead.'
                             % type(data))
        data = base64.b64encode(data)
        return data.decode('ascii')


class RouteEntry(object):

    def __init__(self, view_function, view_name, path, methods,
                 authorizer_name=None,
                 api_key_required=None, content_types=None,
                 cors=False, authorizer=None):
        self.view_function = view_function
        self.view_name = view_name
        self.uri_pattern = path
        self.methods = methods
        self.authorizer_name = authorizer_name
        self.api_key_required = api_key_required
        #: A list of names to extract from path:
        #: e.g, '/foo/{bar}/{baz}/qux -> ['bar', 'baz']
        self.view_args = self._parse_view_args()
        self.content_types = content_types
        # cors is passed as either a boolean or a CORSConfig object. If it is a
        # boolean it needs to be replaced with a real CORSConfig object to
        # pass the typechecker. None in this context will not inject any cors
        # headers, otherwise the CORSConfig object will determine which
        # headers are injected.
        if cors is True:
            cors = CORSConfig()
        elif cors is False:
            cors = None
        self.cors = cors
        self.authorizer = authorizer

    def _parse_view_args(self):
        if '{' not in self.uri_pattern:
            return []
        # The [1:-1] slice is to remove the braces
        # e.g {foobar} -> foobar
        results = [r[1:-1] for r in _PARAMS.findall(self.uri_pattern)]
        return results

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class APIGateway(object):

    _DEFAULT_BINARY_TYPES = [
        'application/octet-stream',
        'application/x-tar',
        'application/zip',
        'audio/basic',
        'audio/ogg',
        'audio/mp4',
        'audio/mpeg',
        'audio/wav',
        'audio/webm',
        'image/png',
        'image/jpg',
        'image/gif',
        'video/ogg',
        'video/mpeg',
        'video/webm',
    ]

    def __init__(self):
        self.binary_types = self.default_binary_types

    @property
    def default_binary_types(self):
        return list(self._DEFAULT_BINARY_TYPES)


class Chalice(object):

    FORMAT_STRING = '%(name)s - %(levelname)s - %(message)s'

    def __init__(self, app_name, configure_logs=True):
        self.app_name = app_name
        self.api = APIGateway()
        self.routes = {}
        self.current_request = None
        self.debug = False
        self.configure_logs = configure_logs
        self.log = logging.getLogger(self.app_name)
        self._authorizers = {}
        if self.configure_logs:
            self._configure_logging()

    def _configure_logging(self):
        log = logging.getLogger(self.app_name)
        if self._already_configured(log):
            return
        handler = logging.StreamHandler(sys.stdout)
        # Timestamp is handled by lambda itself so the
        # default FORMAT_STRING doesn't need to include it.
        formatter = logging.Formatter(self.FORMAT_STRING)
        handler.setFormatter(formatter)
        log.propagate = False
        if self.debug:
            level = logging.DEBUG
        else:
            level = logging.ERROR
        log.setLevel(level)
        log.addHandler(handler)

    def _already_configured(self, log):
        if not log.handlers:
            return False
        for handler in log.handlers:
            if isinstance(handler, logging.StreamHandler):
                if handler.stream == sys.stdout:
                    return True
        return False

    @property
    def authorizers(self):
        return self._authorizers.copy()

    def define_authorizer(self, name, header, auth_type, provider_arns=None):
        warnings.warn(
            "define_authorizer() is deprecated and will be removed in future "
            "versions of chalice.  Please use CognitoUserPoolAuthorizer(...) "
            "instead", DeprecationWarning)
        self._authorizers[name] = {
            'header': header,
            'auth_type': auth_type,
            'provider_arns': provider_arns,
        }

    def route(self, path, **kwargs):
        def _register_view(view_func):
            self._add_route(path, view_func, **kwargs)
            return view_func
        return _register_view

    def _add_route(self, path, view_func, **kwargs):
        name = kwargs.pop('name', view_func.__name__)
        methods = kwargs.pop('methods', ['GET'])
        authorizer_name = kwargs.pop('authorizer_name', None)
        authorizer = kwargs.pop('authorizer', None)
        api_key_required = kwargs.pop('api_key_required', None)
        content_types = kwargs.pop('content_types', ['application/json'])
        cors = kwargs.pop('cors', False)
        if not isinstance(content_types, list):
            raise ValueError('In view function "%s", the content_types '
                             'value must be a list, not %s: %s'
                             % (name, type(content_types), content_types))
        if kwargs:
            raise TypeError('TypeError: route() got unexpected keyword '
                            'arguments: %s' % ', '.join(list(kwargs)))
        if path in self.routes:
            raise ValueError(
                "Duplicate route detected: '%s'\n"
                "URL paths must be unique." % path)
        entry = RouteEntry(view_func, name, path, methods,
                           authorizer_name, api_key_required,
                           content_types, cors, authorizer)
        self.routes[path] = entry

    def __call__(self, event, context):
        # This is what's invoked via lambda.
        # Sometimes the event can be something that's not
        # what we specified in our request_template mapping.
        # When that happens, we want to give a better error message here.
        resource_path = event.get('requestContext', {}).get('resourcePath')
        if resource_path is None:
            return error_response(error_code='InternalServerError',
                                  message='Unknown request.',
                                  http_status_code=500)
        http_method = event['requestContext']['httpMethod']
        if resource_path not in self.routes:
            raise ChaliceError("No view function for: %s" % resource_path)
        route_entry = self.routes[resource_path]
        if http_method not in route_entry.methods:
            return error_response(
                error_code='MethodNotAllowedError',
                message='Unsupported method: %s' % http_method,
                http_status_code=405)
        view_function = route_entry.view_function
        function_args = [event['pathParameters'][name]
                         for name in route_entry.view_args]
        self.current_request = Request(event['queryStringParameters'],
                                       event['headers'],
                                       event['pathParameters'],
                                       event['requestContext']['httpMethod'],
                                       event['body'],
                                       event['requestContext'],
                                       event['stageVariables'],
                                       event.get('isBase64Encoded', False))
        # We're doing the header validation after creating the request
        # so can leverage the case insensitive dict that the Request class
        # uses for headers.
        if route_entry.content_types:
            content_type = self.current_request.headers.get(
                'content-type', 'application/json')
            if not _matches_content_type(content_type,
                                         route_entry.content_types):
                return error_response(
                    error_code='UnsupportedMediaType',
                    message='Unsupported media type: %s' % content_type,
                    http_status_code=415,
                )
        response = self._get_view_function_response(view_function,
                                                    function_args)
        if self._cors_enabled_for_route(route_entry):
            self._add_cors_headers(response, route_entry.cors)

        response_headers = CaseInsensitiveMapping(response.headers)
        if not self._validate_binary_response(
                self.current_request.headers, response_headers):
            content_type = response_headers.get('content-type', '')
            return error_response(
                error_code='BadRequest',
                message=('Request did not specify an Accept header with %s, '
                         'The response has a Content-Type of %s. If a '
                         'response has a binary Content-Type then the request '
                         'must specify an Accept header that matches.'
                         % (content_type, content_type)),
                http_status_code=400
            )
        response = response.to_dict(self.api.binary_types)
        return response

    def _validate_binary_response(self, request_headers, response_headers):
        # Validates that a response is valid given the request. If the response
        # content-type specifies a binary type, there must be an accept header
        # that is a binary type as well.
        request_accept_header = request_headers.get('accept')
        response_content_type = response_headers.get(
            'content-type', 'application/json')
        response_is_binary = _matches_content_type(response_content_type,
                                                   self.api.binary_types)
        expects_binary_response = False
        if request_accept_header is not None:
            expects_binary_response = _matches_content_type(
                request_accept_header, self.api.binary_types)
        if response_is_binary and not expects_binary_response:
            return False
        return True

    def _get_view_function_response(self, view_function, function_args):
        try:
            response = self._invoke_view_function(view_function, function_args)
        except ChaliceViewError as e:
            # Any chalice view error should propagate.  These
            # get mapped to various HTTP status codes in API Gateway.
            response = Response(body={'Code': e.__class__.__name__,
                                      'Message': str(e)},
                                status_code=e.STATUS_CODE)
        except Exception as e:
            headers = {}
            if self.debug:
                # If the user has turned on debug mode,
                # we'll let the original exception propogate so
                # they get more information about what went wrong.
                self.log.debug("Caught exception for %s", view_function,
                               exc_info=True)
                stack_trace = ''.join(traceback.format_exc())
                body = stack_trace
                headers['Content-Type'] = 'text/plain'
            else:
                body = {'Code': 'InternalServerError',
                        'Message': 'An internal server error occurred.'}
            response = Response(body=body, headers=headers, status_code=500)
        if not isinstance(response, Response):
            response = Response(body=response)
        self._validate_response(response)
        return response

    def _invoke_view_function(self, view_function, function_args):
        response = view_function(*function_args)
        self._validate_response(response)
        return response

    def _validate_response(self, response):
        if isinstance(response, Response):
            for header, value in response.headers.items():
                if '\n' in value:
                    raise ChaliceError("Bad value for header '%s': %r" %
                                       (header, value))

    def _cors_enabled_for_route(self, route_entry):
        return route_entry.cors is not None

    def _add_cors_headers(self, response, cors):
        for name, value in cors.get_access_control_headers().items():
            if name not in response.headers:
                response.headers[name] = value
