from rest_framework import serializers
from django.db import transaction, DatabaseError
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password



from .models import Task, Action


class TaskSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('date',)


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        try:
            with transaction.atomic():
                user = User.objects.create(
                    username=validated_data['username']
                )
                user.set_password(validated_data['password'])
                user.save()
                return user
        except DatabaseError:
            return {'message':'create user error'}


        

    class Meta:
        model = User
        fields = ( "id", "username", "password", )


class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = ('text','date')

