from rest_framework.views import exception_handler

#exc => Exception that was raised
#context => contains informaton about the request an response
#responses => default response returned by django when an exception occurs 
def custom_exception_handler(exc, context):

    handlers = {
        "ValidationError":_handle_generic_error,
        "PermissionDenied": _handle_generic_error,
        "Http404": _handle_generic_error,
        "NotAuthenticated": _handle_authentication_error
    }

    response = exception_handler(exc, context)
    if response is not None:
        response.data['status_code'] = response.status_code

    #get the exception class name
    exception_class = exc.__class__.__name__
    #check if the exception class is in our dictionary of handlers
    if exception_class in handlers:
        return handlers[exception_class](exc, context, response)
        
    return response

def _handle_authentication_error(exc, context, response):
    
    response.data ={
        "error":"please login to proceed", 
        "status_code": response.status_code
    }
    return response

def _handle_generic_error(exc, context, response):
    return response