from django.contrib import admin
from .models import UserModel

#이 코드가 나의UserModel을 admin에 추가해줍니다.
admin.site.register(UserModel)
