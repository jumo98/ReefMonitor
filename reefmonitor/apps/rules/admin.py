from django.contrib import admin

from .models import Rule, Violation, Hint

# Register your models here.
admin.site.register(Rule)
admin.site.register(Violation)
admin.site.register(Hint)