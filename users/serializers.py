from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    # Пароль будет доступен только для записи
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role', 'password')

    def create(self, validated_data):
        # Создаем пользователя, устанавливая хешированный пароль
        user = User(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            role=validated_data.get('role', 'user'),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user 