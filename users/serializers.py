from users.models import UserModel, UserConfirmationModel, VIA_PHONE, VIA_EMAIL, CODE_VERIFIED, NEW, DONE, PHOTO_STEP
from rest_framework import exceptions
from django.db.models import Q
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from shared_app.utility import check_email_or_phone, send_email, send_phone_code


class SignUpSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    def __init__(self, *args, **kwargs):
        super(SignUpSerializer, self).__init__(*args, **kwargs)
        self.fields['email_phone_number'] = serializers.CharField(required=False)

    class Meta:
        model = UserModel
        fields = (
            'id',
            'auth_type',
            'auth_status'
        )
        extra_kwargs = {
            'auth_type': {'read_only': True, 'required': False},
            'auth_status': {'read_only': True, 'required': False}
        }

    def create(self, validated_data):
        user = super(SignUpSerializer, self).create(validated_data)
        print(user)
        if user.auth_type == VIA_EMAIL:
            code = user.create_verify_code(VIA_EMAIL)
            print(code)
            send_email(user.email, code)
        elif user.auth_type == VIA_PHONE:
            code = user.create_verify_code(VIA_PHONE)
            print(code)
            send_email(user.phone_number, code)
            # send_phone_code(user.phone_number, code) #twilio dan subscription olganda ishlatiladi
        user.save()
        return user

    def validate(self, data):
        super(SignUpSerializer, self).validate(data)
        data = self.auth_validate(data)
        return data

    @staticmethod
    def auth_validate(data):
        user_input = str(data.get('email_phone_number')).lower()

        # check is it email or phone number
        input_type = check_email_or_phone(user_input)
        if input_type == 'email':
            data = {
                "email": data.get('email_phone_number'),
                "auth_type": VIA_EMAIL
            }
        elif input_type == 'phone':
            data = {
                "phone_number": user_input,
                "auth_type": VIA_PHONE
            }
        else:
            data = {
                "success": False,
                "meassage": "You must send email or phone number"
            }
            raise ValidationError(data)
        print("data", data)
        return data

    def validate_email_phone_number(self, value):
        value = value.lower()
        if value and UserModel.objects.filter(email=value).exists():
            data = {
                "success": False,
                "message": "This email already exists."
            }
            raise ValidationError(data)
        elif value and UserModel.objects.filter(phone_number=value).exists():
            data = {
                "success": False,
                "message": "This phone number already exists."
            }
            raise ValidationError(data)
        return value

    def to_representation(self, instance):
        print('to_rep', instance)
        data = super(SignUpSerializer, self).to_representation(instance)
        data.update(instance.token())

        return data