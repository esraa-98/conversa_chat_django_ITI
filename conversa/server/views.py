from django.db.models import Count
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.response import Response

from .models import Category, Server
from .schema import server_list_docs
from .serializer import CategorySerializer, ServerSerializer


class CategoryListViewSet(viewsets.ViewSet):
    queryset = Category.objects.all()

    @extend_schema(responses=CategorySerializer)
    def list(self, request):
        serializer = CategorySerializer(self.queryset, many=True)
        return Response(serializer.data)


class ServerListViewSet(viewsets.ViewSet):
    queryset = Server.objects.all()

    @server_list_docs
    def list(self, request):

        # get category
        category = request.query_params.get("category")
        # no.servers
        quantity = request.query_params.get("quantity")
        # user is logged in
        by_user = request.query_params.get("by_user") == "true"

        by_serverId = request.query_params.get("by_serverId")

        with_num_members = request.query_params.get(
            "with_num_members") == "true"

        # can't access server if user not logged in
        # if by_user or by_serverId and not request.user.is_authenticated:
        #     raise AuthenticationFailed

        if category:
            self.queryset = self.queryset.filter(category__name=category)

        if by_user:
            if by_user and request.user.is_authenticated:
                user_id = request.user.id
                self.queryset = self.queryset.filter(member=user_id)
            else:
                raise AuthenticationFailed

        if with_num_members:
            self.queryset = self.queryset.annotate(num_members=Count("member"))

        if by_serverId:
            # if not request.user.is_authenticated:
            #   raise AuthenticationFailed()
            try:
                self.queryset = self.queryset.filter(id=by_serverId)
                if not self.queryset.exists():
                    raise ValidationError(
                        detail=f"server with id {by_serverId} not found")
            # raise error in case : send boolean instead integer
            except ValueError:
                raise ValidationError(detail="server value error")

        # get specific no.servers
        if quantity:
            self.queryset = self.queryset[: int(quantity)]

        serializer = ServerSerializer(self.queryset, many=True, context={
                                      "num_members": with_num_members})
        return Response(serializer.data)
