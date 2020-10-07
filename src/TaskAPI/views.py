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
        data = {
            **request.data,
            'user':request.user.id,
        }
        task = TaskSerializer(data=data)
        if task.is_valid():
            task.save()
            action = Action.objects.create(text=f'Вы создали {task.data["title"]}',user=request.user)
            return Response(status=status.HTTP_201_CREATED, data=task.data)
        return Response(status=status.HTTP_400_BAD_REQUEST,data={'message':'not valid data'})

        
    def get(self, request):
        f = TaskFilter(request.GET, queryset=Task.objects.filter(user=request.user))
        serializer = TaskSerializer(f.qs, many=True)
        return Response(serializer.data)


class UpdateOrDeleteView(APIView):
    permission_classes = [IsAuthenticated]


    def get(self, request, pk):
        task = Task.objects.get(user=request.user, id=pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data)


    def delete(self, request, pk):
        try:
            task = Task.objects.filter(user=request.user).get(id=pk)
            task.delete()
            action = Action.objects.create(text=f'Вы удалили {task.title}',user=user)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND ,data= {'message':'task not found'})
        return Response({'message':'succesfull deleted'})
    

    def patch(self, request, pk):
        task = Task.objects.get(id=pk, user=request.user)
        if task:
            serializer = TaskSerializer(task, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                action = Action.objects.create(text=f'Вы изменили {task.title} , {TaskSerializer(task).data} на {request.data}',user=request.user)
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
        actions = Action.objects.filter(user=request.user).order_by('-date')
        serializer = ActionSerializer(actions, many=True)
        return Response(serializer.data)

