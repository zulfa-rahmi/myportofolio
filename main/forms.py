from django.forms import (
    ModelForm,
    TextInput,
    Textarea,
    DateInput,
    CheckboxInput,
    NumberInput,
    URLInput,
)
from main.models import Project, Experience


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


class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = [
            "title",
            "organization",
            "category",
            "description",
            "started_at",
            "ended_at",
            "is_current",
        ]

        labels = {
            "title": "Posisi / Peran",
            "organization": "Organisasi / Perusahaan",
            "category": "Kategori",
            "description": "Deskripsi Pengalaman",
            "started_at": "Tanggal Mulai",
            "ended_at": "Tanggal Selesai",
            "is_current": "Masih Berlangsung",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Software Engineering Teaching Assistant",
                    "maxlength": 255,
                }
            ),
            "organization": TextInput(
                attrs={
                    "placeholder": "Fakultas Ilmu Komputer UI",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan peran dan kontribusimu",
                    "rows": 3,
                }
            ),
            "started_at": DateInput(
                attrs={
                    "type": "date",
                }
            ),
            "ended_at": DateInput(
                attrs={
                    "type": "date",
                }
            ),
            "is_current": CheckboxInput(),
        }