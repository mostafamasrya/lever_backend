from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.settings import api_settings
import math
## you can override page_size, max_page_size from url query params \
## to make it more dynamic
class CustomPagination(PageNumberPagination):
    page_size = api_settings.PAGE_SIZE # default page size
    # max_page_size = 1000 # default max page size
    page_size_query_param = 'page_size' # if you want to dynamic items per page from request you must have to add it 
      
    def get_paginated_response(self, data):
        self.validate_page_size()
                    
        # you can count total page from request by total and page_size
        total_page = math.ceil(self.page.paginator.count / self.page_size)
        
        # here is your response
        return Response({
            'count': self.page.paginator.count,
            'total': total_page,
            'page_size': self.page_size,
            'current': self.page.number,
            'previous': self.get_previous_link(),
            'next': self.get_next_link(),
            'results': data
        })

    def validate_page_size(self):
        page_size = self.request.query_params.get(self.page_size_query_param)
        if page_size and isinstance(page_size, int) and page_size > 0:
            self.page_size = int(page_size)