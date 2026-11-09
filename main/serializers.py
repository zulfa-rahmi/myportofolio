from django.utils.html import strip_tags
from rest_framework import serializers

from main.models import Project, Experience
from django.utils import dateformat

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

class ExperienceSerializer(serializers.ModelSerializer):
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()
    category_display = serializers.CharField(
        source="get_category_display",
        read_only=True
    )
    started_label = serializers.SerializerMethodField()
    ended_label = serializers.SerializerMethodField()

    class Meta:
        model = Experience
        fields = [
            "id",
            "title",
            "organization",
            "description",
            "category",
            "category_display",
            "thumbnail",
            "started_at",
            "ended_at",
            "is_current",
            "started_label",
            "ended_label",
            "star_count",
            "is_starred",
            "starred_by_names",
        ]
        read_only_fields = [
            "id",
            "category_display",
            "started_label",
            "ended_label",
            "star_count",
            "is_starred",
            "starred_by_names",
        ]

    def validate_title(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError(
                "Title cannot be empty."
            )
        return value

    def validate_organization(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError(
                "Organization cannot be empty."
            )
        return value

    def validate_description(self, value):
        value = strip_tags(value).strip()

        if not value:
            raise serializers.ValidationError(
                "Description cannot be empty."
            )

        return value

    def validate(self, attrs):
        attrs = super().validate(attrs)

        started_at = attrs.get(
            "started_at",
            getattr(self.instance, "started_at", None)
        )
        ended_at = attrs.get(
            "ended_at",
            getattr(self.instance, "ended_at", None)
        )
        is_current = attrs.get(
            "is_current",
            getattr(self.instance, "is_current", False)
        )

        if started_at and ended_at and ended_at < started_at:
            raise serializers.ValidationError({
                "ended_at": "End date cannot be before start date."
            })

        if is_current and ended_at:
            raise serializers.ValidationError({
                "ended_at": "Ongoing experience cannot have an end date."
            })

        return attrs

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")

        if request is None or not request.user.is_authenticated:
            return False

        return obj.starred_by.filter(
            pk=request.user.pk
        ).exists()

    def get_starred_by_names(self, obj):
        return list(
            obj.starred_by.values_list("username", flat=True)
        )

    def get_started_label(self, obj):
        if obj.started_at is None:
            return None

        return dateformat.format(obj.started_at, "M Y")


    def get_ended_label(self, obj):
        if obj.ended_at is None:
            return None

        return dateformat.format(obj.ended_at, "M Y")

    def to_representation(self, instance):
        data = super().to_representation(instance)

        # Mempertahankan format data yang saat ini digunakan
        # oleh experience.js agar perubahan frontend minimal.
        return {
            "pk": str(instance.pk),
            "fields": {
                key: value
                for key, value in data.items()
                if key != "id"
            }
        }