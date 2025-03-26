from django.http import JsonResponse
from rest_framework.decorators import api_view

@api_view(['GET']) # Defines the HTTP methods that the view will accept, GET in this case
def demo_get_request(request): # The view function that will be called, must always have a request parameter
    return JsonResponse({'message': 'GET method is working!'}) # Returns a JSON response with a message
