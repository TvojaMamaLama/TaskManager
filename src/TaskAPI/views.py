from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


from .models import Action
from .serializers import ActionSerializer
from .services import create_task, create_user, get_task_list, get_task, delete_task, patch_task


class CreateOrGetListView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        status, data = create_task(request)
        return Response(status=status, data=data)

    def get(self, request):
        data = get_task_list(request)
        return Response(data)


class UpdateOrDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        data = get_task(request, pk)
        return Response(data)

    def delete(self, request, pk):
        status, data = delete_task(request, pk)
        return Response(status=status, data=data)

    def patch(self, request, pk):
        status, data = patch_task(request, pk)
        return Response(status=status, data=data)


class CreateUserView(APIView):

    def post(self, request):
        status, data = create_user(request)
        return Response(status=status, data=data)


class HistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        actions = Action.objects.filter(user=request.user).order_by('-date')
        serializer = ActionSerializer(actions, many=True)
        return Response(serializer.data)
