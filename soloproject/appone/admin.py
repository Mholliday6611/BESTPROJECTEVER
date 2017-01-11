from django.contrib import admin
from models import UserProfile, Post, Category, Page, Comment
# Register your models here.
class PostAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug':('title',)}
class CategoryAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug':('name',)}
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Page)
admin.site.register(UserProfile)
