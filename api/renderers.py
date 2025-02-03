from rest_framework.renderers import JSONRenderer

class StandardizedJSONRenderer(JSONRenderer):
    """
    A custom JSON renderer that standardizes API responses.
    """

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Subclass of the JSONRenderer for a standardized format
        Returns the reformated response and context
        """
        # Access the response and request from the renderer context
        response = renderer_context.get('response', None)
        request = renderer_context.get('request', None)

        # Initialize base standardized response structure
        standardized_response = {
            "method": request.method if request else None,
            "call": request.path if request else None,
            "query_parameters": request.GET if request and request.method == "GET" else None,
            "status": response.status_code if response else None,
            "message": "Success" if response and response.status_code < 400 else "Error",
        }

        # Format the data and errors based on the status code
        if response and response.status_code >= 400:  # Error case
            standardized_response["data"] = None
            standardized_response["errors"] = data
        elif response and "results" in data:  # Paginated results
            standardized_response["pagination"] = {
                k: v for k, v in data.items() if k != "results"
            }
            standardized_response["pagination"]["page_size"] = len(data["results"])
            standardized_response["data"] = data["results"]
            standardized_response["errors"] = None
        else:  # General success case
            standardized_response["data"] = data
            standardized_response["errors"] = None

        # Render the standardized response
        return super().render(standardized_response, accepted_media_type, renderer_context)