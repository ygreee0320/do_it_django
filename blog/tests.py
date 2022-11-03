from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post, Category
from django.contrib.auth.models import User  #author를 위해 User모델 임포트

# Create your tests here.
class TestView(TestCase): #클래스 이름: Test로 시작

    def setUp(self):  # 테스트를 위해 생성하는 것들
        self.client = Client()
        # User 레코드를 2개 생성
        self.user_kim = User.objects.create_user(username="kim", password="somepassword")
        self.user_lee = User.objects.create_user(username="lee", password="somepassword")
        # Category 레코드를 2개 생성
        self.category_com = Category.objects.create(name="computer", slug="computer")
        self.category_cul = Category.objects.create(name="culture", slug="culture")
        # Post 레코드 생성
        self.post_001 = Post.objects.create(title="첫번째 포스트",content="첫번째 포스트입니다",
                                     author=self.user_kim,   #작성자 self.user_kim 으로 지정
                                       category=self.category_com)
        self.post_002 = Post.objects.create(title="두번째 포스트", content="두번째 포스트입니다",
                                      author=self.user_lee,
                                       category=self.category_cul)
        self.post_003 = Post.objects.create(title="세번째 포스트", content="세번째 포스트입니다",
                                      author=self.user_lee)
    def nav_test(self, soup):   #navbar가 정상적으로 보이는 지 확인(호출 함수)
        navbar = soup.nav
        self.assertIn('Blog', navbar.text)
        self.assertIn('About Me', navbar.text)

        home_btn = navbar.find('a', text="Home")
        self.assertEqual(home_btn.attrs['href'], "/")
        blog_btn = navbar.find('a', text="Blog")
        self.assertEqual(blog_btn.attrs['href'], "/blog/")
        about_btn = navbar.find('a', text="About Me")
        self.assertEqual(about_btn.attrs['href'], "/about_me/")

    def category_test(self, soup):
        category_card = soup.find('div', id='category-card') #id가 category-card인 div요소 찾기
        self.assertIn('Categories', category_card.text) # 그 요소 안에 'Categories' 문구가 있는지 확인
        self.assertIn(f'{self.category_com} ({self.category_com.post_set.count()})', category_card.text)
        self.assertIn(f'{self.category_cul} ({self.category_cul.post_set.count()})', category_card.text)
        self.assertIn(f'미분류 (1)', category_card.text)  #모든 카테고리가 제대로 출력되어 있는지 확인

    def test_post_list(self):  #test로 시작하면 자동 실행됨
        response = self.client.get('/blog/')
        # response 결과가 정상적인지
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')
        # title이 정상적으로 보이는지
        self.assertEqual(soup.title.text, 'Blog')

        self.nav_test(soup)  # navbar가 정상적으로 보이는지 (함수 호출)
        self.category_test(soup)  # category가 정상적으로 보이는지 (함수 호출)

        self.assertEqual(Post.objects.count(), 3)  #포스트가 있는 경우

        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        main_area = soup.find('div', id="main-area")
        self.assertIn(self.post_001.title, main_area.text)
        self.assertIn(self.post_002.title, main_area.text)
        #메인 영역에서 작성자명이 나오는 지 확인, username.upper():작성자명 대문자
        self.assertIn(self.post_001.author.username.upper(), main_area.text)
        self.assertIn(self.post_002.author.username.upper(), main_area.text)
        self.assertNotIn('아무 게시물이 없습니다.', main_area.text)

        # Post가 정상적으로 보이는지
        # 1.맨처음엔 포스트가 하나도 안보임
        Post.objects.all().delete()
        self.assertEqual(Post.objects.count(), 0)

        response = self.client.get('/blog/')
        # response 결과가 정상적인지
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')

        main_area = soup.find('div', id="main-area")
        self.assertIn('아무 게시물이 없습니다.', main_area.text)

        # 2. Post가 있는 경우
       #post_001 = Post.objects.create(title="첫번째 포스트",content="첫번째 포스트입니다",
        #                               author=self.user_kim)
        #post_002 = Post.objects.create(title="두번째 포스트", content="두번째 포스트입니다",
        #                               author=self.user_lee)


    def test_post_detail(self):
        #post_001 = Post.objects.create(title="첫번째 포스트", content="첫번째 포스트입니다",
         #                              author=self.user_kim)
        self.assertEqual(self.post_001.get_absolute_url(), '/blog/1/')

        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.nav_test(soup) #카테고리 카드가 잘 만들어졌는 지 확인 (함수 호출)

        self.assertIn(self.post_001.title, soup.title.text) #포스트 영역에 카테고리가 있는지 확인

        main_area = soup.find('div', id='main-area')
        post_area = main_area.find('div', id='post-area')

        self.assertIn(self.post_001.title, post_area.text)
        self.assertIn(self.post_001.content, post_area.text)
        # 포스트 영역에서 작성자명이 나오는 지 확인, username.upper():작성자명 대문자
        self.assertIn(self.post_001.author.username.upper(), post_area.text)