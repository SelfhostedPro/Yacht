from flask import make_response, jsonify
import werkzeug.exceptions

# def register_json_errors(app_blueprint)
def register_errorhandlers(blueprint):
    # create helper function

    # werkzeug.exceptions.BadRequest
    @blueprint.errorhandler(400)
    def bad_request(error):
        return make_response(jsonify({
            'error': {
                'code': 400,
                'message': error.description or 'Bad Request'
            }
        }), 400)

    # werkzeug.exceptions.Unauthorized
    @blueprint.errorhandler(401)
    def unauthorized(error):
        return make_response(jsonify({
            'error': {
                'code': 401,
                'message': error.description or 'Unauthorized'
            }
        }), 401)

    # 402, Payment Required

    # werkzeug.exceptions.Forbidden
    @blueprint.errorhandler(403)
    def forbidden(error):
        return make_response(jsonify({
            'error': {
                'code': 403,
                'message': error.description or 'Forbidden'
            }
        }), 403)

    # werkzeug.exceptions.NotFound
    @blueprint.errorhandler(404)
    def not_found(error):
        return make_response(jsonify({
            'error': {
                'code': 404,
                'message': error.description or 'Not Found'
            }
        }), 404)

    # Error used by Webargs.
    # werkzeug.exceptions.MethodNotAllowed
    @blueprint.errorhandler(405)
    def method_not_allowed(error):
        return make_response(jsonify({
            'error': {
                'code': 405,
                'message': error.description or 'Method Not Allowed'
            }
        }), 405)

    # werkzeug.exceptions.NotAcceptable  406

    # 407, Proxy Authentication Required

    # werkzeug.exceptions.RequestTimeout 408
    # werkzeug.exceptions.Conflict       409
    @blueprint.errorhandler(409)
    def gone(error):
        return make_response(jsonify({
            'error': {
                'code': 409,
                'message': error.description or 'Conflict'
            }
        }), 409)

    # werkzeug.exceptions.Gone
    @blueprint.errorhandler(410)
    def gone(error):
        return make_response(jsonify({
            'error': {
                'code': 410,
                'message': error.description or 'Gone'
            }
        }), 410)

    # werkzeug.exceptions.LengthRequired        411
    # werkzeug.exceptions.PreconditionFailed    412
    # werkzeug.exceptions.RequestEntityTooLarge 413
    # werkzeug.exceptions.RequestURITooLarge    414

    # werkzeug.exceptions.UnsupportedMediaType
    @blueprint.errorhandler(415)
    def unsupported_media_type(error):
        return make_response(jsonify({
            'error': {
                'code': 415,
                'message': error.description or 'Unsupported Media Type'
            }
        }), 415)

    # werkzeug.exceptions.RequestedRangeNotSatisfiable  416
    # werkzeug.exceptions.ExpectationFailed             417
    # werkzeug.exceptions.ImATeapot                     418

    # 419, Unknown Status
    # 420, Policy Not Fulfilled
    # 421, Misdirected Request

    # Error used by Webargs.
    @blueprint.errorhandler(422)
    def unprocessable_entity(error):
        return make_response(jsonify({
            'error': {
                'code': 422,
                'message': error.description or 'Unprocessable Entity'
            }
        }), 422)

    # 423, Locked
    # 424, Failed Dependency
    # 425, Unordered Collection/Too Early
    # 426, Upgrade Required

    # werkzeug.exceptions.PreconditionRequired          428

    # werkzeug.exceptions.TooManyRequests
    @blueprint.errorhandler(429)
    def too_many_requests(error):
        return make_response(jsonify({
            'error': {
                'code': 429,
                'message': error.description or 'Too Many Requests'
            }
        }), 429)

    # 430, Would Block

    # werkzeug.exceptions.RequestHeaderFieldsTooLarge   431

    # 444, No Response
    # 449, The request should be retried after doing the appropriate action
    # 451, Unavailable For Legal Reasons

    # werkzeug.exceptions.InternalServerError
    @blueprint.errorhandler(werkzeug.exceptions.InternalServerError)
    def internal_server_error(error):
        return make_response(jsonify({
            'error': {
                'code': 500,
                'message': error.description or 'Internal Server Error'
            }
        }), 500)


    # werkzeug.exceptions.NotImplemented
    @blueprint.errorhandler(werkzeug.exceptions.NotImplemented)
    def internal_server_error(error):
        return make_response(jsonify({
            'error': {
                'code': 501,
                'message': error.description or 'Not Implemented'
            }
        }), 501)

    # werkzeug.exceptions.BadGateway            502
    # werkzeug.exceptions.ServiceUnavailable    503

    # 504, Gateway Timeout
    # 505, HTTP Version not supported
    # 506, Variant Also Negioates
    # 507, Insufficient Storage
    # 508, Loop Detected
    # 509, Bandwidth Limit Exceeded
    # 510, Not Extended
    # 511, Authentication Reuired

    @blueprint.errorhandler(Exception)
    def uncaught_server_error(error):
        return make_response(jsonify({
            'error': {
                'code': 500,
                'message': 'Internal Server Error'
            }
        }), 500)