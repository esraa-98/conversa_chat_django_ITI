from django.db.models import Count
from django.http import Http404
from rest_framework import status
from rest_framework import viewsets
from drf_spectacular.utils import extend_schema
from rest_framework.exceptions import ValidationError,AuthenticationFailed
from .serializer import ServerListSerializer,CategorySerializer,ChannelSerializer,ServerSerializer
from .schema import server_list_docs
from rest_framework.response import Response
from .models import Server,Category,Channel
from rest_framework.permissions import AllowAny

class ChannelViewSet(viewsets.ModelViewSet):
    serializer_class = ChannelSerializer
    queryset = Channel.objects.all()

class CategoryViewSet(viewsets.ViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = (AllowAny,)


    def list(self, request,*args, **kwargs):
        # GET method for retrieving all categories
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        # POST method for creating a new category
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        # GET method for retrieving a single category by ID
        category = self.queryset.get(pk=pk)
        serializer = self.serializer_class(category)
        return Response(serializer.data)

    def update(self, request, pk=None):
        # PUT method for updating a category by ID
        category = self.queryset.get(pk=pk)
        serializer = self.serializer_class(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        # PATCH method for partially updating a category by ID
        category = self.queryset.get(pk=pk)
        serializer = self.serializer_class(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        # DELETE method for deleting a category by ID
        category = self.queryset.get(pk=pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ServerListViewSet(viewsets.ViewSet):
    serializer_class = ServerListSerializer
    queryset = Server.objects.all()
    
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

        by_serverId = request.query_params.get("by_serverid")

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
        
        
    
        serializer = self.serializer_class(self.queryset,many=True,context={"num_members":with_num_members})
        return Response(serializer.data)
    
class ServerViewSet(viewsets.ViewSet):
    serializer_class = ServerSerializer
    queryset = Server.objects.all()

    def create(self, request, *args, **kwargs):
        """
          Create a new server.

            **Args:**
                request (Request): The HTTP request object containing the server data.

            **Returns:**
                Response: A JSON response containing the created server data or validation errors.

            **Raises:**
                N/A

            **Example:**
                The following example demonstrates how to create a new server using a POST request:

                ```bash
                POST /api/server/create
                {
                    "name": "My Server",
                    "category": "Gaming",
                    "description": "A gaming community server",
                    "members": ["user1", "user2"],
                    "banner": upload image,
                    "icon": upload icon,
                }
                ```

            Note:
                This method uses the ServerSerializer for data validation and saving. If the provided data is
                valid, the server is saved, and a response with the server data and HTTP status 201 Created is returned.
                If there are validation errors, a response with the errors and HTTP status 400 Bad Request is returned.
        """
        
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        """
        Update a server instance.

        Args:
            request (Request): The HTTP request object containing the updated server data.
            pk (int): The primary key of the server.

        Returns:
            Response: A JSON response containing the updated server data or validation errors.

        Raises:
            N/A
        """
        server = self.get_object(pk)
        serializer = self.serializer_class(server, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # def partial_update(self, request, pk=None):
    #     """
    #     Partially update a server instance.

    #     Args:
    #         request (Request): The HTTP request object containing the partially updated server data.
    #         pk (int): The primary key of the server.

    #     Returns:
    #         Response: A JSON response containing the partially updated server data or validation errors.

    #     Raises:
    #         N/A
    #     """
    #     server = self.get_object(pk)
    #     serializer = self.serializer_class(server, data=request.data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        """
        Destroy a server instance.

        Args:
            request (Request): The HTTP request object.
            pk (int): The primary key of the server.

        Returns:
            Response: A 204 No Content response or a 404 Not Found response.

        Raises:
            N/A
        """
        server = self.get_object(pk)
        server.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def get_object(self, pk):
        try:
            return Server.objects.get(pk=int(pk))
        except Server.DoesNotExist:
            raise Http404
    

