"""
API Custom Response Classes
"""
from django.utils.deprecation import MiddlewareMixin
from rest_framework.response import Response

class StandardizedResponse(MiddlewareMixin):
    """
    Standardized API response format for the DRF API
    Imported as a middleware mixin for DRF 
    in settings.py 
    MIDDLEWARE = {
        ...
        'api.responses.StandardizedResponse',
        ...
    }

    Pulls in the response and reformats it, saying if there are any errors
    or any other message that needs to be returned.
    """
    def process_template_response(self, request, response):
        """
        Defines a standardized template for API responses

        """
        # Check if the response is an HTTPResponse object
        if isinstance(response, Response):
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                # Do not modify the response for browsable API requests
                return response


            # Grab response and request information
            status_code = response.status_code
            method = request.method
            endpoint = request.path
            query_params = request.GET

            # Set up base response template
            standardized_data = {
                "method": method,
                "call": endpoint,
                "query_parameters": query_params if method == "GET" else None,
                "status": status_code,
                "message": "Success" if status_code < 400 else "Error",

            }

            # Formate the data and error keys if errors
            if status_code >= 400: # Format for errors
                standardized_data['data'] = None
                standardized_data['errors'] = response.data

            # Else reformat paginated results
            elif response.data is not None and 'results' in response.data:
                standardized_data['pagination'] = {
                    f"{k}": f"{v}" for k, v in response.data.items() if k != 'results'
                }
                standardized_data['pagination']['page_size'] = str(len(response.data['results']))
                standardized_data['data'] = response.data['results']
                standardized_data['errors'] = None
            
            # Else return null data and errors for no-response calls
            else:
                standardized_data['data'] = None
                standardized_data['errors'] = None
            
            # Overwrite the response data
            response.data = standardized_data
            response.content_type = "application/json"

        return response
