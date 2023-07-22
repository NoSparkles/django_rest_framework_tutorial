from rest_framework import generics, mixins, authentication
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from api.authentication import TokenAuthentication
from api.mixins import StaffEditorPermissionMixin, UserQuerySetMixin
from .models import Product
from .serializers import ProductSerializer



class ProductListCreateAPIView(UserQuerySetMixin, StaffEditorPermissionMixin, generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [authentication.SessionAuthentication, TokenAuthentication]

    def perform_create(self, serializer):
        print(serializer)
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content')
        if content is None:
            content = title
        serializer.save(user=self.request.user, content=content)
        return super().perform_create(serializer)
    
    # def get_queryset(self, *args, **kwargs):
    #     qs = super().get_queryset(*args, **kwargs)
    #     request = self.request
    #     print(request.user)
    #     return qs.filter(user = request.user)
        

class ProductDetailAPIView(StaffEditorPermissionMixin, generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDestroyAPIView(StaffEditorPermissionMixin, generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_destroy(self, instance):
        super().perform_destroy(instance)

class ProductUpdateAPIView(StaffEditorPermissionMixin, generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.content:
            instance.content = instance.title








class ProductMixinView(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)







@api_view(['POST', "GET"])
def product_alt_view(request, pk=None, *args, **kwargs):
    method = request.method

    if method == "GET":
        if pk is not None:
            obj = get_object_or_404(Product, pk=pk)
            data = ProductSerializer(obj, many=False)
            return Response(data)
        queryset = Product.objects.all()
        data = ProductSerializer(queryset, many=True)
        return Response(data)

    if method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            title = serializer.validated_data.get('title')
            content = serializer.validated_data.get('content')
            if content is None:
                content = title
                serializer.save(content=content)
                return Response(serializer.data)
            return Response({'invalid': 'not good data'}, status=400)

