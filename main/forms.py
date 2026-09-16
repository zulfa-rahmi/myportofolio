from django.forms import ModelForm, TextInput, Textarea, URLInput, NumberInput

from main.models import Project

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "event",
            "description",
            "year",
            "cover_image",
            "project_url",
        ]

        labels = {
            "title": "Nama Proyek",
            "event": "Kegiatan",
            "description": "Deskripsi Proyek",
            "year": "Tahun Membuat",
            "cover_image": "URL Gambar Proyek",
            "project_url": "URL Proyek",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Portfolio Website",
                    "maxlength": 255,
                }
            ),
            "event": TextInput(
                attrs={
                    "placeholder": "Tugas Mata Kuliah PBP",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan Proyekmu",
                    "rows": 3,
                }
            ),
            "year": NumberInput(
                attrs={
                    "placeholder": "2026",
                    "min": "1900",
                    "max": "2099",
                }
            ),
            "cover_image": URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/thumbnail?id=...&sz=w1000",
                }
            ),
            "project_url": URLInput(
                attrs={
                    "placeholder": "https://github.com/kakBurhan/burhanquestv4",
                }
            ),
        }
