from django.utils.html import strip_tags
from rest_framework import serializers

from main.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id", "title", "event", "description", "year",
            "cover_image", "project_url", "created_at",
            "star_count", "is_starred", "starred_by_names",
        ]
        read_only_fields = ["id", "created_at"]

    def validate_title(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        return value

    def validate_event(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Event cannot be empty.")
        return value

    def validate_description(self, value):
        return strip_tags(value)

    def validate_cover_image(self, value):
        return strip_tags(value).strip()

    def validate_year(self, value):
        # Sama dengan batas min/max pada widget ProjectForm.
        if not 1900 <= value <= 2099:
            raise serializers.ValidationError("Year must be between 1900 and 2099.")
        return value

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return request.user in obj.starred_by.all()

    def get_starred_by_names(self, obj):
        return ", ".join(user.username for user in obj.starred_by.all())
