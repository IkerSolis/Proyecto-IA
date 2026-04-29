from rest_framework import serializers

class OnboardingSerializer(serializers.Serializer):
    nombre = serializers.CharField(max_length=100)
    giro = serializers.CharField(max_length=100, required=False, allow_blank=True)
    descripcion = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(max_length=150)
    password = serializers.CharField(write_only=True, min_length=6)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
