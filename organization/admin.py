from django.contrib import admin

from .models import CustomToken
from .models import Organization
from .models import TodoItem

admin.site.register(Organization)
admin.site.register(TodoItem)
admin.site.register(CustomToken)
