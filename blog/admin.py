from django.contrib import admin
from .models import Post, Category  # Post, Category 모델 임포트

# Register your models here.
admin.site.register(Post)  #관리자 페이지에 Post 모델 등록

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name',)}
    # Category 모델의 name 필드에 값이 입력됐을 때 자동으로 slug 생성됨.

admin.site.register(Category, CategoryAdmin) #관리자 페이지에 Category 모델 등록