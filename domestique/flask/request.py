import logging

from flask import request

from ..logging import get_calling_method_text

logger = logging.getLogger(__name__)


def _handle_bad_request_json(request, caller, e=None):

    logger.error(f"Expecting JSON passed to '{caller}' but got invalid request.data:\n{request.data}")
    if e:
        logger.exception(f"Got {type(e)} attempting to access request JSON: {e}", exc_info=False)
    raise ValueError(f"Invalid request - no valid JSON passed")


def get_reqjson(request):

    try:
    
        if not request:
            raise ValueError(f"Missing required request from '{get_calling_method_text()}'!")

        content_type = request.content_type

        if content_type != "application/json":
            # Warn about content_type explicitly, to be helpful to the developer :)
            raise TypeError(f"Invalid request Content-Type: '{content_type}' - required: 'application/json'")

        if not request.is_json:
            _handle_bad_request_json(request, get_calling_method_text(), None)

        try:
            reqjson = request.json
        except Exception as e:
            _handle_bad_request_json(request, get_calling_method_text(), e)

        logger.debug(f"Type (reqjson): {type(reqjson)}")
        logger.debug(f"Request JSON: {reqjson}")

        return reqjson

    except (TypeError, ValueError) as e:

        raise e

    except Exception as e:

        message = f"An error occurred processing request from {get_calling_method_text()}: {e}"
        logger.exception(message, exc_info=True)
        raise e


def get_arg(request, name, default_val=None):

    if not request or not name:
        raise ValueError(f"Missing required request/arg name from '{get_calling_method_text()}'!")

    val = request.args.get(name, default_val)
    logger.debug(f"Value for request argument '{name}': {val}")
    return val


def get_required_arg(request, name):

    val = get_arg(request, name, None)
    if not val:
        message = f"Missing '{name}' parameter"
        logger.error(f"{message}:\n{request}")
        raise ValueError(message)
    return val


def get_reqjson_val(reqjson, name, default_val=None):

    if not reqjson or not name:
        raise ValueError(f"Missing required reqjson/name from '{get_calling_method_text()}'!")

    val = reqjson.get(name, None)
    logger.debug(f"Value for reqjson prop '{name}': {val}")
    return val


def get_required_reqjson_val(reqjson, name):

    val = get_reqjson_val(reqjson, name, None)
    if not val:
        message = f"Missing '{name}' value in reqjson"
        logger.error(f"{message}:\n{reqjson}")
        raise ValueError(message)
    return val

