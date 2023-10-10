from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework import status

from django_filters.rest_framework import DjangoFilterBackend

from webapp.products.pagination import ProductPagination
from webapp.products.filters import ProductFilter
from webapp.products.models import Product
from webapp.products.serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """Product viewset to create, update, delete, list and retrieve products"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "id"
    http_method_names = ["get", "post", "put", "patch", "delete"]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = ProductPagination
    ordering = ("id",)

    def get_object(self):
        """Get product object"""
        obj = get_object_or_404(Product, id=int(self.kwargs.get("id")))
        return obj

    def list(self, request):
        # get queryset and filter
        queryset = self.filter_queryset(self.get_queryset())

        # paginate queryset
        page = self.paginate_queryset(queryset)

        if page is not None:
            # serialize page
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # serialize queryset
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # serialize product
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request):
        # serialize request data
        serializer = ProductSerializer(
            data=request.data)

        if serializer.is_valid():
            # create product
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)

        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, **kwargs):
        instance = self.get_object()
        # serialize request data
        serializer = self.get_serializer(
            instance, data=request.data, partial=False)

        if serializer.is_valid():
            # update product
            serializer.save()
            return Response(serializer.data)

        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, **kwargs):
        instance = self.get_object()
        # serialize request data
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)

        if serializer.is_valid():
            # update product
            serializer.save()
            return Response(serializer.data)

        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, **kwargs):
        instance = self.get_object()
        # delete product
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
