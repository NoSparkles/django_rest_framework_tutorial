#from django.http import JsonResponse
import json
from products.models import Product
from products.serializers import ProductSerializer
from django.forms.models import model_to_dict

from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def api_home(request):
    data = {}
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.data
    return Response(data)
