from rest_framework import serializers

from .models import Country, State, Tag, URL


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ["name_of_the_state", "state_code"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["name_of_the_tag",]


class URLSerializer(serializers.ModelSerializer):
    class Meta:
        model = URL
        fields = ["url", "name"]
