from django.db import models
import os

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=30)
    hook_text = models.CharField(max_length=100, blank=True) # 데이터 자체가 변경됨->migration필수!
    content = models.TextField()

    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)  # _media 생략됨 _media/blog/images/
    # %Y 2022 / %y 22
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d/', blank=True)
    created_at = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #추후 author 작성

    def __str__(self):
        return f'[{self.pk}]{self.title} : {self.created_at}'

    def get_absolute_url(self):
        return f'/blog/{self.pk}/'

    def get_file_name(self):
        return os.path.basename(self.file_upload.name)

    def get_file_ext(self):
        return self.get_file_name().split('.')[-1]
        # ~.txt ~~.docx 등을 가져옴 ->스플릿에 의해서 ~ txt / ~~ docx 두개로 쪼개서 배열스트링에 전달
        # a.b.c.txt -> a b c txt 로 쪼개지면 -> 배열에서 제일 마지막이 확장자임 (제일 마지막 원소 표시 : -1)