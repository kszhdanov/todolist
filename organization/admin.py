from django.contrib import admin
from .models import Organization
from .models import TodoItem
from .models import CustomToken


admin.site.register(Organization)
admin.site.register(TodoItem)
admin.site.register(CustomToken)
