import json
import time


from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User


from .models import Task
from .serializers import UserSerializer, TaskSerializer


client = Client()


def get_token():
    response = client.post(
            reverse('get_token'),
            {
            'username':'Natasha',
            'password':'1234567'
            }
        )
    authorization = 'JWT ' + response.data['access']
    return authorization


class AuthAndApiTest(TestCase):


    def setUp(self):
        user = User.objects.create(username='Natasha')
        user.set_password('1234567')
        user.save()

        Task.objects.create(
            title='Test',
            description='Test description',
            status='N',
            end_date='2020-10-13',
            user=user
        )


    def test_ok_registry(self):
        data = {
            'username':'nikita',
            'password':'1234567'
        }
        response = client.post(
            reverse('registry'),
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)


    def test_bad_registry(self):
        data = {
            'username':'nikita',
        }
        response = client.post(
            reverse('registry'),
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)


    def test_verify(self):
        response = client.get(
            reverse('create_or_get'),
            HTTP_AUTHORIZATION = get_token()
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)


    def test_get_tasks(self):
        response = client.get(
            reverse('create_or_get'),
            HTTP_AUTHORIZATION = get_token(),
            )
        user = User.objects.all().first()
        task = Task.objects.filter(user=user.id)
        serializer = TaskSerializer(task, many=True)
        self.assertEquals(response.data, serializer.data)

    
    def test_create_task(self):
        response = client.post(
            reverse('create_or_get'),
            {
                'title':'Test1',
                'description':'Test description 1',
                'status':'N',
                'end_date':'2020-10-13',
            },
            content_type='application/json',
            HTTP_AUTHORIZATION = get_token()
            )
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        