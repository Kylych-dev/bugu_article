from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from apps.accounts.models import (
    CustomUser, 
    AuthorProfile, 
    SubscriberProfile
)


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        # validators=[validate_password]
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
    )
    role = serializers.ChoiceField(choices=[
        ('subscriber', 'Subscriber'), 
        ('author', 'Author')], 
        write_only=True
        )


    class Meta:
        model = CustomUser
        fields = [
            'id',
            'email',
            'role',
            'username',
            'password',
            'password2'
        ]
        extra_kwargs = {
            'password': {
                'write_only': True
                },
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {
                    "password": "Password fields didn't match."
                }
            )
        
        validate_password(attrs["password"])
        return attrs
    
    def create(self, validated_data):
        role = validated_data.pop('role')
        validated_data.pop('password2')

        user = CustomUser.objects.create_user(**validated_data)

        if role == 'subscriber':
            SubscriberProfile.objects.create(user=user)
        elif role == 'author':
            AuthorProfile.objects.create(user=user)
        
        return user
    

        # return super().create(validated_data)