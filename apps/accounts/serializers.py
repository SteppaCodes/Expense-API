from rest_framework import serializers

from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=30, write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']
    
    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': 'Email already exists'})
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


        
