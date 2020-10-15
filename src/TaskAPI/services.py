import django_filters
from rest_framework import status


from .models import Task, Action
from .serializers import TaskSerializer, UserSerializer


class TaskFilter(django_filters.FilterSet):
    class Meta:
        model = Task
        fields = ['status', 'end_date', ]


def create_task(request: dict) -> (int, dict):
    data = {
        **request.data,
        'user': request.user.id,
    }
    task = TaskSerializer(data=data)
    if task.is_valid():
        task.save()
        Action.objects.create(
            text=f'Вы создали {task.data["title"]}',
            user=request.user
        )
        return status.HTTP_201_CREATED, task.data
    else:
        status.HTTP_400_BAD_REQUEST, {'message': 'not valid data'}


def create_user(request: dict) -> (int, dict):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return status.HTTP_201_CREATED, {'id': serializer.data.id, 'username': serializer.data.username}
    else:
        return status.HTTP_400_BAD_REQUEST, {'message': 'not valid data'}


def get_task_list(request: dict) -> dict:
    f = TaskFilter(request.GET, queryset=Task.objects.filter(user=request.user))
    serializer = TaskSerializer(f.qs, many=True)
    return serializer.data


def get_task(request: dict, pk: int) -> (int, dict):
    task = Task.objects.get(user=request.user, id=pk)
    serializer = TaskSerializer(task)
    return serializer.data


def delete_task(request: dict, pk: int) -> (int, dict):
    try:
        task = Task.objects.filter(user=request.user).get(id=pk)
        task.delete()
        Action.objects.create(text=f'Вы удалили {task.title}', user=request.user)
    except Task.DoesNotExist:
        return status.HTTP_404_NOT_FOUND, {'message': 'task not found'}
    return status.HTTP_200_OK, {'message': 'succesfull deleted'}


def patch_task(request: dict, pk: int) -> (int, dict):
    try:
        task = Task.objects.get(id=pk, user=request.user)
    except Task.DoesNotExist:
        task = None
    if task:
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            Action.objects.create(text=f'Вы изменили {task.title} , {TaskSerializer(task).data} на {request.data}', user=request.user)
            return status.HTTP_200_OK, serializer.data
        else:
            return status.HTTP_400_BAD_REQUEST, {'message': 'not valid data'}

    else:
        return status.HTTP_404_NOT_FOUND, {'message': 'task not found'}
