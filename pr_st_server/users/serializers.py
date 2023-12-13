from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name', 'consentReceiveNews', 'consentPersonalData', 'address')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            consentReceiveNews=validated_data['consentReceiveNews'],
            consentPersonalData=validated_data['consentPersonalData'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user
