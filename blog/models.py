from django.db import models
from django.contrib.auth.models import User
import os

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):   #관리자페이지(admin)의 Tags목록에 이름을 보이게 하기
        return self.name

    def get_absolute_url(self): # IP주소/blog/tag/슬러그명/
        return f'/blog/tag/{self.slug}/'

class Category(models.Model):  # 카테고리 모델
    name = models.CharField(max_length=50, unique=True) # name 필드 : 각 카테고리의 이름, 동일한  name 불가
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)
    # SlugField : 사람이 읽을 수 있는 텍스트로 고유 URL생성, allow_unicode : SlugField의 한글지원

    def __str__(self):
        return self.name

    def get_absolute_url(self): #카테고리의 레코드별 URL 생성 규칙 정의
        return f'/blog/category/{self.slug}'
        # urls.py에서 상세페이지 url은 /blog/category/slug필드 로 정함 -> 그대로 url생성

    class Meta:  # Category의 메타 설정에서 복수형 이름 직접 지정 -> 관리자 페이지에 메뉴이름 Categories로
        verbose_name_plural = 'Categories'

class Post(models.Model):
    title = models.CharField(max_length=30) #CharField: 문자를 담는 필드(최대길이=30)
    hook_text = models.CharField(max_length=100, blank=True) # 데이터 자체가 변경됨->migration필수!
    content = models.TextField() # 문자열의 길이 제한X

    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)  # _media 생략됨 _media/blog/images/
    # %Y 2022 / %y 22
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d/', blank=True)
    created_at = models.DateTimeField() #DateTimeField: 월,일,시,분,초 기록할 수 있게 해주는 필드

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #User 모델을 사용하여 author 작성(모델에서 외래키를 구현할때)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    #Category 모델을 사용하여 category 작성
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag, blank=True)  # 다대다관계, null=True 필요X(자동으로 비움)

    def __str__(self):  #관리자페이지(admin)의 포스트 목록에 제목을 보이게 하기
        return f'[{self.pk}]{self.title}:: {self.author} : {self.created_at}'
        # self.pk : 해당 포스트의 pk값(각 레코드에 대한 고유값, 모델을 만들면 기본적으로 생성됨) , self.title : 해당 포스트의 제목
    def get_absolute_url(self): #포스트의 레코드별 URL 생성 규칙 정의
        return f'/blog/{self.pk}/' # urls.py에서 상세페이지 url은 /blog/레코드의pk/ 로 정함 -> 그대로 url생성

    def get_file_name(self):
        return os.path.basename(self.file_upload.name)

    def get_file_ext(self):
        return self.get_file_name().split('.')[-1]
        # ~.txt ~~.docx 등을 가져옴 ->스플릿에 의해서 ~ txt / ~~ docx 두개로 쪼개서 배열스트링에 전달
        # a.b.c.txt -> a b c txt 로 쪼개지면 -> 배열에서 제일 마지막이 확장자임 (제일 마지막 원소 표시 : -1)