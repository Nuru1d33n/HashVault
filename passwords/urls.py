from django.urls import path
from . import views

urlpatterns = [
    # Home page
    path('', views.index, name='index'),

    # Handle password input (textarea, file, or manual input)
    path('handle-password/', views.handle_password, name='handle_password'),

    # View hashes related to a password
    path('password/<int:password_id>/hashes/', views.hash_password, name='hash_password'),

    # Check if a hash exists in the database
    path('check-hash/', views.check_hash, name='check_hash'),

]
