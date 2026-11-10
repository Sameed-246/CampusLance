import tempfile
from datetime import date
from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from accounts.models import CustomUser
from applications.models import Application
from profiles.models import StudentProfile

from .models import Job
from .resume_scanner import analyze_resume


class ResumeScannerAnalysisTests(TestCase):
    def test_analysis_summarizes_job_skill_match(self):
        student = CustomUser.objects.create_user(
            username="analysis-student",
            password="test-password",
            role="student",
        )
        job = Job(
            title="Python developer",
            category="Python",
            description="Build Python and Django features.",
        )
        profile = StudentProfile(user=student, skills="Python, Django")

        result = analyze_resume("Python Django portfolio project", job, profile)

        self.assertIn("Python developer", result["summary"])
        self.assertCountEqual(["python", "django"], result["matched_skills"])
        self.assertEqual(100, result["fit_score"])


class ResumeScannerViewTests(TestCase):
    def setUp(self):
        self.media_directory = tempfile.TemporaryDirectory()
        self.settings_override = override_settings(
            MEDIA_ROOT=self.media_directory.name
        )
        self.settings_override.enable()
        self.addCleanup(self.settings_override.disable)
        self.addCleanup(self.media_directory.cleanup)

        self.client_user = CustomUser.objects.create_user(
            username="client",
            password="test-password",
            role="client",
        )
        self.student = CustomUser.objects.create_user(
            username="student",
            password="test-password",
            role="student",
        )
        self.job = Job.objects.create(
            client=self.client_user,
            title="Python developer",
            category="Python",
            description="Build Python applications with Django.",
            budget=500,
            deadline=date(2027, 1, 1),
        )
        self.application = Application.objects.create(
            job=self.job,
            student=self.student,
            proposal="I have Python experience.",
        )
        self.profile = StudentProfile.objects.create(
            user=self.student,
            skills="Python, Django",
        )

    def test_client_can_scan_applicant_pdf(self):
        self.profile.resume = SimpleUploadedFile(
            "resume.pdf",
            b"%PDF-1.4 test document",
            content_type="application/pdf",
        )
        self.profile.save()
        self.client.force_login(self.client_user)

        with patch(
            "jobs.views.extract_resume_text",
            return_value="Python Django experience",
        ):
            response = self.client.post(
                reverse(
                    "scan_applicant_resume",
                    args=[self.application.id],
                )
            )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Scan summary")
        self.assertContains(response, "Python developer")
        self.assertContains(response, "Matched skills")

    def test_other_client_cannot_scan_applicant_resume(self):
        other_client = CustomUser.objects.create_user(
            username="other-client",
            password="test-password",
            role="client",
        )
        self.client.force_login(other_client)

        response = self.client.post(
            reverse(
                "scan_applicant_resume",
                args=[self.application.id],
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_scan_reports_when_student_has_no_resume(self):
        self.client.force_login(self.client_user)

        response = self.client.post(
            reverse(
                "scan_applicant_resume",
                args=[self.application.id],
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "No resume has been uploaded to this student's profile yet.",
        )
        self.assertContains(response, "This student has not uploaded a resume.")

    def test_scanner_does_not_use_account_resume_instead_of_profile_resume(self):
        self.student.resume = SimpleUploadedFile(
            "account-resume.pdf",
            b"%PDF-1.4 account resume",
            content_type="application/pdf",
        )
        self.student.save()
        self.client.force_login(self.client_user)

        response = self.client.post(
            reverse(
                "scan_applicant_resume",
                args=[self.application.id],
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This student has not uploaded a resume.")
