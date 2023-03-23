from django.conf.urls.static import static
from django.urls import path
from django.conf import settings
from .views import *

urlpatterns = [
    path('', MainPageView.as_view(), name='home'),
    path('author/<str:id>/', AuthorDetailView.as_view(), name='author'),
    path('book-detail/<int:pk>/', BookDetailView.as_view(), name='detail'),
    path('add-book/', add_book, name='add-book'),
    path('delete-book/<int:pk>/', DeleteBookView.as_view(), name='delete-book'),
]