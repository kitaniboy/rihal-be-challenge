"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from django.contrib import admin
from django.urls import path

from app.endpoints.DocumentEndpoint import DocumentEndpoint
from app.endpoints.authentication import register
from app.endpoints import (
    get_occurrences,
    list_documents,
    get_sentences,
    add_document,
    word_search,
    get_page,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('document/', add_document, name='add_document'),
    path('documents/', list_documents, name='list_documents'),
    path('search/', word_search, name='word_search'),
    path('document/<int:id>', DocumentEndpoint.as_view(), name='document'),
    path('document/<int:id>/page/<int:num>', get_page, name='page'),
    path('document/<int:id>/sentences', get_sentences, name='entences'),
    path('document/<int:id>/top', get_occurrences, name='occurrences'),
    path('register/', register, name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
