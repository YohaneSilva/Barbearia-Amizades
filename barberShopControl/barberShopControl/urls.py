from django.urls import path, include

urlpatterns = [
    path('', include('core.urls')),
]

handler404 = 'core.views.error_404_view'