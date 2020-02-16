from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from api import models
from rest_framework import exceptions
from rest_framework.authentication import BasicAuthentication

FMP_DICT = {
    1:{
        'id':'001',
        'note':'接口可用性低',
        'customername':'jiaofeng2'
    },
    2:{
        'id': '002',
        'note': 'BOS订单回调失败',
        'customername': 'zhanchangwen'
    },
}

def md5(user):
    import hashlib
    import time

    ctime = str(time.time())
    m = hashlib.md5(bytes(user, encoding='utf-8'))
    m.update(bytes(ctime, encoding='utf-8'))
    return m.hexdigest()


class AuthView(APIView):
    """
    用户登录认证
    """
    def post(self, request, *args, **kwargs):
        ret = {'code': 1000, 'msg': None}
        try:
            user = request.POST.get('username')
            pwd = request.POST.get('password')
            print(user, pwd)
            obj = models.UserInfo.objects.filter(username=user, password=pwd).first()
            if not obj:
                ret['code'] = 1001
                ret['msg'] = '用户名或密码错误'
            token = md5(user)
            ret['token'] = token
            models.UserToken.objects.update_or_create(user=obj, defaults={'token': token})
        except Exception as e:
            ret['code'] = '1002'
            ret['msg'] = '请求异常'
        return JsonResponse(ret)

class Authtication(object):

    def authenticate(self, request):
        token = request.GET.get('token')
        print(token)
        token_obj = models.UserToken.objects.filter(token=token).first()
        if not token_obj:
            raise exceptions.AuthenticationFailed('用户认证失败')
        # 将两个字段赋值给request以供后续使用
        return token_obj.user, token_obj

    def authenticate_header(self,request):
        pass

class FmpView(APIView):
    """"
    故障管理相关业务
    """
    authentication_classes = [Authtication]

    def get(self,request,*args,**kwargs):
        # request.user
        # request.auth
        ret = {'code': 1000, 'msg': None, 'data': None}
        try:
            ret['data'] = FMP_DICT
        except Exception as e:
            ret['code'] = '1002'
            ret['msg'] = '请求异常'
        return JsonResponse(ret)