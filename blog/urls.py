from django.urls import path
from . import views

urlpatterns = [   # IP주소/blog/
    path('', views.PostList.as_view()),  #인덱스부분 클래스로 대체
    path('<int:pk>/', views.PostDetail.as_view()),
    path('<int:pk>/new_comment/', views.new_comment),
    path('update_comment/<int:pk>/', views.CommentUpdate.as_view()),
    path('create_post/', views.PostCreate.as_view()),
    path('update_post/<int:pk>/', views.PostUpdate.as_view()),
    path('category/<str:slug>/', views.category_page), # IP주소/blog/category/슬러그명/ 입력시 : views.py의 category_page()함수로
    path('tag/<str:slug>/', views.tag_page),   # IP주소/blog/tag/슬러그명/ 입력시 : views.py의 tag_page()함수 호출

    #path('', views.index),  # IP주소/blog
    #path('<int:pk>/', views.single_post_page)
]