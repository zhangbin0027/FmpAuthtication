from django.db import models
# from django.contrib.auth.models import AbstractUser

class UserInfo(models.Model):
    user_type_choices = (
        (1, '普通用户'),
        (2, 'VIP'),
        (3, 'SVIP')
    )
    user_type = models.IntegerField(choices=user_type_choices)
    username = models.CharField(max_length=32, unique=True, verbose_name="用户名")
    password = models.CharField(max_length=64, verbose_name="密码")
    phone = models.CharField(max_length=32, null=True, blank=True, verbose_name="手机号码")
    # phone =models.CharField(max_length=32, null=True, blank=True, verbose_name="手机号码")

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = '用户表'
        verbose_name_plural = '用户表'

class UserToken(models.Model):
    user = models.OneToOneField(to='UserInfo',on_delete=models.CASCADE)
    token = models.CharField(max_length=64)

    def __str__(self):
        return self.user

    class Meta:
        verbose_name = 'token表'
        verbose_name_plural = 'token表'

