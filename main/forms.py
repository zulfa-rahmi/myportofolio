from django.core.exceptions import ValidationError
from django.forms import (
    ModelForm,
    TextInput,
    Textarea,
    DateInput,
    CheckboxInput,
    NumberInput,
    URLInput,
)
from django.utils.html import strip_tags
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

    # ---- Sanitasi XSS di sisi server ----
    def _clean_text(self, field_name):
        """Buang tag HTML dari field teks. Kalau hasilnya kosong
        (mis. input hanya berisi <img onerror=...>), input ditolak."""
        value = strip_tags(self.cleaned_data.get(field_name, "")).strip()
        if not value:
            raise ValidationError(
                "Isian ini tidak boleh kosong atau hanya berisi tag HTML."
            )
        return value

    def clean_title(self):
        return self._clean_text("title")

    def clean_organization(self):
        return self._clean_text("organization")

    def clean_description(self):
        return self._clean_text("description")

    def clean(self):
        cleaned = super().clean()
        started_at = cleaned.get("started_at")
        ended_at = cleaned.get("ended_at")
        if started_at and ended_at and ended_at < started_at:
            self.add_error(
                "ended_at", "Tanggal selesai tidak boleh sebelum tanggal mulai."
            )
        return cleaned
