from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenGenerator

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def generate_token(self, user):
        # Generate a random token
        token_generator = TokenGenerator()
        token = token_generator.make_token(user)

        # Save the token in the database
        refresh = RefreshToken.for_user(user)
        refresh.access_token = token
        refresh.save(using=self._db)

        return token
