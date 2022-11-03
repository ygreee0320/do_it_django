from django.shortcuts import render
from .models import Post, Category
from django.views.generic import ListView, DetailView

# Create your views here.
class PostList(ListView):  #클래스이름:모델명+리스트
    model = Post
    ordering = '-pk'

    def get_context_data(self, *, object_list=None, **kwargs):  #카테고리 카드를 채우기 위한 정보 정의
        context = super(PostList,self).get_context_data()  # 기존에 제공했던 기능을 그대로 가져와 context에 저장
        context['categories'] = Category.objects.all()  # 모든 카테고리를 가져와 'categories'라는 키에 연결해 담기
        context['no_category_post_count'] = Post.objects.filter(category=None).count
        #카테고리가 지정되지 않은 포스트의 개수를 세어, 'no_category_post_count'에 담기
        return context

def category_page(request, slug):  #매개변수로 꼭필요한 request 이외에 slug까지 설정
    if slug == 'no_category' : #만약 매개변수(slug) 값이 'no_category'라면
        category = '미분류'  # category 변수에 실제 Category 모델의 레코드가 아닌, '미분류'문자열 저장
        post_list = Post.objects.filter(category=None)
    else :
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)
    return render(request, 'blog/post_list.html', {
        'category' : category,
        'post_list' : post_list,
        'categories' : Category.objects.all(),
        'no_category_post_count' : Post.objects.filter(category=None).count
    })

    # 템플릿 필요, 이름: 모델명_list.html : post_list.html <-자동생성
    # 파라미터(자동으로 전달되는 데이터) -> 모델명_list : post_list

class PostDetail(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data() # 기존에 제공했던 기능을 그대로 가져와 context에 저장
        context['categories'] = Category.objects.all()  #모든 카테고리를 가져와 'categories'키에 연결해 담기
        context['no_category_post_count'] = Post.objects.filter(category=None).count #카테고리가 지정되지 않은 개수
        return context

    # 템플릿 모델명_detail.html : post_detail.html
    # 파라미터(자동으로 전달되는 데이터) -> 모델명 : post

#def index(request):
#    posts1 = Post.objects.all().order_by('-pk') # 역순 출력
#    return render (request, 'blog/index.html', {'posts': posts1})

#def single_post_page(request, pk):
#    post2 = Post.objects.get(pk=pk)
#    return render(request, 'blog/single_post_page.html', {'post':post2})