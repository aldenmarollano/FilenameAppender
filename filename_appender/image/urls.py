from .views import upload_images, upload_view, download_image, reset_view
from django.urls import path

app_name = "image"
urlpatterns = [
    path('', upload_images, name='upload_images'),
    path('upload/', upload_view, name='success'),
    path('delete/', reset_view, name='delete'),
    path('upload/<int:image_id>', download_image, name='download'),
]