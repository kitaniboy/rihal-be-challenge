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
from django.contrib import admin
from django.urls import path

from app.endpoints.DocumentEndpoint import DocumentEndpoint
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
    path('document/', add_document),
    path('documents/', list_documents),
    path('search/', word_search),
    path('document/<int:id>', DocumentEndpoint.as_view()),
    path('document/<int:id>/page/<int:num>', get_page),
    path('document/<int:id>/sentences', get_sentences),
    path('document/<int:id>/occurrences', get_occurrences),
    path('document/<int:id>/top', get_occurrences),
]
