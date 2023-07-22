from rest_framework import serializers
from rest_framework.reverse import reverse

from api.serializers import UserPublicSerializer
from .models import Product
from .validators import validate_title_no_hello, unique_product_title

class ProductInLineSerializer(serializers.Serializer):
  url = serializers.HyperlinkedIdentityField('product-detail', lookup_field='pk', read_only=True)
  title = serializers = serializers.CharField(read_only=True)

class ProductSerializer(serializers.ModelSerializer):
    owner = UserPublicSerializer(source='user', read_only=True)
    edit_url = serializers.SerializerMethodField(read_only=True)
    url = serializers.HyperlinkedIdentityField('product-detail', lookup_field='pk')
    title = serializers.CharField(validators=[validate_title_no_hello, unique_product_title])
    class Meta:
        model = Product
        fields = [
            'owner',
            'url',
            'edit_url',
            'pk',
            'title',
            'content',
            'price',
            'sale_price',
            'public'
        ]

    # def validate_title(self, value): 
    #     request = self.context.get('request')
    #     user = request.user
    #     qs = Product.objects.filter(user=user, title__exact=value)
    #     if qs.exists():
    #         raise serializers.ValidationError('Is already a product name.') 
    #     return value

    def get_edit_url(self, obj):
        request = self.context['request']
        if request is None:
            return None
        return reverse('product-edit', kwargs={'pk': obj.pk},request=request)