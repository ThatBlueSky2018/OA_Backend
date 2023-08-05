from rest_framework import serializers

from .models import UserProfile, Structure


# 包含所有字段
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


# 只有部分字段
class UserMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'name', 'gender', 'mobile', 'email', 'department', 'post', 'superior', 'is_active']


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['name', 'gender', 'birthday', 'is_active', 'mobile', 'email', 'joined_date', 'department',
                  'post', 'superior', 'role']


# 只有密码
class UserPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['password']


class StructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Structure
        fields = '__all__'
