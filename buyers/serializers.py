from rest_framework import serializers
from accounts.models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    confirm_password=serializers.CharField(write_only=True)
    class Meta:
        model=CustomUser
        fields=['id','email','password','confirm_password','first_name','last_name','contact','address','user_type','city']

    def validate(self,data):
        if data['password']!=data['confirm_password']:
            raise serializers.ValidationError('Password does not Match')
        return data
    
    def create(self,validate_data):
        validate_data.pop('confirm_password',None)

        return CustomUser.objects.create_user(**validate_data)
    
    
class LoginSerializer(serializers.Serializer):
    email=serializers.EmailField()
    password=serializers.CharField()