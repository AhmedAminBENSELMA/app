from rest_framework import serializers
from .models.annex6a import Annex6a
from .models.annex import Annex


class Annex6aSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annex6a
        fields = '__all__'
        


class AnnexSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annex
        fields = '__all__'
        