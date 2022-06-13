from django.shortcuts import render,redirect
# 같은폴더안에있는 models.py에 UserModel이란것을 import한다
from .models import UserModel
#HttpResponse 화면에 글자를 띄울때 사용
from django.http import HttpResponse
from django.contrib.auth import get_user_model#데이터베이스 안에 사용자가 있는지 검사하는 함수
from django.contrib import auth # 사용자 auth 기능
from django.contrib.auth.decorators import login_required

def sign_up_view(request):
    #조건문으로 GET,POST를 나눈다.
    if request.method =='GET':
        user=request.user.is_authenticated #로그인 확인
        if user:# 로그인이 되어있다면
            return redirect('/')
        else:# 로그인이 되어있지 않다면
            return render(request,'user/signup.html')
        #user/signup.html화면을 띄운다.
        return render(request,'user/signup.html')
    #post는 데이터를 전달해달라 요청 하는것
    elif request.method=='POST':
        #여기다가 db내용을 저장한다.
        #request.POST안에 많은데이터가있는데 그중에서'username'데이터를
        #get()메소드를 사용해서가져오는데 없다면 None으로 처리하고,이것을
        #username라는 변수에 저장하여 쓰겠다.
        username = request.POST.get('username',None)
        password = request.POST.get('password', None)
        password2 = request.POST.get('password2', None)
        bio = request.POST.get('bio', None)

        #패스워드와 확인패스워드가 같지않다면
        if password != password2:
            #다시한번 화면을 띄운다.
            return render(request,'user/signup.html')
        #같다면 아이디 중복검사를 한다.
        else:
            #get_user_model 은 데이터베이스 안에 사용자가 있는지 검사하는 함수
            exist_user = get_user_model().objects.filter(username=username)

            # filters는 조건을 확인하여 objectsid값을 가져온다.
            # exist_user = UserModel.objects.filter(username=username)
            if exist_user :
                print(exist_user)
                return render(request, 'user/signup.html')
            #패스워드와 확인패스워드가 같다면 저장!
            else:
                #create_user 바로 유저를 생성 해 줄 수 있는 함수 (간결해짐)
                UserModel.objects.create_user(username=username, password=password, bio=bio)
                # #new_uesr라는변수에 UserModel()클래스를 가져온다.
                # new_uesr = UserModel()
                # #UserModel()에 username 등등을 넣어준다.
                # new_uesr.username = username
                # new_uesr.password = password
                # new_uesr.bio = bio
                # #데이터베이스에저장하기위해 save()를써준다.
                # new_uesr.save()
                # #저장이 다된후 redirect()를 사용하여 로그인페이지로 간다.
                return redirect('/sign-in')

#장고의 기본기능을 추가해보기
def sign_in_view(request):
    if request.method == 'POST':
        #request.POST 요청한 포스트데이터가 다담겨있는데 거기에username,password를 가져온다는뜻
        username = request.POST.get('username',None)
        password = request.POST.get('password',None)

        #UserModel은 이미데이터베이스와 연결되어있는 클래스 어떤데이터를 가져올건지 조건을써준다.
        #.get(nsername=username)앞에 유저네임은 UserModel안에 정의한 username이다.
        #username을 적은 사용자가 있어야한다.
        #내가불러온 password가 클라이언트에서 post메소드로받은 password가 같다면

        me = auth.authenticate(request,username=username, password=password)#사용자 불러오기
        if me is not None:
            # request.session 요청한 포스트 데이터들이 있는데
            #세션은 사용자정보를 저장하는 공간이다. 쿠키?세션?
            #딕셔너리의 구조로 키값 = ['user'] 벨류 =  UserModel.objects.get(username=username).username
            # request.session['user'] = me.username
            # return HttpResponse(me.username)
            auth.login(request,me)
            return redirect('/')
        else:
            return redirect('/sign-in')
    elif request.method == 'GET':
        if request.method == 'GET':
            user = request.user.is_authenticated  # 로그인 확인
            if user:  # 로그인이 되어있다면
                return redirect('/')
            else:  # 로그인이 되어있지 않다면
                return render(request, 'user/signin.html')

@login_required #사용자가 로그인이 되어있어야만 접근 할 수 있는 함수
def logout(request):
    auth.logout(request) # 인증 되어있는 정보를 없애기
    return redirect("/")

# user/views.py

@login_required
def user_view(request):
    if request.method == 'GET':
        # 사용자를 불러오기, exclude와 request.user.username 를 사용해서 '로그인 한 사용자'를 제외하기
        user_list = UserModel.objects.all().exclude(username=request.user.username)
        return render(request, 'user/user_list.html', {'user_list': user_list})


@login_required
def user_follow(request, id):
    me = request.user
    #팔로우를 누르려는 사람
    click_user = UserModel.objects.get(id=id)
    #그사람을 팔로우하는 모든사람 중에서 내가 들어가 있다면, 빼준다.
    if me in click_user.followee.all():
        click_user.followee.remove(request.user)
    else:
        click_user.followee.add(request.user)
    return redirect('/user')

