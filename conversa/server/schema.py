from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter,extend_schema
from .serializer import ServerSerializer
from rest_framework import status

server_list_docs = extend_schema(
         responses=ServerSerializer(many=True),
         parameters=[
             OpenApiParameter(
                 name="category",
                 type=OpenApiTypes.STR,
                 location=OpenApiParameter.QUERY,
                 description="category of servers to retrieve",
             ),
             OpenApiParameter(
                 name="quantity",
                 type=OpenApiTypes.INT,
                 location=OpenApiParameter.QUERY,
                 description="Number of servers to retrieve",
             ),
             OpenApiParameter(
                 name="by_user",
                 type=OpenApiTypes.BOOL,
                 location=OpenApiParameter.QUERY,
                 description="filter servers by the current authenticated user (true/false)",
             ),
             OpenApiParameter(
                 name="by_serverId",
                 type=OpenApiTypes.INT,
                 location=OpenApiParameter.QUERY,
                 description="include server by id",
             ),
             OpenApiParameter(
                 name="with_num_members",
                 type=OpenApiTypes.BOOL,
                 location=OpenApiParameter.QUERY,
                 description="include number of members for each server",
             ),

         ],                                                     
)

# server_create_docs = extend_schema(
#         parameters=[
#             OpenApiParameter(
#                 name='name',
#                 type=OpenApiTypes.STR,
#                 description='Name of the server',
#                 required=True,
#                 location=OpenApiParameter.QUERY,
#             ),
#             OpenApiParameter(
#                 name='owner',
#                 type=OpenApiTypes.INT,
#                 description='ID of the server owner (User)',
#                 required=True,
#                 location=OpenApiParameter.QUERY,
#             ),
#             OpenApiParameter(
#                 name='category',
#                 type=OpenApiTypes.STR,
#                 description='name of the server category',
#                 required=True,
#                 location=OpenApiParameter.QUERY,
#             ),
#             OpenApiParameter(
#                 name='description',
#                 type=OpenApiTypes.STR,
#                 description='Description of the server',
#                 required=False,
#                 location=OpenApiParameter.QUERY,
#             ),
#             OpenApiParameter(
#                 name='members',
#                 type={'type': 'array', 'items': {'type': 'string'}},
#                 description='List of member usernames',
#                 required=False,
#                 location=OpenApiParameter.QUERY,
#             ),
#             OpenApiParameter(
#                 name='banner',
#                 type=OpenApiTypes.BINARY,
#                 description='Server banner image file',
#                 required=False,
#                 location=OpenApiParameter.QUERY,
#             ),
#             OpenApiParameter(
#                 name='icon',
#                 type=OpenApiTypes.BINARY,
#                 description='Server icon image file',
#                 required=False,
#                 location=OpenApiParameter.QUERY,
#             ),
#         ],
#         responses={status.HTTP_201_CREATED: ServerSerializer},
# )

    