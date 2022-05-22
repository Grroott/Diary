from django.forms.widgets import TextInput, PasswordInput, CheckboxInput, Textarea
from ckeditor.widgets import CKEditorWidget
from django.test import SimpleTestCase, TestCase
from daytoday.forms import (
    SelectDate,
    MyLoginAuthForm,
    NewContentForm,
    ContentEditForm,
    UserRegisterForm,
    FeedbackForm,
)
from django.contrib.auth.models import User
from .form_config import (
    FORM_FIELDS,
    FORM_USER,
    FORM_NEW_CONTENT,
    FORM_EDIT_CONTENT,
    FORM_FEEDBACK,
)


class SelectDateTest(SimpleTestCase):
    def test_select_date(self):
        self.date_form = SelectDate()
        self.assertEqual(self.date_form.input_type, "date")


class LoginTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.empty_form = MyLoginAuthForm()
        cls.user = User.objects.create_user(**FORM_USER["Login"])
        return super().setUpClass()

    def test_username_field(self):
        self.assertEqual(self.empty_form.fields["username"].label, "Username")
        self.assertEqual(self.empty_form.fields["username"].max_length, 150)
        self.assertTrue(self.empty_form.fields["username"].required)
        self.assertEqual(self.empty_form.fields["username"].help_text, "")
        self.assertIsInstance(self.empty_form.fields["username"].widget, TextInput)

    def test_password_field(self):
        self.assertEqual(self.empty_form.fields["password"].label, "Password")
        self.assertIsNone(self.empty_form.fields["password"].max_length)
        self.assertTrue(self.empty_form.fields["password"].required)
        self.assertEqual(self.empty_form.fields["password"].help_text, "")
        self.assertIsInstance(self.empty_form.fields["password"].widget, PasswordInput)

    def test_field_names(self):
        self.assertListEqual(list(self.empty_form.fields.keys()), FORM_FIELDS["login"])

    def test_login_validation(self):
        self.assertFalse(self.empty_form.is_valid())

        self.login_form = MyLoginAuthForm(
            data={
                "username": FORM_USER["Login"]["username"],
                "password": FORM_USER["Login"]["password"],
            }
        )
        self.assertTrue(self.login_form.is_valid())

    def test_wrong_username(self):
        self.username_wrong_form = MyLoginAuthForm(
            data={
                "username": "wrngusername",
                "password": FORM_USER["Login"]["password"],
            }
        )
        self.assertFalse(self.username_wrong_form.is_valid())
        self.assertInHTML(
            "Please enter a correct Username &amp; Password",
            str(self.username_wrong_form.errors),
        )

    def test_wrong_password(self):
        self.username_wrong_form = MyLoginAuthForm(
            data={
                "username": FORM_USER["Login"]["username"],
                "password": "wrongpassword",
            }
        )
        self.assertFalse(self.username_wrong_form.is_valid())
        self.assertInHTML(
            "Please enter a correct Username &amp; Password",
            str(self.username_wrong_form.errors),
        )

    def test_missing_username(self):
        self.no_username_form = MyLoginAuthForm(
            data={"password": FORM_USER["Login"]["password"]}
        )
        self.assertFalse(self.no_username_form.is_valid())
        self.assertInHTML("This field is required.", str(self.no_username_form.errors))

    def test_missing_password(self):
        self.no_password_form = MyLoginAuthForm(
            data={"username": FORM_USER["Login"]["username"]}
        )
        self.assertFalse(self.no_password_form.is_valid())
        self.assertInHTML("This field is required.", str(self.no_password_form.errors))


class NewContentTest(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        cls.empty_content_form = NewContentForm()
        return super().setUpClass()

    def test_date_field(self):
        self.assertEqual(self.empty_content_form.fields["date"].label, "Date")
        self.assertTrue(self.empty_content_form.fields["date"].required)
        self.assertEqual(self.empty_content_form.fields["date"].help_text, "")
        self.assertIsInstance(self.empty_content_form.fields["date"].widget, SelectDate)

    def test_content_field(self):
        self.assertEqual(self.empty_content_form.fields["content"].label, "Content")
        self.assertTrue(self.empty_content_form.fields["content"].required)
        self.assertEqual(self.empty_content_form.fields["content"].help_text, "")
        self.assertIsInstance(
            self.empty_content_form.fields["content"].widget, CKEditorWidget
        )

    def test_bookmark_field(self):
        self.assertEqual(self.empty_content_form.fields["bookmark"].label, "Bookmark")
        self.assertFalse(self.empty_content_form.fields["bookmark"].required)
        self.assertEqual(self.empty_content_form.fields["bookmark"].help_text, "")
        self.assertIsInstance(
            self.empty_content_form.fields["bookmark"].widget, CheckboxInput
        )

    def test_field_names(self):
        self.assertListEqual(
            list(self.empty_content_form.fields.keys()), FORM_FIELDS["new_content"]
        )

    def test_new_content_validation(self):
        self.assertFalse(self.empty_content_form.is_valid())

        self.valid_form = NewContentForm(
            data={
                "date": FORM_NEW_CONTENT["date"],
                "content": FORM_NEW_CONTENT["content"],
                "bookmark": True,
            }
        )
        self.assertTrue(self.valid_form.is_valid())
        self.assertTrue(self.valid_form.data.get("date"), FORM_NEW_CONTENT["date"])
        self.assertTrue(
            self.valid_form.data.get("content"), FORM_NEW_CONTENT["content"]
        )
        self.assertTrue(self.valid_form.data.get("bookmark"), True)

    def test_no_date(self):
        self.no_date_form = NewContentForm(
            data={
                "content": FORM_NEW_CONTENT["content"],
                "bookmark": True,
            }
        )
        self.assertFalse(self.no_date_form.is_valid())

    def test_no_content(self):
        self.no_content_form = NewContentForm(
            data={
                "date": FORM_NEW_CONTENT["date"],
                "bookmark": True,
            }
        )
        self.assertFalse(self.no_content_form.is_valid())

    def test_no_bookmark(self):
        self.no_bookmark_form = NewContentForm(
            data={
                "date": FORM_NEW_CONTENT["date"],
                "content": FORM_NEW_CONTENT["content"],
            }
        )
        self.assertTrue(self.no_bookmark_form.is_valid())


class ContentEditTest(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        cls.empty_content_form = ContentEditForm()
        return super().setUpClass()

    def test_date_field(self):
        self.assertEqual(self.empty_content_form.fields["date"].label, "Date")
        self.assertTrue(self.empty_content_form.fields["date"].required)
        self.assertEqual(self.empty_content_form.fields["date"].help_text, "")
        self.assertIsInstance(self.empty_content_form.fields["date"].widget, SelectDate)

    def test_content_field(self):
        self.assertEqual(self.empty_content_form.fields["content"].label, "Content")
        self.assertTrue(self.empty_content_form.fields["content"].required)
        self.assertEqual(self.empty_content_form.fields["content"].help_text, "")
        self.assertIsInstance(
            self.empty_content_form.fields["content"].widget, CKEditorWidget
        )

    def test_bookmark_field(self):
        self.assertEqual(self.empty_content_form.fields["bookmark"].label, "Bookmark")
        self.assertFalse(self.empty_content_form.fields["bookmark"].required)
        self.assertEqual(self.empty_content_form.fields["bookmark"].help_text, "")
        self.assertIsInstance(
            self.empty_content_form.fields["bookmark"].widget, CheckboxInput
        )

    def test_field_names(self):
        self.assertListEqual(
            list(self.empty_content_form.fields.keys()), FORM_FIELDS["edit_content"]
        )

    def test_edit_content_validation(self):
        self.assertFalse(self.empty_content_form.is_valid())

        self.valid_form = ContentEditForm(
            data={
                "date": FORM_EDIT_CONTENT["date"],
                "content": FORM_EDIT_CONTENT["content"],
                "bookmark": True,
            }
        )
        self.assertTrue(self.valid_form.is_valid())
        self.assertTrue(self.valid_form.data.get("date"), FORM_EDIT_CONTENT["date"])
        self.assertTrue(
            self.valid_form.data.get("content"), FORM_EDIT_CONTENT["content"]
        )
        self.assertTrue(self.valid_form.data.get("bookmark"), True)

    def test_no_date(self):
        self.no_date_form = ContentEditForm(
            data={
                "content": FORM_EDIT_CONTENT["content"],
                "bookmark": True,
            }
        )
        self.assertFalse(self.no_date_form.is_valid())

    def test_no_content(self):
        self.no_content_form = ContentEditForm(
            data={
                "date": FORM_EDIT_CONTENT["date"],
                "bookmark": True,
            }
        )
        self.assertFalse(self.no_content_form.is_valid())

    def test_no_bookmark(self):
        self.no_bookmark_form = ContentEditForm(
            data={
                "date": FORM_EDIT_CONTENT["date"],
                "content": FORM_EDIT_CONTENT["content"],
            }
        )
        self.assertTrue(self.no_bookmark_form.is_valid())


class UserRegistrationTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.empty_register = UserRegisterForm()
        return super().setUpClass()

    def test_username_field(self):
        self.assertIsNone(self.empty_register.fields["username"].label)
        self.assertTrue(self.empty_register.fields["username"].required)
        self.assertEqual(
            self.empty_register.fields["username"].help_text,
            "Username should be Alphanumeric of length 5 to 15",
        )
        self.assertIsInstance(self.empty_register.fields["username"].widget, TextInput)

    def test_email_field(self):
        self.assertIsNone(self.empty_register.fields["email"].label)
        self.assertTrue(self.empty_register.fields["email"].required)
        self.assertEqual(self.empty_register.fields["email"].help_text, "")
        self.assertIsInstance(self.empty_register.fields["username"].widget, TextInput)

    def test_password1_field(self):
        self.assertEqual(self.empty_register.fields["password1"].label, "Password")
        self.assertTrue(self.empty_register.fields["password1"].required)
        self.assertEqual(self.empty_register.fields["password1"].help_text, "")
        self.assertIsInstance(
            self.empty_register.fields["password1"].widget, PasswordInput
        )

    def test_password2_field(self):
        self.assertEqual(
            self.empty_register.fields["password2"].label, "Re-enter password"
        )
        self.assertTrue(self.empty_register.fields["password2"].required)
        self.assertEqual(self.empty_register.fields["password2"].help_text, "")
        self.assertIsInstance(
            self.empty_register.fields["password2"].widget, PasswordInput
        )

    def test_field_names(self):
        self.assertListEqual(
            list(self.empty_register.fields.keys()), FORM_FIELDS["register"]
        )

    def test_register_validation(self):
        self.assertFalse(self.empty_register.is_valid())

        self.valid_form = UserRegisterForm(
            data={
                "username": FORM_USER["Register"]["username"],
                "email": FORM_USER["Register"]["email"],
                "password1": FORM_USER["Register"]["password1"],
                "password2": FORM_USER["Register"]["password1"],
            }
        )
        self.assertTrue(self.valid_form.is_valid())

        self.assertTrue(
            self.valid_form.data.get("username"), FORM_USER["Register"]["username"]
        )
        self.assertTrue(
            self.valid_form.data.get("email"), FORM_USER["Register"]["email"]
        )
        self.assertTrue(
            self.valid_form.data.get("password1"), FORM_USER["Register"]["password1"]
        )
        self.assertTrue(
            self.valid_form.data.get("password2"), FORM_USER["Register"]["password2"]
        )

    def test_invalid_username(self):
        self.short_user_form = UserRegisterForm(
            data={
                "username": FORM_USER["WrongRegister"]["short_user"],
                "email": FORM_USER["Register"]["email"],
                "password1": FORM_USER["Register"]["password1"],
                "password2": FORM_USER["Register"]["password1"],
            }
        )
        self.assertFalse(self.short_user_form.is_valid())
        self.assertInHTML(
            "Ensure this value has at least 5 characters (it has 2).",
            str(self.short_user_form.errors),
        )

        self.long_user_form = UserRegisterForm(
            data={
                "username": FORM_USER["WrongRegister"]["long_user"],
                "email": FORM_USER["Register"]["email"],
                "password1": FORM_USER["Register"]["password1"],
                "password2": FORM_USER["Register"]["password1"],
            }
        )
        self.assertFalse(self.long_user_form.is_valid())
        self.assertInHTML(
            "Ensure this value has at most 15 characters (it has 24).",
            str(self.long_user_form.errors),
        )

        self.sp_chars_user_form = UserRegisterForm(
            data={
                "username": FORM_USER["WrongRegister"]["sp_chars_user"],
                "email": FORM_USER["Register"]["email"],
                "password1": FORM_USER["Register"]["password1"],
                "password2": FORM_USER["Register"]["password1"],
            }
        )
        self.assertFalse(self.sp_chars_user_form.is_valid())
        self.assertInHTML(
            "Enter a valid username. This value may contain only letters and numbers",
            str(self.sp_chars_user_form.errors),
        )

        self.empty_user_form = UserRegisterForm(
            data={
                "username": FORM_USER["WrongRegister"]["empty_user"],
                "email": FORM_USER["Register"]["email"],
                "password1": FORM_USER["Register"]["password1"],
                "password2": FORM_USER["Register"]["password1"],
            }
        )
        self.assertFalse(self.empty_user_form.is_valid())
        self.assertInHTML(
            "This field is required.",
            str(self.empty_user_form.errors),
        )

    def test_wrong_email_form(self):
        self.wrong_email_form = UserRegisterForm(
            data={
                "username": FORM_USER["Register"]["username"],
                "email": FORM_USER["WrongRegister"]["wrong_email"],
                "password1": FORM_USER["Register"]["password1"],
                "password2": FORM_USER["Register"]["password1"],
            }
        )
        self.assertFalse(self.wrong_email_form.is_valid())
        self.assertInHTML(
            "Enter a valid email address.",
            str(self.wrong_email_form.errors),
        )

    def test_wrong_password(self):

        self.small_pwd_form = UserRegisterForm(
            data={
                "username": FORM_USER["Register"]["username"],
                "email": FORM_USER["Register"]["email"],
                "password1": FORM_USER["WrongRegister"]["wrong_password1"],
                "password2": FORM_USER["WrongRegister"]["wrong_password1"],
            }
        )
        self.assertFalse(self.small_pwd_form.is_valid())
        self.assertInHTML(
            "This password is too short. It must contain at least 8 characters.",
            str(self.small_pwd_form.errors),
        )

        self.wrong_pwd2_form = UserRegisterForm(
            data={
                "username": FORM_USER["Register"]["username"],
                "email": FORM_USER["Register"]["email"],
                "password1": FORM_USER["Register"]["password1"],
                "password2": FORM_USER["WrongRegister"]["wrong_password2"],
            }
        )
        self.assertFalse(self.wrong_pwd2_form.is_valid())
        self.assertInHTML(
            "The two password fields didn’t match.",
            str(self.wrong_pwd2_form.errors),
        )


class FeedbackTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.empty_feedback_form = FeedbackForm()
        return super().setUpClass()

    def test_subject_field(self):
        self.assertEqual(self.empty_feedback_form.fields["subject"].label, "Subject")
        self.assertTrue(self.empty_feedback_form.fields["subject"].required)
        self.assertEqual(
            self.empty_feedback_form.fields["subject"].help_text,
            "",
        )
        self.assertIsInstance(
            self.empty_feedback_form.fields["subject"].widget, TextInput
        )

    def test_your_feedback_field(self):
        self.assertEqual(
            self.empty_feedback_form.fields["your_feedback"].label, "Your feedback"
        )
        self.assertTrue(self.empty_feedback_form.fields["your_feedback"].required)
        self.assertEqual(self.empty_feedback_form.fields["your_feedback"].help_text, "")
        self.assertIsInstance(
            self.empty_feedback_form.fields["your_feedback"].widget, Textarea
        )

    def test_field_names(self):
        self.assertListEqual(
            list(self.empty_feedback_form.fields.keys()), FORM_FIELDS["feedback"]
        )

    def test_register_validation(self):
        self.assertFalse(self.empty_feedback_form.is_valid())

        self.valid_form = FeedbackForm(
            data={
                "subject": FORM_FEEDBACK["subject"],
                "your_feedback": FORM_FEEDBACK["your_feedback"],
            }
        )
        self.assertTrue(self.valid_form.is_valid())

        self.assertTrue(self.valid_form.data.get("subject"), FORM_FEEDBACK["subject"])
        self.assertTrue(
            self.valid_form.data.get("your_feedback"), FORM_FEEDBACK["your_feedback"]
        )

    def test_missing_subject(self):
        self.no_subject_form = FeedbackForm(
            data={"your_feedback": FORM_FEEDBACK["your_feedback"]}
        )
        self.assertFalse(self.no_subject_form.is_valid())
        self.assertInHTML("This field is required.", str(self.no_subject_form.errors))

    def test_missing_feedback(self):
        self.no_feedback_form = FeedbackForm(data={"subject": FORM_FEEDBACK["subject"]})
        self.assertFalse(self.no_feedback_form.is_valid())
        self.assertInHTML("This field is required.", str(self.no_feedback_form.errors))
