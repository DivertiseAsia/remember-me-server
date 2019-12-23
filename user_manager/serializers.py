from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers, validators

from user_manager.models import Profile

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    birth_date = serializers.SerializerMethodField()

    @staticmethod
    def get_birth_date(obj):
        return Profile.objects.get(user=obj).birth_date

    class Meta:
        model = User
        extra_kwargs = {
            'id': {'read_only': True},
            'password': {'write_only': True},
            'last_login': {'read_only': True},
            'is_staff': {'read_only': True},
            'is_active': {'read_only': True},
        }
        fields = ('username', 'email', 'first_name', 'last_name', 'birth_date')


class RegistrationSerializer(UserSerializer):
    email = serializers.EmailField(required=True, validators=[
        validators.UniqueValidator(
            queryset=User.objects.all(),
            message='This email is already registered.')
    ])
    username = serializers.CharField(required=True, validators=[
        validators.UniqueValidator(
            queryset=User.objects.all(),
            message='The username is already being used.')
    ])
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(required=True, write_only=True)
    last_name = serializers.CharField(required=True, write_only=True)
    birth_date = serializers.DateField(required=True, write_only=True)

    def validate(self, data):
        if not data.get('password') or not data.get('confirm_password'):
            raise serializers.ValidationError('Please enter a password and confirm it.')

        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError('Passwords do not match.')

        return data

    def create(self, validated_data):
        self.validate(validated_data)
        validated_data['is_active'] = True  # TODO: Default should be false with confirmation
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        profile = Profile.objects.get(user=user)
        profile.update_profile(
            birth_date=validated_data['birth_date']
        )

        return user

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'confirm_password', 'first_name', 'last_name', 'birth_date')


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            try:
                user = User.objects.get(username__iexact=username)
            except User.DoesNotExist:
                raise serializers.ValidationError('This account is not exist.')
        else:
            raise serializers.ValidationError('Username and password are required.')

        if not user.is_active:
            raise serializers.ValidationError('This account is inactive.')

        return data

    def verify_user(self):
        return authenticate(username=self.validated_data['username'], password=self.validated_data['password'])

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class BirthdaySerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    birth_date = serializers.SerializerMethodField()

    @staticmethod
    def get_name(obj):
        return obj.first_name

    @staticmethod
    def get_birth_date(obj):
        return Profile.objects.get(user=obj).birth_date

    class Meta:
        model = User
        fields = ('name', 'birth_date')


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate(self, data):
        if not data.get('new_password') or not data.get('confirm_password'):
            raise serializers.ValidationError('Please enter new password and confirm it.')

        if data.get('new_password') != data.get('confirm_password'):
            raise serializers.ValidationError('New password and confirm password do not match.')

        return data

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
