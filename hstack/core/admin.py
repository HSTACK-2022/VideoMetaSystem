from django.contrib import admin
from .models import Post, Category

admin.site.register(Post)

#name 필드에 값이 입력되면 자동으로 slug 생성
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}

admin.site.register(Category, CategoryAdmin)