"""
URL configuration for AlgaecideDB project.

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
# from django.contrib import admin
# from django.urls import path, include
# from . import views

# from rest_framework.schemas import get_schema_view
# from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer
from django.contrib import admin
from django.urls import path, include                 # add this
from django.conf import settings
from django.conf.urls.static import static
# from algaecide.views import StatsView

# schema_view = get_schema_view(title='API DOC', renderer_classes=[SwaggerUIRenderer, OpenAPIRenderer])  # add



# router = routers.DefaultRouter()                      # add this
# router.register('algae', views.AlgaecideViewSet, 'algae')     # add this
# router.register('algaecide', views.AlgaecideViewSet, 'algaecide')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('algaecide/', include('algaecide.urls')) ,
    # path('stats/', StatsView.as_view(), name='stats'),        
    # path('algaecide/', include("algaecide.urls")),                # add this
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('api/docs/', schema_view, name='docs')  # add
]

if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
  urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)