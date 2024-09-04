"""
API Custom Response Classes
"""

from rest_framework.response import Response

def ApiResponse(Response):
    """
    Define a standard response object across the project
    """
    def __init__(
            self,
            status=None,
            data=None,
            template_name=None,
            headers=None, 
            exception=False, 
            content_type=None
    ):
        
        response = {
            "metadata": {
                "datafiles": [],
                "pagination": {
                    "current_page": 0,
                    "pageSize": 1000,
                    "totalCount": 10,
                    "totalPages": 1
                },
                "status": [
                    {
                        "message": "Request accepted, response successful",
                        "messageType": "INFO"
                    }
                ],
            },            
            "result": {
                "data": data
            }
        }
    
        super().__init__(response, status=status, template_name=template_name, headers=headers, exception=exception, content_type=content_type)