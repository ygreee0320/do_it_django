from django.shortcuts import render, redirect

from .forms import CommentForm
from .models import Post, Category, Tag, Comment
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin   #author자동으로 넣기(+redirect)
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify
from .forms import CommentForm
from django.shortcuts import get_object_or_404
from django.db.models import Q

# Create your views here.
class PostUpdate(LoginRequiredMixin,UpdateView):
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category'] # , 'tags' 지움
    # 템플릿명: post_forms 자동 생성-> 겹치니까 다른 이름으로
    template_name = 'blog/post_update_form.html' #원래 제공하는 템플릿을 PostCreate가 사용해서 다른 템플릿 지정

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate,self).dispatch(request, *args, **kwargs)
        # 가입, 인증되었고 그 포스트의 작성자를 가져와서 현재 작성자와 같은지 확인
        else:
            raise PermissionDenied

    def form_valid(self, form):
        response = super(PostUpdate, self).form_valid(form)
        self.object.tags.clear()
        tags_str = self.request.POST.get('tags_str')
        if tags_str:  # 태그에 뭔가 있다면(NULL)이 아니라면
            tags_str = tags_str.strip()  # 문자열 앞뒤 빈칸 없앰
            tags_str = tags_str.replace(',',';')  # ,를 ;로 변경하고
            tags_list = tags_str.split(';')  # ; 단위로 쪼갬
            for t in tags_list:
                t = t.strip()
                tag, is_tag_created = Tag.objects.get_or_create(name=t)  # 기존의 태그라면 그 태그 사용, 아니라면 태그 생성
                if is_tag_created:  # 태그가 새로 만들어졌다면 (bool값이 true라면)
                    tag.slug = slugify(t, allow_unicode=True)
                    tag.save()
                self.object.tags.add(tag)
        return response

    def get_context_data(self, *, object_list=None, **kwargs):  #카테고리 카드를 채우기 위한 정보 정의
        context = super(PostUpdate,self).get_context_data()  # 기존에 제공했던 기능을 그대로 가져와 context에 저장
        if self.object.tags.exists():
            tags_str_list = list() #빈 리스트 생성
            for t in self.object.tags.all():
                tags_str_list.append(t.name) # tag의 name string 필드 가져와서 뒤에 넣기
            context['tags_str_default'] = ';'.join(tags_str_list)
        context['categories'] = Category.objects.all()  # 모든 카테고리를 가져와 'categories'라는 키에 연결해 담기
        context['no_category_post_count'] = Post.objects.filter(category=None).count
        #카테고리가 지정되지 않은 포스트의 개수를 세어, 'no_category_post_count'에 담기
        return context

class PostCreate(LoginRequiredMixin,UserPassesTestMixin,CreateView):  #사용자 입력
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category']  # , 'tags' 지움
    # 템플릿명: post_forms 자동 생성
    def test_func(self):  #이미 등록된, 상속받은 함수
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form):  #클래스 내의 함수-> 이벤트 발생 시 자동 실행
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_superuser or current_user.is_staff):
            # 가입,인증 되었고 슈퍼유저or 스텝유저 라면 현재 로그인된 유저로 자동 author
            form.instance.author = current_user
            response = super(PostCreate, self).form_valid(form)
            tags_str = self.request.POST.get('tags_str') #사용자가 작성한 정보 전달 방식(get,post)중 post (모델명이 아님)
            if tags_str:  #태그에 뭔가 있다면(NULL)이 아니라면
                tags_str = tags_str.strip() #문자열 앞뒤 빈칸 없앰
                tags_str = tags_str.replace(',', ';')  # ,를 ;로 변경하고
                tags_list = tags_str.split(';')  # ; 단위로 쪼갬
                for t in tags_list:
                    t = t.strip()
                    tag, is_tag_created = Tag.objects.get_or_create(name=t)  # 기존의 태그라면 그 태그 사용, 아니라면 태그 생성
                    if is_tag_created:  # 태그가 새로 만들어졌다면 (bool값이 true라면)
                        tag.slug = slugify(t, allow_unicode=True)
                        tag.save()
                    self.object.tags.add(tag)
            return response
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
    ordering = '-pk'  # 포스트 최신순
    paginate_by = 5   # 한 페이지에 5개 포스트 보여주기

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

class PostSearch(PostList):  # 포스트리스트가 상속 받고있는 ListView도 상속, post_list, post_list.html 자동 호출
    paginate_by = None

    def get_queryset(self):
        q = self.kwargs['q']
        post_list = Post.objects.filter( #필터를 통해 걸러내고 저장
            Q(title__contains=q) | Q(tags__name__contains=q)
        ).distinct()  # 같은 포스트가 여러개 검색되어도 하나만 출력
        return post_list
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostSearch, self).get_context_data()
        q = self.kwargs['q']
        context['search_info'] = f'Search : {q} ({self.get_queryset().count()})'
        return context

class PostDetail(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data() # 기존에 제공했던 기능을 그대로 가져와 context에 저장
        context['categories'] = Category.objects.all()  #모든 카테고리를 가져와 'categories'키에 연결해 담기
        context['no_category_post_count'] = Post.objects.filter(category=None).count #카테고리가 지정되지 않은 개수
        context['comment_form'] = CommentForm
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

def new_comment(request,pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)
        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()  # 서버에 코멘트 세이브
                return redirect(comment.get_absolute_url())
        else:  # GET
            return redirect(post.get_absolute_url())
    else:
        raise PermissionDenied

class CommentUpdate(UpdateView):
    model = Comment
    form_class = CommentForm
    # CreateView, UpdateView, form을 사용하면
    # 템플릿: 모델명_forms 로 자동 생성  (comment_form)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(CommentUpdate,self).dispatch(request, *args, **kwargs)
        # 가입, 인증되었고 그 포스트의 작성자를 가져와서 현재 작성자와 같은지 확인
        else:
            raise PermissionDenied

#def index(request):
#    posts1 = Post.objects.all().order_by('-pk') # 역순 출력
#    return render (request, 'blog/index.html', {'posts': posts1})

#def single_post_page(request, pk):
#    post2 = Post.objects.get(pk=pk)
#    return render(request, 'blog/single_post_page.html', {'post':post2})