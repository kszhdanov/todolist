from rest_framework import serializers

from .models import Organization, TodoItem


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ('id', 'title', 'users')


class ToDoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoItem
        fields = ('id', 'text', 'organization')
