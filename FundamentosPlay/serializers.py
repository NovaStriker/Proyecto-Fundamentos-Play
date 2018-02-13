from rest_framework import serializers

from .models import FichaCompletacion


class UserSerializer(serializers.ModelSerializer):

    class Meta:

        model = FichaCompletacion

        fields = '__all__'
