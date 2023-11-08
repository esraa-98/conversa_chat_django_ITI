from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter,extend_schema
from .serializer import ChannelSerializer,ServerSerializer

server_list_docs = extend_schema(responses=ServerSerializer(many=True),
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

         ]                        
                                 
)