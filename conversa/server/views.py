from django.db.models import Count
from rest_framework import status
from rest_framework import viewsets
from drf_spectacular.utils import extend_schema
from rest_framework.exceptions import ValidationError,AuthenticationFailed
from rest_framework.permissions import IsAuthenticated #Is Authenticated
from .serializer import ServerSerializer,CategorySerializer
from .schema import server_list_docs
from rest_framework.response import Response
from .models import Server,Category

class CategoryListViewSet(viewsets.ViewSet):
    queryset = Category.objects.all()

    @extend_schema(responses=CategorySerializer)
    def list(self, request):
        serializer = CategorySerializer(self.queryset, many=True)
        return Response(serializer.data)
    

class ServerListViewSet(viewsets.ViewSet):
    queryset = Server.objects.all()
    # permission_classes = [IsAuthenticated]
    
    @server_list_docs
    def list(self,request):
        """
        List all servers, or filter the list by category, user, quantity, or server ID.

        **Request Parameters:**

        * `category`: The name of the server category to filter by.
        * `quantity`: The number of servers to return.
        * `by_user`: Whether to filter the list to only servers that the current user is a member of.
        * `by_serverId`: Whether to filter the list to only the server with the specified ID.
        * `with_num_members`: Whether to annotate the response with the number of members of each server.

        **Returns:**

        A Response object containing a list of servers, serialized in JSON. Each server object will include the following fields:

        * `id`: The server ID.
        * `name`: The server name.
        * `category`: The server category.
        * `description`: The server description.
        * `member_count`: The number of members of the server (if `with_num_members` is specified).

        **Raises:**

        * AuthenticationFailed: If the user is not logged in and attempts to access servers by user or by server ID.
        * ValidationError: If the `category`, `quantity`, or `serverId` parameter is invalid.

        **Examples:**

        * List all servers:

            ```
            GET /servers
            ```

        * List servers in the "Gaming" category:

            ```
            GET /servers?category=Gaming
            ```

        * List the top 10 servers by number of members:

            ```
            GET /servers?with_num_members=true&quantity=10&by_num_members=desc
            ```

        * Get the server with ID 12345:

            ```
            GET /servers?by_serverId=12345
            ```

        * List all servers that the current user is a member of:

            ```
            GET /servers?by_user=true
            ```
        """
        # get category
        category = request.query_params.get("category")
        # no.servers
        quantity = request.query_params.get("quantity")
        # user is logged in
        by_user = request.query_params.get("by_user") == "true"

        by_serverId = request.query_params.get("by_serverId")

        with_num_members = request.query_params.get("with_num_members") == "true"

        
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
            #if not request.user.is_authenticated:
            #   raise AuthenticationFailed()
            try:
                self.queryset = self.queryset.filter(id=by_serverId)    
                if not self.queryset.exists():
                    raise ValidationError(detail=f"server with id {by_serverId} not found")
            #raise error in case : send boolean instead integer 
            except ValueError:
                raise ValidationError(detail="server value error")
            
        # get specific no.servers
        if quantity:
            self.queryset = self.queryset[: int(quantity)]
        
        
    
        serializer = ServerSerializer(self.queryset,many=True,context={"num_members":with_num_members})
        return Response(serializer.data)


# class ServerCreateViewSet(viewsets.ViewSet):
#     serializer_class = ServerSerializer

#     @server_create_docs
#     def create(self, request):
#         """
#           Create a new server.

#             **Args:**
#                 request (Request): The HTTP request object containing the server data.

#             **Returns:**
#                 Response: A JSON response containing the created server data or validation errors.

#             **Raises:**
#                 N/A

#             **Example:**
#                 The following example demonstrates how to create a new server using a POST request:

#                 ```bash
#                 POST /api/server/create
#                 {
#                     "name": "My Server",
#                     "category": "Gaming",
#                     "description": "A gaming community server",
#                     "members": ["user1", "user2"],
#                     "banner": upload image,
#                     "icon": upload icon,
#                 }
#                 ```

#             Note:
#                 This method uses the ServerSerializer for data validation and saving. If the provided data is
#                 valid, the server is saved, and a response with the server data and HTTP status 201 Created is returned.
#                 If there are validation errors, a response with the errors and HTTP status 400 Bad Request is returned.
#         """
        
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


