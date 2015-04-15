from django.contrib import admin
from task.models import Employee, Task, Report, Message

admin.site.register(Employee)
admin.site.register(Task)
admin.site.register(Report)
admin.site.register(Message)
# Register your models here.
