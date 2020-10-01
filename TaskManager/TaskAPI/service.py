from rest_framework_simplejwt.state import token_backend
import django_filters
from .models import Task


def get_user_id(request):
    token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
    payload = token_backend.decode(token, verify=True)                 
    user_id = payload.get('user_id')
    return user_id


class TaskFilter(django_filters.FilterSet):
    class Meta:
        model = Task
        fields = ['status','end_date']