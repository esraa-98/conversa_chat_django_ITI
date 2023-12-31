"""
URL configuration for conversa project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView,SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from server.views import ServerListViewSet,CategoryViewSet,ChannelViewSet,ServerViewSet
from django.conf import settings
from django.conf.urls.static import static
from webchat.consumer import WebChatConsumer
from webchat.views import MessageViewSet,ConversationViewSet
# from server.routers import routers
# automatic generate url
router = DefaultRouter()
router.register("api/server/select",ServerListViewSet)
router.register("api/server/channel",ChannelViewSet)
router.register("api/server/category", CategoryViewSet)
router.register("api/server",ServerViewSet)
router.register("api/messages",MessageViewSet,basename="message")
router.register("api/conversations", ConversationViewSet, basename='conversation')

urlpatterns = [
    path('admin/', admin.site.urls),
    # download schema
    path('api/docs/schema',SpectacularAPIView.as_view(),name="schema"),
    # show the swagger ui
    path('api/docs/schema/ui',SpectacularSwaggerView.as_view()),
]+ router.urls

websocket_urlpatterns = [
    # Map the path to the WebChatConsumer class using as_asgi() to convert it to an ASGI application.
    path("<str:serverId>/<str:channelId>",WebChatConsumer.as_asgi())
]

if settings.DEBUG:
    # Serve static files from MEDIA_ROOT during development
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
