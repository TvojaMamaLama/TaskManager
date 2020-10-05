from django.urls import path, include


from rest_framework_simplejwt.views import TokenObtainPairView
from .views import CreateOrGetView, UpdateOrDeleteView, CreateUserView, HistoryView


urlpatterns = [
    path('user/registry/', CreateUserView.as_view(), name='registry'),
    path('user/token/', TokenObtainPairView.as_view(), name='get_token'),
    path('tasks/', CreateOrGetView.as_view(),name='create_or_get'),
    path('tasks/<int:pk>/', UpdateOrDeleteView.as_view(), name='update_or_delete'),
    path('tasks/history/', HistoryView.as_view()),
]