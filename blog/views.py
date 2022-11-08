from django.shortcuts import render, redirect
from .models import Post, Category, Tag
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin   #author자동으로 넣기(+redirect)

# Create your views here.
class PostCreate(LoginRequiredMixin,UserPassesTestMixin,CreateView):  #사용자 입력
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category']

    def test_func(self):  #이미 등록된, 상속받은 함수
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form):  #클래스 내의 함수-> 이벤트 발생 시 자동 실행
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_superuser or current_user.is_staff):
            # 가입,인증 되었고 슈퍼유저or 스텝유저 라면 현재 로그인된 유저로 자동 author
            form.instance.author = current_user
            return super(PostCreate, self).form_valid(form)
        else:
            return redirect('/blog/') #올바른 유저가 아니라면 그냥 블로그 부름

    # 템플릿 : 모델명_form.html
    def get_context_data(self, *, object_list=None, **kwargs):  #카테고리 카드를 채우기 위한 정보 정의
        context = super(PostCreate,self).get_context_data()  # 기존에 제공했던 기능을 그대로 가져와 context에 저장
        context['categories'] = Category.objects.all()  # 모든 카테고리를 가져와 'categories'라는 키에 연결해 담기
        context['no_category_post_count'] = Post.objects.filter(category=None).count
        #카테고리가 지정되지 않은 포스트의 개수를 세어, 'no_category_post_count'에 담기
        return context

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

def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug) #슬러그와 같은 슬러그의 태그를 가져옴
    post_list = tag.post_set.all()  #같은 태그의 모든 포스트를 포스트리스트에 넣기
    return render(request, 'blog/post_list.html', {
        'tag' : tag,  #위의 변수에 저장된 값 전달해서 넘겨주기
        'post_list' : post_list,
        'categories': Category.objects.all(),
        'no_category_post_count': Post.objects.filter(category=None).count
    })

    # 템플릿 모델명_detail.html : post_detail.html
    # 파라미터(자동으로 전달되는 데이터) -> 모델명 : post

#def index(request):
#    posts1 = Post.objects.all().order_by('-pk') # 역순 출력
#    return render (request, 'blog/index.html', {'posts': posts1})

#def single_post_page(request, pk):
#    post2 = Post.objects.get(pk=pk)
#    return render(request, 'blog/single_post_page.html', {'post':post2})