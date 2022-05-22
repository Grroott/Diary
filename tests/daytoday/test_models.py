from django.test import TestCase
from django.contrib.auth.models import User
from daytoday.models import Daily, Feedback
from .model_config import MODEL_USER, MODEL_DIARY, MODEL_FEEDBACK


class UserTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.user = User.objects.create_user(**MODEL_USER["User"])
        return super().setUpClass()

    def test_user_instance(self):
        self.assertIsInstance(self.user, User)

    def test_username(self):
        self.assertEqual(self.user.username, MODEL_USER["User"]["username"])

    def test_password(self):
        self.assertNotEqual(self.user.password, MODEL_USER["User"]["password"])

    def test_email(self):
        self.assertEqual(self.user.email, MODEL_USER["User"]["email"])

    def test_user_permission(self):
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)
        self.assertTrue(self.user.is_active)

        # Make user as super & validate
        self.user.is_superuser = True
        self.user.save()
        self.assertTrue(self.user.is_superuser)


class DailyTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.user = User.objects.create_user(**MODEL_USER["Daily"])
        cls.daily = Daily(
            date=MODEL_DIARY["date"], content=MODEL_DIARY["content"], user=cls.user
        )
        return super().setUpClass()

    def test_daily_instance(self):
        self.assertIsInstance(self.daily, Daily)

    def test_daily_date(self):
        self.assertEqual(self.daily.date, MODEL_DIARY["date"])

    def test_daily_content(self):
        self.assertEqual(self.daily.content, MODEL_DIARY["content"])

    def test_daily_user(self):
        self.assertEqual(self.daily.user.username, MODEL_USER["Daily"]["username"])

    def test_daily_bookmark(self):
        self.assertFalse(self.daily.bookmark)

        # Make bookmark true & validate
        self.daily.bookmark = True
        self.daily.save()
        self.assertTrue(self.daily.bookmark)

    def test_daily_str(self):
        self.assertEqual(
            self.daily.__str__(),
            f"{MODEL_USER['Daily']['username']} - {MODEL_DIARY['date']}",
        )



class FeedbackTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.user = User.objects.create_user(**MODEL_USER["Feedback"])
        cls.feedback = Feedback(
            subject=MODEL_FEEDBACK["subject"],
            your_feedback=MODEL_FEEDBACK["your_feedback"],
            user=cls.user,
        )
        return super().setUpClass()

    def test_feedback_instance(self):
        self.assertIsInstance(self.feedback, Feedback)

    def test_feedback_subject(self):
        self.assertEqual(self.feedback.subject, MODEL_FEEDBACK["subject"])

    def test_feedback_content(self):
        self.assertEqual(self.feedback.your_feedback, MODEL_FEEDBACK["your_feedback"])

    def test_feedback_user(self):
        self.assertEqual(
            self.feedback.user.username, MODEL_USER["Feedback"]["username"]
        )

    def test_feedback_str(self):
        self.assertEqual(self.feedback.__str__(), MODEL_FEEDBACK["subject"])
