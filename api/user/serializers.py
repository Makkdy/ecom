from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import authentication_classes, permission_classes
from .models import CustomUser

class CustomUserSerializer(serializers.HyperlinkedModelSerializer):


    # create methode describe the methode to create user
    # this methode will be hit whenever we send "POST" request to default route
    def create(self, validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model (**validated_data)

        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    # this methode hit whenever we hit "PUT" request to default route (Not sure read docs)
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
                
        instance.save()
        return instance


    class Meta:
        model = CustomUser
        # write_only make sure that password doesn't send to fornt end only available while "POST" request not "PUT", or any else
        extra_kwargs = {'password': {'write_only': True}}
        fields = ('name','email','password','phone','gender','is_active','is_staff','is_superuser')