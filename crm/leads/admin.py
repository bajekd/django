from django.contrib import admin

from .models import Agent, Category, FollowUp, Lead, User, UserProfile


class LeadAdmin(admin.ModelAdmin):
  list_display = ['first_name', 'last_name', 'age', 'email']
  list_display_links = ['first_name']
  list_editable = ['last_name', 'age', 'email']
  list_filter = ['category']
  search_fields = ['first_name', 'last_name', 'email']
  
  
admin.site.register(Category)
admin.site.register(User)
admin.site.register(Lead, LeadAdmin)
admin.site.register(UserProfile)
admin.site.register(Agent)
admin.site.register(FollowUp)
