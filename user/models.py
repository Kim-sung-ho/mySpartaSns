#user/models.py
from django.db import models
#장고에서사용하는 기본적인 모델 AbstractUser == (auth_user) 을 사용하겠다.
from django.contrib.auth.models import AbstractUser
#장고의 셋팅을 넣어준다.
from django.conf import settings


# 유저모델 클레스 models.Model을 상속받았다,수정함
class UserModel(AbstractUser):
    #db테이블의 이름을 설정
    class Meta:
        db_table ="my_user"

    bio = models.TextField(max_length=500, blank=True)
    follow = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='followee')

