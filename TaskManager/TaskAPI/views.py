from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated


from django.contrib.auth.models import User
from .models import Task
from .serializers import TaskSerializer, UserSerializer
from .service import get_user_id, TaskFilter


class CreateOrGetView(APIView):
    permission_classes = [IsAuthenticated]


    def post(self,request):                
        user_id = get_user_id(request)
        data = {
            **request.data,
            'user':user_id,
        }
        task = TaskSerializer(data=data)
        if task.is_valid():
            task.save()
            return Response(status=201)
        return Response(status=400,data={'error':'not valid data'})

        
    def get(self, request):
        user_id = get_user_id(request)
        f = TaskFilter(request.GET, queryset=Task.objects.filter(user=user_id))
        serializer = TaskSerializer(f.qs, many=True)
        return Response(serializer.data)


class UpdateOrDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        user_id = get_user_id(request)
        task = Task.objects.filter(id=pk, user=user_id)
        task.delete()
        return Response(status=200,data= {'message':'succesfull deleted'})
    

    def patch(self, request, pk):
        user_id = get_user_id(request)
        task = Task.objects.filter(id=pk, user=user_id).first()
        if task:
            serializer = TaskSerializer(task, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

        else:
            return Response(status=404,data= {'message':'task not found'})
    

class CreateUserView(CreateAPIView):
    model = User
    serializer_class = UserSerializer
