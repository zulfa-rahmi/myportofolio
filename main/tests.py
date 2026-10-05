import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from main.forms import ExperienceForm, ProjectForm
from main.models import Experience, Project


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_experience(**overrides):
    data = {
        "title": "Asisten Dosen PBP",
        "organization": "Fasilkom UI",
        "description": "Membantu mahasiswa memahami pengembangan web.",
        "category": "part-time",
        "started_at": datetime.date(2025, 1, 1),
    }
    data.update(overrides)
    return Experience.objects.create(**data)


def make_project(**overrides):
    data = {
        "title": "TwinStore AI",
        "event": "Bizclash 3.0 2026",
        "description": "An AI-powered application that simulates retail stores.",
        "year": 2026,
    }
    data.update(overrides)
    return Project.objects.create(**data)


class UserMixin:
    """Membuat user biasa dan superuser untuk test yang butuh login."""

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user("biasa", password="StrongPass123!")
        cls.admin = User.objects.create_superuser(
            "admin", "admin@example.com", "StrongPass123!"
        )


# ---------------------------------------------------------------------------
# Halaman utama
# ---------------------------------------------------------------------------

class MainPageTest(TestCase):
    def test_main_page_uses_correct_template(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")

    def test_main_page_shows_profile_data(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertContains(response, "Zulfa Rahmi Nasution")
        self.assertContains(response, "S1 Sistem Informasi")
        self.assertContains(response, "SMA Labschool Kebayoran")
        self.assertContains(response, "Tech Innovation")

    def test_main_page_has_social_links(self):
        response = self.client.get(reverse("main:show_main"))

        for link in response.context["socials"].values():
            self.assertContains(response, f'href="{link}"')

    def test_main_page_has_navigation_links(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertContains(response, f'href="{reverse("main:show_experience")}"')
        self.assertContains(response, f'href="{reverse("main:show_projects")}"')

    def test_main_page_does_not_list_experience_or_project_data(self):
        make_experience(title="Judul Pengalaman Unik")
        make_project(title="Judul Proyek Unik")
        response = self.client.get(reverse("main:show_main"))

        self.assertNotContains(response, "Judul Pengalaman Unik")
        self.assertNotContains(response, "Judul Proyek Unik")

    def test_last_login_default_when_cookie_missing(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertContains(response, "Belum ada sesi login")

    def test_last_login_read_from_cookie(self):
        self.client.cookies["last_login"] = "2026-09-28 08:00:00"
        response = self.client.get(reverse("main:show_main"))

        self.assertContains(response, "2026-09-28 08:00:00")

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)


# ---------------------------------------------------------------------------
# Experience
# ---------------------------------------------------------------------------

class ExperienceModelTest(TestCase):
    def test_str_returns_title(self):
        self.assertEqual(str(make_experience()), "Asisten Dosen PBP")

    def test_default_category_is_full_time(self):
        experience = make_experience(category=Experience._meta.get_field("category").default)

        self.assertEqual(experience.category, "full-time")

    def test_is_ongoing_depends_on_ended_at(self):
        ongoing = make_experience()
        finished = make_experience(ended_at=datetime.date(2025, 6, 1))

        self.assertTrue(ongoing.is_ongoing)
        self.assertFalse(finished.is_ongoing)


class ExperiencePageTest(UserMixin, TestCase):
    """Halaman hanya berisi kerangka; data dimuat lewat fetch() ke endpoint JSON."""

    def setUp(self):
        self.experience = make_experience(is_current=True)

    def test_page_uses_correct_template(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")

    def test_page_is_skeleton_without_server_rendered_data(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, reverse("main:get_experience_json"))
        self.assertContains(response, 'id="loading"')
        self.assertContains(response, 'id="error"')
        self.assertContains(response, 'id="empty"')

    def test_add_modal_hidden_for_anonymous_visitor(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertNotContains(response, "add-experience-modal")
        self.assertContains(response, "canManage: false")

    def test_add_modal_hidden_for_regular_user(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("main:show_experience"))

        self.assertNotContains(response, "add-experience-modal")

    def test_add_modal_shown_for_superuser(self):
        self.client.force_login(self.admin)
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "add-experience-modal")
        self.assertContains(response, "canManage: true")


class ExperienceJsonTest(UserMixin, TestCase):
    def setUp(self):
        self.experience = make_experience(is_current=True)
        self.url = reverse("main:get_experience_json")

    def test_returns_json_list_for_anonymous_visitor(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        data = response.json()
        self.assertEqual(len(data), 1)
        fields = data[0]["fields"]
        self.assertEqual(data[0]["pk"], str(self.experience.id))
        self.assertEqual(fields["title"], "Asisten Dosen PBP")
        self.assertEqual(fields["category_display"], "Part-Time")
        self.assertEqual(fields["started_label"], "Jan 2025")
        self.assertTrue(fields["is_current"])

    def test_includes_star_info(self):
        self.experience.starred_by.add(self.user)
        self.client.force_login(self.user)
        fields = self.client.get(self.url).json()[0]["fields"]

        self.assertEqual(fields["star_count"], 1)
        self.assertTrue(fields["is_starred"])
        self.assertEqual(fields["starred_by_names"], ["biasa"])

    def test_is_starred_false_for_anonymous_and_other_users(self):
        self.experience.starred_by.add(self.user)

        self.assertFalse(self.client.get(self.url).json()[0]["fields"]["is_starred"])
        self.client.force_login(self.admin)
        fields = self.client.get(self.url).json()[0]["fields"]
        self.assertFalse(fields["is_starred"])
        self.assertEqual(fields["star_count"], 1)

    def test_finished_experience_has_end_label(self):
        self.experience.is_current = False
        self.experience.ended_at = datetime.date(2025, 6, 1)
        self.experience.save()
        fields = self.client.get(self.url).json()[0]["fields"]

        self.assertEqual(fields["ended_label"], "Jun 2025")
        self.assertFalse(fields["is_current"])

    def test_empty_list(self):
        Experience.objects.all().delete()

        self.assertEqual(self.client.get(self.url).json(), [])

    def test_ordered_by_latest_start_date(self):
        make_experience(title="Lebih Lama", started_at=datetime.date(2023, 1, 1))
        make_experience(title="Paling Baru", started_at=datetime.date(2026, 1, 1))
        titles = [i["fields"]["title"] for i in self.client.get(self.url).json()]

        self.assertEqual(titles, ["Paling Baru", "Asisten Dosen PBP", "Lebih Lama"])

    def test_search_by_title(self):
        make_experience(title="Business Development Staff", organization="OH")

        self.assertEqual(self.client.get(self.url, {"q": "bisnis"}).json(), [])
        data = self.client.get(self.url, {"q": "business"}).json()
        self.assertEqual([i["fields"]["title"] for i in data], ["Business Development Staff"])

    def test_search_by_organization(self):
        make_experience(title="Staff", organization="COMPFEST")
        data = self.client.get(self.url, {"q": "compfest"}).json()

        self.assertEqual([i["fields"]["title"] for i in data], ["Staff"])


class ExperienceCreateAjaxTest(UserMixin, TestCase):
    def setUp(self):
        self.url = reverse("main:create_experience_ajax")
        self.payload = {
            "title": "Staff Bisdev",
            "organization": "OH Fasilkom",
            "category": "organization",
            "description": "Mengelola sponsorship.",
            "started_at": "2025-03-01",
        }

    def test_get_not_allowed(self):
        self.client.force_login(self.admin)

        self.assertEqual(self.client.get(self.url).status_code, 405)

    def test_anonymous_gets_403_json(self):
        response = self.client.post(self.url, self.payload)

        self.assertEqual(response.status_code, 403)
        self.assertIn("message", response.json())
        self.assertEqual(Experience.objects.count(), 0)

    def test_regular_user_gets_403(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url, self.payload)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(Experience.objects.count(), 0)

    def test_superuser_creates_201(self):
        self.client.force_login(self.admin)
        response = self.client.post(self.url, self.payload)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["data"]["fields"]["title"], "Staff Bisdev")
        self.assertTrue(Experience.objects.filter(title="Staff Bisdev").exists())

    def test_editor_group_member_creates_201(self):
        from django.contrib.auth.models import Group

        self.user.groups.add(Group.objects.create(name="Editor"))
        self.client.force_login(self.user)

        self.assertEqual(self.client.post(self.url, self.payload).status_code, 201)

    def test_invalid_data_gets_400_with_errors(self):
        self.client.force_login(self.admin)
        self.payload["title"] = ""
        response = self.client.post(self.url, self.payload)

        self.assertEqual(response.status_code, 400)
        self.assertIn("title", response.json()["errors"])
        self.assertEqual(Experience.objects.count(), 0)

    def test_end_date_before_start_date_rejected(self):
        self.client.force_login(self.admin)
        self.payload["ended_at"] = "2024-01-01"
        response = self.client.post(self.url, self.payload)

        self.assertEqual(response.status_code, 400)
        self.assertIn("ended_at", response.json()["errors"])

    def test_html_tags_are_stripped(self):
        self.client.force_login(self.admin)
        self.payload["title"] = "<b>Staff</b> Bisdev"
        self.client.post(self.url, self.payload)

        self.assertEqual(Experience.objects.get().title, "Staff Bisdev")

    def test_xss_only_payload_is_rejected(self):
        self.client.force_login(self.admin)
        self.payload["description"] = "<img src=\"x\" onerror=\"alert('XSS!')\">"
        response = self.client.post(self.url, self.payload)

        self.assertEqual(response.status_code, 400)
        self.assertIn("description", response.json()["errors"])
        self.assertEqual(Experience.objects.count(), 0)

    def test_csrf_is_enforced(self):
        from django.test import Client

        client = Client(enforce_csrf_checks=True)
        client.force_login(self.admin)

        self.assertEqual(client.post(self.url, self.payload).status_code, 403)
        self.assertEqual(Experience.objects.count(), 0)


class ExperienceStarAjaxTest(UserMixin, TestCase):
    def setUp(self):
        self.experience = make_experience()
        self.url = reverse("main:toggle_star_experience", args=[self.experience.id])

    def test_anonymous_gets_403(self):
        self.assertEqual(self.client.post(self.url).status_code, 403)
        self.assertEqual(self.experience.starred_by.count(), 0)

    def test_get_not_allowed(self):
        self.client.force_login(self.user)

        self.assertEqual(self.client.get(self.url).status_code, 405)

    def test_toggle_on_and_off(self):
        self.client.force_login(self.user)
        on = self.client.post(self.url).json()["fields"]
        self.assertTrue(on["is_starred"])
        self.assertEqual(on["star_count"], 1)

        off = self.client.post(self.url).json()["fields"]
        self.assertFalse(off["is_starred"])
        self.assertEqual(off["star_count"], 0)

    def test_unknown_id_returns_404(self):
        self.client.force_login(self.user)
        url = reverse(
            "main:toggle_star_experience", args=["00000000-0000-0000-0000-000000000000"]
        )

        self.assertEqual(self.client.post(url).status_code, 404)


class ExperienceCrudTest(UserMixin, TestCase):
    def setUp(self):
        self.experience = make_experience()
        self.payload = {
            "title": "Staff Bisdev",
            "organization": "OH Fasilkom",
            "category": "organization",
            "description": "Mengelola sponsorship.",
            "started_at": "2025-03-01",
        }

    def test_create_requires_login(self):
        response = self.client.get(reverse("main:create_experience"))

        self.assertRedirects(
            response,
            f'/login/?next={reverse("main:create_experience")}',
        )

    def test_create_forbidden_for_non_superuser(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("main:create_experience"), self.payload)

        self.assertEqual(response.status_code, 403)
        self.assertFalse(Experience.objects.filter(title="Staff Bisdev").exists())

    def test_create_form_shown_to_superuser(self):
        self.client.force_login(self.admin)
        response = self.client.get(reverse("main:create_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience_form.html")

    def test_superuser_can_create(self):
        self.client.force_login(self.admin)
        response = self.client.post(reverse("main:create_experience"), self.payload)

        self.assertRedirects(response, reverse("main:show_experience"))
        self.assertTrue(Experience.objects.filter(title="Staff Bisdev").exists())

    def test_create_with_invalid_data_shows_form_again(self):
        self.client.force_login(self.admin)
        self.payload["title"] = ""
        response = self.client.post(reverse("main:create_experience"), self.payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Experience.objects.count(), 1)

    def test_superuser_can_update(self):
        self.client.force_login(self.admin)
        url = reverse("main:update_experience", args=[self.experience.id])
        response = self.client.post(url, self.payload)

        self.assertRedirects(response, reverse("main:show_experience"))
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Staff Bisdev")

    def test_update_unknown_id_returns_404(self):
        self.client.force_login(self.admin)
        url = reverse(
            "main:update_experience", args=["00000000-0000-0000-0000-000000000000"]
        )

        self.assertEqual(self.client.get(url).status_code, 404)

    def test_delete_forbidden_for_non_superuser(self):
        self.client.force_login(self.user)
        url = reverse("main:delete_experience", args=[self.experience.id])

        self.assertEqual(self.client.post(url).status_code, 403)
        self.assertTrue(Experience.objects.filter(pk=self.experience.pk).exists())

    def test_delete_via_get_does_not_delete(self):
        self.client.force_login(self.admin)
        url = reverse("main:delete_experience", args=[self.experience.id])
        response = self.client.get(url)

        self.assertRedirects(response, reverse("main:show_experience"))
        self.assertTrue(Experience.objects.filter(pk=self.experience.pk).exists())

    def test_superuser_can_delete_via_post(self):
        self.client.force_login(self.admin)
        url = reverse("main:delete_experience", args=[self.experience.id])
        response = self.client.post(url)

        self.assertRedirects(response, reverse("main:show_experience"))
        self.assertFalse(Experience.objects.filter(pk=self.experience.pk).exists())


# ---------------------------------------------------------------------------
# Projects
# ---------------------------------------------------------------------------

class ProjectModelTest(UserMixin, TestCase):
    def test_str_returns_title(self):
        self.assertEqual(str(make_project()), "TwinStore AI")

    def test_default_ordering_is_newest_year_then_title(self):
        make_project(title="B", year=2025)
        make_project(title="A", year=2025)
        make_project(title="Z", year=2026)

        self.assertEqual(
            [p.title for p in Project.objects.all()], ["Z", "A", "B"]
        )

    def test_starred_by_is_many_to_many(self):
        project = make_project()
        project.starred_by.add(self.user, self.admin)

        self.assertEqual(project.starred_by.count(), 2)
        self.assertIn(project, self.user.starred_projects.all())


class ProjectPageTest(UserMixin, TestCase):
    def setUp(self):
        self.project = make_project(project_url="https://example.com/twinstore")

    def test_page_uses_correct_template(self):
        response = self.client.get(reverse("main:show_projects"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects.html")

    def test_page_shows_project_data(self):
        response = self.client.get(reverse("main:show_projects"))

        self.assertContains(response, self.project.title)
        self.assertContains(response, self.project.event)
        self.assertContains(response, self.project.description)
        self.assertContains(response, 'href="https://example.com/twinstore"')

    def test_link_button_hidden_when_no_project_url(self):
        Project.objects.all().delete()
        make_project(title="Tanpa Link")
        response = self.client.get(reverse("main:show_projects"))

        self.assertNotContains(response, "Lihat Project")

    def test_empty_state_when_no_data(self):
        Project.objects.all().delete()
        response = self.client.get(reverse("main:show_projects"))

        self.assertContains(response, "Belum ada proyek yang ditambahkan.")

    def test_search_by_title_is_case_insensitive(self):
        make_project(title="Ecobyte")
        response = self.client.get(reverse("main:show_projects"), {"title": "twinSTORE"})

        self.assertContains(response, "TwinStore AI")
        self.assertNotContains(response, "Ecobyte")

    def test_search_without_result_shows_specific_empty_state(self):
        response = self.client.get(reverse("main:show_projects"), {"title": "xyz"})

        self.assertContains(response, "Tidak ada proyek dengan nama tersebut.")
        self.assertNotContains(response, "Belum ada proyek yang ditambahkan.")

    def test_cover_image_url_is_used_as_is(self):
        self.project.cover_image = "https://example.com/cover.png"
        self.project.save()
        response = self.client.get(reverse("main:show_projects"))

        self.assertContains(response, 'src="https://example.com/cover.png"')

    def test_cover_image_filename_resolves_to_static_folder(self):
        self.project.cover_image = "tanam.jpg"
        self.project.save()
        response = self.client.get(reverse("main:show_projects"))

        self.assertContains(response, "/static/img/projects/tanam.jpg")

    def test_add_and_delete_buttons_only_for_superuser(self):
        response = self.client.get(reverse("main:show_projects"))
        self.assertNotContains(response, reverse("main:create_project"))

        self.client.force_login(self.user)
        response = self.client.get(reverse("main:show_projects"))
        self.assertNotContains(response, reverse("main:create_project"))

        self.client.force_login(self.admin)
        response = self.client.get(reverse("main:show_projects"))
        self.assertContains(response, reverse("main:create_project"))


class ProjectJsonTest(TestCase):
    def test_returns_json_list(self):
        make_project()
        response = self.client.get(reverse("main:get_projects_json"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["model"], "main.project")
        self.assertEqual(data[0]["fields"]["title"], "TwinStore AI")

    def test_filters_by_title(self):
        make_project(title="Ecobyte")
        make_project(title="Tanam")
        response = self.client.get(reverse("main:get_projects_json"), {"title": "eco"})

        titles = [item["fields"]["title"] for item in response.json()]
        self.assertEqual(titles, ["Ecobyte"])


class ProjectCrudTest(UserMixin, TestCase):
    def setUp(self):
        self.project = make_project()
        self.payload = {
            "title": "Portfolio Website",
            "event": "Tugas Mata Kuliah PBP",
            "description": "Website portofolio pribadi.",
            "year": 2026,
            "cover_image": "",
            "project_url": "",
        }

    def test_create_requires_login(self):
        response = self.client.get(reverse("main:create_project"))

        self.assertRedirects(
            response, f'/login/?next={reverse("main:create_project")}'
        )

    def test_create_forbidden_for_non_superuser(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("main:create_project"), self.payload)

        self.assertEqual(response.status_code, 403)
        self.assertFalse(Project.objects.filter(title="Portfolio Website").exists())

    def test_create_form_shown_to_superuser(self):
        self.client.force_login(self.admin)
        response = self.client.get(reverse("main:create_project"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects_form.html")

    def test_superuser_can_create(self):
        self.client.force_login(self.admin)
        response = self.client.post(reverse("main:create_project"), self.payload)

        self.assertRedirects(response, reverse("main:show_projects"))
        self.assertTrue(Project.objects.filter(title="Portfolio Website").exists())

    def test_create_with_invalid_data_shows_form_again(self):
        self.client.force_login(self.admin)
        self.payload["year"] = ""
        response = self.client.post(reverse("main:create_project"), self.payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Project.objects.count(), 1)

    def test_superuser_can_update(self):
        self.client.force_login(self.admin)
        url = reverse("main:update_project", args=[self.project.id])
        response = self.client.post(url, self.payload)

        self.assertRedirects(response, reverse("main:show_projects"))
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, "Portfolio Website")

    def test_update_unknown_id_returns_404(self):
        self.client.force_login(self.admin)
        url = reverse(
            "main:update_project", args=["00000000-0000-0000-0000-000000000000"]
        )

        self.assertEqual(self.client.get(url).status_code, 404)

    def test_delete_requires_login(self):
        url = reverse("main:delete_project", args=[self.project.id])
        response = self.client.post(url)

        self.assertRedirects(response, f"/login/?next={url}")
        self.assertTrue(Project.objects.filter(pk=self.project.pk).exists())

    def test_delete_forbidden_for_non_superuser(self):
        self.client.force_login(self.user)
        url = reverse("main:delete_project", args=[self.project.id])

        self.assertEqual(self.client.post(url).status_code, 403)
        self.assertTrue(Project.objects.filter(pk=self.project.pk).exists())

    def test_delete_via_get_does_not_delete(self):
        self.client.force_login(self.admin)
        url = reverse("main:delete_project", args=[self.project.id])
        response = self.client.get(url)

        self.assertRedirects(response, reverse("main:show_projects"))
        self.assertTrue(Project.objects.filter(pk=self.project.pk).exists())

    def test_superuser_can_delete_via_post(self):
        self.client.force_login(self.admin)
        url = reverse("main:delete_project", args=[self.project.id])
        response = self.client.post(url)

        self.assertRedirects(response, reverse("main:show_projects"))
        self.assertFalse(Project.objects.filter(pk=self.project.pk).exists())


class ToggleStarTest(UserMixin, TestCase):
    def setUp(self):
        self.project = make_project()
        self.url = reverse("main:toggle_star", args=[self.project.id])

    def test_requires_login(self):
        response = self.client.post(self.url)

        self.assertRedirects(response, f"/login/?next={self.url}")
        self.assertEqual(self.project.starred_by.count(), 0)

    def test_post_stars_then_unstars(self):
        self.client.force_login(self.user)

        response = self.client.post(self.url)
        self.assertRedirects(response, reverse("main:show_projects"))
        self.assertIn(self.user, self.project.starred_by.all())

        self.client.post(self.url)
        self.assertNotIn(self.user, self.project.starred_by.all())

    def test_get_does_not_change_star(self):
        self.client.force_login(self.user)
        self.client.get(self.url)

        self.assertEqual(self.project.starred_by.count(), 0)

    def test_stars_from_different_users_are_independent(self):
        self.client.force_login(self.user)
        self.client.post(self.url)
        self.client.force_login(self.admin)
        self.client.post(self.url)

        self.assertEqual(self.project.starred_by.count(), 2)

    def test_unknown_project_returns_404(self):
        self.client.force_login(self.user)
        url = reverse(
            "main:toggle_star", args=["00000000-0000-0000-0000-000000000000"]
        )

        self.assertEqual(self.client.post(url).status_code, 404)

    def test_star_state_shown_on_projects_page(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("main:show_projects"))
        self.assertContains(response, "Jadilah yang pertama memberi star")

        self.client.post(self.url)
        response = self.client.get(reverse("main:show_projects"))
        self.assertContains(response, "Unstar")
        self.assertContains(response, "is-starred")
        self.assertContains(response, "Dibintangi oleh biasa")


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------

class AuthTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("rahmi", password="StrongPass123!")

    def test_register_page_renders(self):
        response = self.client.get(reverse("main:register"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "register.html")

    def test_register_creates_user_and_redirects_to_login(self):
        response = self.client.post(
            reverse("main:register"),
            {
                "username": "baru",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            },
        )

        self.assertRedirects(response, reverse("main:login"))
        self.assertTrue(User.objects.filter(username="baru").exists())

    def test_register_with_mismatched_passwords_fails(self):
        response = self.client.post(
            reverse("main:register"),
            {
                "username": "baru",
                "password1": "StrongPass123!",
                "password2": "BedaPassword123!",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="baru").exists())

    def test_login_page_renders(self):
        response = self.client.get(reverse("main:login"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")

    def test_login_success_redirects_and_sets_cookie(self):
        response = self.client.post(
            reverse("main:login"),
            {"username": "rahmi", "password": "StrongPass123!"},
        )

        self.assertRedirects(response, reverse("main:show_main"))
        self.assertIn("last_login", response.cookies)
        self.assertIn("_auth_user_id", self.client.session)

    def test_login_with_wrong_password_fails(self):
        response = self.client.post(
            reverse("main:login"),
            {"username": "rahmi", "password": "salah"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotIn("_auth_user_id", self.client.session)
        self.assertNotIn("last_login", response.cookies)

    def test_logout_clears_session_and_cookie(self):
        self.client.post(
            reverse("main:login"),
            {"username": "rahmi", "password": "StrongPass123!"},
        )
        response = self.client.get(reverse("main:logout"))

        self.assertRedirects(response, reverse("main:show_main"))
        self.assertNotIn("_auth_user_id", self.client.session)
        self.assertEqual(response.cookies["last_login"].value, "")

    def test_navbar_changes_with_login_state(self):
        response = self.client.get(reverse("main:show_main"))
        self.assertContains(response, reverse("main:login"))
        self.assertContains(response, reverse("main:register"))
        self.assertNotContains(response, reverse("main:logout"))

        self.client.force_login(self.user)
        response = self.client.get(reverse("main:show_main"))
        self.assertContains(response, reverse("main:logout"))
        self.assertContains(response, "rahmi")
        self.assertNotContains(response, reverse("main:register"))


# ---------------------------------------------------------------------------
# Forms
# ---------------------------------------------------------------------------

class FormTest(TestCase):
    def test_project_form_valid(self):
        form = ProjectForm(
            data={
                "title": "Tanam",
                "event": "Hackathon",
                "description": "Aplikasi pertanian.",
                "year": 2026,
            }
        )

        self.assertTrue(form.is_valid(), form.errors)

    def test_project_form_requires_title_event_description_and_year(self):
        form = ProjectForm(data={})

        self.assertFalse(form.is_valid())
        for field in ("title", "event", "description", "year"):
            self.assertIn(field, form.errors)

    def test_project_form_rejects_invalid_url(self):
        form = ProjectForm(
            data={
                "title": "Tanam",
                "event": "Hackathon",
                "description": "Aplikasi pertanian.",
                "year": 2026,
                "project_url": "bukan-url",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("project_url", form.errors)

    def test_experience_form_valid_without_end_date(self):
        form = ExperienceForm(
            data={
                "title": "Staff",
                "organization": "BEM",
                "category": "organization",
                "description": "Deskripsi.",
                "started_at": "2025-01-01",
                "is_current": True,
            }
        )

        self.assertTrue(form.is_valid(), form.errors)

    def test_experience_form_requires_core_fields(self):
        form = ExperienceForm(data={})

        self.assertFalse(form.is_valid())
        for field in ("title", "organization", "description", "started_at"):
            self.assertIn(field, form.errors)

    def test_experience_form_rejects_unknown_category(self):
        form = ExperienceForm(
            data={
                "title": "Staff",
                "organization": "BEM",
                "category": "tidak-ada",
                "description": "Deskripsi.",
                "started_at": "2025-01-01",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("category", form.errors)