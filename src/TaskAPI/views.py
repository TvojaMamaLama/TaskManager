from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from rest_framework import status


from django.contrib.auth.models import User
from .models import Task, Action
from .serializers import TaskSerializer, UserSerializer, ActionSerializer
from .service import get_user_id, TaskFilter


class CreateOrGetView(APIView):
    permission_classes = [IsAuthenticated]


    def post(self,request):                
        user = User.objects.get(id=get_user_id(request))
        data = {
            **request.data,
            'user':user_id,
        }
        task = TaskSerializer(data=data)
        if task.is_valid():
            task.save()
            action = Action.objects.create(text=f'Вы создали {task.data["title"]}',user=user)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST,data={'error':'not valid data'})

        
    def get(self, request):
        user_id = get_user_id(request)
        f = TaskFilter(request.GET, queryset=Task.objects.filter(user=user_id))
        serializer = TaskSerializer(f.qs, many=True)
        return Response(serializer.data)


class UpdateOrDeleteView(APIView):
    permission_classes = [IsAuthenticated]


    def delete(self, request, pk):
        user = User.objects.get(id=get_user_id(request))
        try:
            task = Task.objects.filter(user=user).get(id=pk)
            task.delete()
            action = Action.objects.create(text=f'Вы удалили {task.title}',user=user)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND ,data= {'message':'task not found'})
        return Response({'message':'succesfull deleted'})
    

    def patch(self, request, pk):
        user = User.objects.get(id=get_user_id(request))
        task = Task.objects.get(id=pk, user=user)
        if task:
            serializer = TaskSerializer(task, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                action = Action.objects.create(text=f'Вы изменили {task.title} , {TaskSerializer(task).data} на {request.data}',user=user)
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={'message':'not valid data'})

        else:
            return Response(status=status.HTTP_404_NOT_FOUND, data= {'message':'task not found'})
    

class CreateUserView(APIView):


    def post(self,request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST,data={'message':'not valid data'})


class HistoryView(APIView):
    permission_classes = [IsAuthenticated] 


    def get(self, request):
        user = User.objects.get(id = get_user_id(request))
        actions = Action.objects.filter(user=user).order_by('-date')
        serializer = ActionSerializer(actions, many=True)
        return Response(serializer.data)

