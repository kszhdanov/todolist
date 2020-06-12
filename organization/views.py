from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Organization
from .models import CustomToken
from .models import TodoItem
from .serializers import OrganizationSerializer
from .serializers import ToDoItemSerializer


class TodoViewList(APIView):
    permission_classes = [IsAuthenticated & IsAdminUser]

    def get(self, request):
        todo_items = TodoItem.objects.all()
        serializer = ToDoItemSerializer(todo_items, many=True)
        return Response({"todo_items": serializer.data})

    def post(self, request):
        todo_item = request.data.get('todo_item')
        serializer = ToDoItemSerializer(data=todo_item)
        if serializer.is_valid(raise_exception=True):
            todo_item_saved = serializer.save()
        return Response({
            "status": "Success",
            "detail": f"Todo item '{todo_item_saved.short_desc()}' created successfully"
        })


class TodoViewDetail(APIView):
    permission_classes = [IsAuthenticated & IsAdminUser]

    def get(self, request, pk):
        todo_item = get_object_or_404(TodoItem.objects.all(), pk=pk)
        serializer = ToDoItemSerializer(todo_item, many=False)
        return Response({"todo_item": serializer.data})

    def put(self, request, pk):
        todo_item = get_object_or_404(TodoItem.objects.all(), pk=pk)
        data = request.data.get('todo_item')
        serializer = ToDoItemSerializer(instance=todo_item, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            todo_item = serializer.save()
        return Response({
            "status": "Success",
            "detail": f"Todo item '{todo_item.short_desc()}' updated successfully"
        })

    def delete(self, request, pk):
        todo_item = get_object_or_404(TodoItem.objects.all(), pk=pk)
        todo_item.delete()
        return Response({
            "status": "Success",
            "detail": f"Todo item with id '{pk}' has been deleted."
        }, status=204)


class OrganizationViewList(APIView):
    permission_classes = [IsAuthenticated & IsAdminUser]

    def get(self, request):
        organizations = Organization.objects.all()
        serializer = OrganizationSerializer(organizations, many=True)
        return Response({"organizations": serializer.data})

    def post(self, request):
        organization = request.data.get('organization')
        serializer = OrganizationSerializer(data=organization)
        if serializer.is_valid(raise_exception=True):
            organization_saved = serializer.save()
        return Response({
            "status": "Success",
            "detail": f"Organization '{organization_saved}' created successfully"
        })


class OrganizationViewDetail(APIView):
    permission_classes = [IsAuthenticated & IsAdminUser]

    def get(self, request, pk):
        organization_saved = get_object_or_404(Organization.objects.all(), pk=pk)
        serializer = OrganizationSerializer(instance=organization_saved, many=False)
        return Response({"organization": serializer.data})

    def put(self, request, pk):
        organization = get_object_or_404(Organization.objects.all(), pk=pk)
        data = request.data.get('organization')
        serializer = OrganizationSerializer(instance=organization, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            organization = serializer.save()
        return Response({
            "status": "Success",
            "detail": f"Organization '{organization}' updated successfully"
        })

    def delete(self, request, pk):
        organization_saved = get_object_or_404(Organization.objects.all(), pk=pk)
        organization_saved.delete()
        return Response({
            "status": "Success",
            "detail": f"Organization with id '{pk}' has been deleted."
        }, status=204)


class OrganizationTodoListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        organization = get_object_or_404(Organization.objects.all(), pk=pk)
        if request.auth.organization != organization:
            return Response({
                "status": "Failure",
                "detail": "Authorized in another organization"
            }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            todo_items = TodoItem.objects.filter(organization=organization)
            todo_item_serializer = ToDoItemSerializer(todo_items, many=True)
            return Response({"todo_items": todo_item_serializer.data})


class CustomAuthTokenView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        organization_pk = int(kwargs.get('pk', None))
        if organization_pk is None:
            return Response({
                "status": "Failure",
                "detail": "No organization PK"
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            organization_to_auth = get_object_or_404(Organization.objects.all(), pk=organization_pk)
            organization_users = [user.username for user in organization_to_auth.users.all()]
            passed_user = serializer.validated_data['user']
            user = get_object_or_404(User.objects.all(), username=passed_user.username)
            if not user.is_active:
                return Response({
                    "status": "Failure",
                    "detail": "User deleted"
                }, status=status.HTTP_406_NOT_ACCEPTABLE)
            if passed_user.username in organization_users:
                try:
                    token = CustomToken.objects.get(user=passed_user)
                except CustomToken.DoesNotExist:
                    token = None
                if token:
                    if token.organization.pk == organization_to_auth.pk:
                        pass
                    else:
                        token.delete()
                token, created = CustomToken.objects.get_or_create(user=passed_user, organization=organization_to_auth)
            else:
                return Response({
                    "status": "Failure",
                    "detail": f"User not in organization {organization_to_auth}"
                }, status=status.HTTP_400_BAD_REQUEST)
            return Response({'token': token.key})
