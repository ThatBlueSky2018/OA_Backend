from django.utils import timezone
from datetime import timedelta
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from rest_framework.views import APIView
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.viewsets import ViewSet

from .models import UserProfile
from .serializers import UserSerializer, UserMessageSerializer, UserPasswordSerializer, UserUpdateSerializer

TOKEN_EXPIRY_HOURS = 24  # Token过期时间（小时）


class UserRegisterView(GenericAPIView):
    """
    注册用户的视图
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  # 设置为所有人都可以注册(该视图类可能并不会使用到)
    throttle_classes = [ScopedRateThrottle, ]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': '请同时输入用户名和密码!'}, status=status.HTTP_400_BAD_REQUEST)

        if UserProfile.objects.filter(username__exact=username):
            return Response({"error": "该用户名已经存在!"}, status=HTTP_400_BAD_REQUEST)

        data = request.data.copy()
        serializer = self.get_serializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = UserProfile.objects.create_user(username=username, password=password,)
            token = Token.objects.create(user=user)
            return Response({'message': "注册成功！", 'token': token.key},
                            status=HTTP_201_CREATED)

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    """
    用户登录的视图
    """
    permission_classes = [AllowAny]
    throttle_scope = "post"
    throttle_classes = [ScopedRateThrottle]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': '请同时输入用户名和密码!'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        # 此处应注意：如果账号被禁用，也会显示用户名或密码错误!
        if not user:
            return Response({'error': '用户名或密码错误!', 'addition': "如果您确保用户名和密码无误，您的账号可能被禁用!"},
                            status=status.HTTP_401_UNAUTHORIZED)
        user.last_login = timezone.now()
        user.save()
        # 删除过期的Token
        Token.objects.filter(user=user, created__lte=timezone.now() - timedelta(hours=TOKEN_EXPIRY_HOURS)).delete()
        # 获取或创建Token
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'detail': "登录成功！", 'token': token.key},
                        status=HTTP_200_OK)


class UserLogoutView(APIView):
    """
    退出登录
    """
    throttle_scope = "post"
    throttle_classes = [ScopedRateThrottle, ]

    def get(self, request):
        user = request.user
        Token.objects.filter(user=user).delete()
        if request.session.get('user_id', None) is not None:
            del request.session['user_id']
        if request.session.get('type', None) is not None:
            del request.session['type']
        if request.session.get('rating', None) is not None:
            del request.session['rating']
        return Response({'detail': '成功退出！'}, status=HTTP_200_OK)


class UserListView(ListModelMixin, GenericAPIView):
    """
    查看用户列表
    """
    queryset = UserProfile.objects.all()
    permission_classes = [IsAdminUser]  # 只有管理员才可查看用户列表
    serializer_class = UserMessageSerializer

    def get(self, request):
        return self.list(request)


class UserDetailView(RetrieveModelMixin, GenericAPIView):
    """
    某个用户查看自己的信息
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserMessageSerializer

    def get(self, request, pk):
        return self.retrieve(request, pk)


class UserChangePasswordView(UpdateModelMixin, GenericAPIView):
    """
    用户自己修改密码
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserPasswordSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        # 更新用户密码
        new_password = serializer.validated_data.get('password')
        instance.set_password(new_password)
        instance.save()

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response({'detail': "修改成功!"})

    def put(self, request, pk):
        return self.update(request, pk)


class UserCreateView(GenericAPIView):
    """
    创建一个用户
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]  # 只有管理员才有权限创建用户
    throttle_scope = "post"
    throttle_classes = [ScopedRateThrottle, ]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Please provide both username and password.'}, status=status.HTTP_400_BAD_REQUEST)

        if UserProfile.objects.filter(username__exact=username):
            return Response({"error": "The username already exists!"}, status=HTTP_400_BAD_REQUEST)

        data = request.data.copy()
        name = data['name']
        mobile = data['mobile']
        email = data['email']
        gender = data['gender']
        serializer = self.get_serializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = UserProfile.objects.create_user(username=username, password=password, name=name,
                                                   mobile=mobile, email=email, gender=gender)
            token = Token.objects.create(user=user)
            return Response({'message': "创建成功！", 'token': token.key},
                            status=HTTP_201_CREATED)

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class UserUpdateView(UpdateModelMixin, GenericAPIView):
    """
    修改一个用户的信息(目前所有人均可修改)
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserUpdateSerializer

    def put(self, request, pk):
        return self.update(request, pk)


class UserDeleteView(DestroyModelMixin, GenericAPIView):
    """
    删除一个用户
    """
    queryset = UserProfile.objects.all()
    permission_classes = [IsAdminUser]  # 只有管理员才能删除用户
    serializer_class = UserSerializer

    def delete(self, request, pk):
        return self.destroy(request, pk)


class UserActivationView(ViewSet):
    """
    单个或批量启用用户
    """
    permission_classes = [IsAdminUser]  # 只有管理员才能启用用户

    @action(methods=['patch'], detail=False)
    def batch_activate(self, request):
        user_ids = request.data.get('user_ids', [])
        is_active = request.data.get('is_active', False)

        # 更新选中用户的激活状态
        UserProfile.objects.filter(id__in=user_ids).update(is_active=is_active)

        # 获取更新后的用户列表
        return Response({'detail': '批量更新成功'}, status=HTTP_200_OK)


class UserDeactivateView(ViewSet):
    """
    单个或批量禁用用户
    """
    permission_classes = [IsAdminUser]  # 只有管理员才能禁用用户

    @action(methods=['patch'], detail=False)
    def batch_deactivate(self, request):
        user_ids = request.data.get('user_ids', [])
        is_active = request.data.get('is_active', False)
        # 更新选中用户的激活状态
        UserProfile.objects.filter(id__in=user_ids).update(is_active=is_active)

        # 获取更新后的用户列表
        return Response({'detail': '批量更新成功'}, status=HTTP_200_OK)


class AdminPasswdChangeView(UpdateModelMixin, GenericAPIView):
    """
    管理员修改用户的密码
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserPasswordSerializer
    permission_classes = [IsAdminUser]  # 只有管理员才能修改密码

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        # 更新用户密码
        new_password = serializer.validated_data.get('password')
        instance.set_password(new_password)
        instance.save()

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response({'detail': "修改成功!"})

    def put(self, request, pk):
        return self.update(request, pk)
