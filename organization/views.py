from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Organization
from .models import TodoItem
from .serializers import OrganizationSerializer
from .serializers import ToDoItemSerializer


class TodoViewList(APIView):
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
    def get(self, request, pk):
        organization = get_object_or_404(Organization.objects.all(), pk=pk)
        todo_items = TodoItem.objects.filter(organization=organization)
        todo_item_serializer = ToDoItemSerializer(todo_items, many=True)
        return Response({"todo_items": todo_item_serializer.data})
