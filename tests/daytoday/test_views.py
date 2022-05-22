from django.test import TestCase
from http import HTTPStatus
from django.urls import reverse
from django.utils import timezone
from .views_config import (
    VIEW_LOGIN_REQUIRED_URL,
    VIEW_USER,
    VIEW_DAILY,
    VIEW_FEEDBACK,
    VIEW_OTHER_DATES,
    VIEW_HTML_MAP,
)
from django.contrib.auth.models import User
from daytoday.models import Daily, Feedback


class HomeTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(**VIEW_USER["Home"])
        return super().setUpClass()

    def test_gethome_without_login(self):
        wrong_home = self.client.get(reverse("home"))
        self.assertEqual(wrong_home.status_code, HTTPStatus.FOUND.value)
        self.assertEqual(wrong_home.url, VIEW_LOGIN_REQUIRED_URL + reverse("home"))

    def test_posthome_without_login(self):
        wrong_home = self.client.post(
            reverse("home"), {"selected_date": VIEW_DAILY["date"]}
        )
        self.assertEqual(wrong_home.status_code, HTTPStatus.FOUND.value)
        self.assertEqual(wrong_home.url, VIEW_LOGIN_REQUIRED_URL + reverse("home"))

    def test_home_get(self):
        self.client.post(reverse("login"), VIEW_USER["Home"])

        get_home = self.client.get(reverse("home"))
        self.assertEqual(get_home.status_code, HTTPStatus.OK.value)
        self.assertTrue(
            f"'date': '{timezone.now().date().strftime('%Y-%m-%d')}'"
            in str(get_home.context)
        )
        self.assertTemplateUsed(get_home, VIEW_HTML_MAP["home"])

    def test_home_post(self):
        self.client.post(reverse("login"), VIEW_USER["Home"])

        # post empty data
        no_data_post_home = self.client.post(reverse("home"), {"selected_date": ""})
        self.assertEqual(no_data_post_home.status_code, HTTPStatus.OK.value)
        self.assertEqual(no_data_post_home.content, b"No date selected!")

        # post any date
        data_post_home = self.client.post(
            reverse("home"), {"selected_date": VIEW_DAILY["date"]}
        )
        self.assertEqual(data_post_home.status_code, HTTPStatus.FOUND.value)
        self.assertEqual(data_post_home.content, b"")
        self.assertEqual(data_post_home.url, reverse("home") + VIEW_DAILY["date"])


class ViewSpecificContentTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(**VIEW_USER["ViewSpecific"])
        return super().setUpClass()

    def test_viewcontent_without_login(self):
        without_login = self.client.get(reverse("home"))
        self.assertEqual(without_login.status_code, HTTPStatus.FOUND.value)
        self.assertEqual(without_login.url, VIEW_LOGIN_REQUIRED_URL + reverse("home"))

    def test_without_content(self):
        self.client.post(reverse("login"), VIEW_USER["ViewSpecific"])
        without_content = self.client.get(
            reverse("view_specific_content", kwargs={"date": VIEW_DAILY["date"]})
        )
        self.assertEqual(without_content.status_code, HTTPStatus.OK.value)
        self.assertTemplateUsed(without_content, VIEW_HTML_MAP["dairy_not_written"])
        self.assertTrue(
            f"""'date': '{VIEW_DAILY["date"]}'""" in str(without_content.context)
        )

    def test_with_content(self):
        self.client.post(reverse("login"), VIEW_USER["ViewSpecific"])
        self.content = Daily(
            date=VIEW_DAILY["date"],
            content=VIEW_DAILY["content"],
            user=self.user,
        )
        self.content.save()
        with_content = self.client.get(
            reverse("view_specific_content", kwargs={"date": VIEW_DAILY["date"]})
        )
        self.assertEqual(with_content.status_code, HTTPStatus.OK.value)
        self.assertTemplateUsed(with_content, VIEW_HTML_MAP["view_specific"])
        self.assertTrue(
            f"""'posts': <Daily: {self.user} - {VIEW_DAILY["date"]}>"""
            in str(with_content.context)
        )

        # Another user should not have above data
        User.objects.create_user(**VIEW_USER["ViewSpecific2"])
        self.client.post(reverse("login"), VIEW_USER["ViewSpecific2"])
        new_user_content = self.client.get(
            reverse("view_specific_content", kwargs={"date": VIEW_DAILY["date"]})
        )
        self.assertTemplateUsed(new_user_content, VIEW_HTML_MAP["dairy_not_written"])


class NewContentTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.user = User.objects.create_user(**VIEW_USER["NewContent"])
        return super().setUpClass()

    def test_newcontent_without_login(self):
        without_login = self.client.get(reverse("new_content"))
        self.assertEqual(without_login.status_code, HTTPStatus.FOUND.value)
        self.assertEqual(
            without_login.url, VIEW_LOGIN_REQUIRED_URL + reverse("new_content")
        )

    def test_post_existing_date(self):
        self.client.post(reverse("login"), VIEW_USER["NewContent"])
        self.content = Daily(
            date=VIEW_DAILY["date"],
            content=VIEW_DAILY["content"],
            user=self.user,
        )
        self.content.save()
        data_old_post = self.client.post(
            reverse("new_content"), {"date": VIEW_DAILY["date"]}
        )
        self.assertEqual(data_old_post.status_code, HTTPStatus.FOUND.value)
        self.assertEqual(data_old_post.url, reverse("home") + VIEW_DAILY["date"])

    def test_post_new_date(self):
        self.client.post(reverse("login"), VIEW_USER["NewContent"])
        data_new_post = self.client.post(
            reverse("new_content"), {"date": VIEW_OTHER_DATES["Date1"]}
        )
        self.assertEqual(data_new_post.status_code, HTTPStatus.OK.value)
        self.assertTrue(
            f"""'value': '{VIEW_OTHER_DATES["Date1"]}'""" in str(data_new_post.context)
        )

    def test_get_with_date(self):
        self.client.post(reverse("login"), VIEW_USER["NewContent"])
        data_new_get_selected = self.client.get(
            reverse("new_content"), {"selected_date": VIEW_OTHER_DATES["Date2"]}
        )
        self.assertEqual(data_new_get_selected.status_code, HTTPStatus.OK.value)
        self.assertTemplateUsed(data_new_get_selected, VIEW_HTML_MAP["new_content"])
        self.assertTrue(
            f"""'value': '{VIEW_OTHER_DATES["Date2"]}'"""
            in str(data_new_get_selected.context)
        )

    def test_get_without_date(self):
        self.client.post(reverse("login"), VIEW_USER["NewContent"])
        data_new_get = self.client.get(reverse("new_content"))
        self.assertEqual(data_new_get.status_code, HTTPStatus.OK.value)
        self.assertTrue(
            f"""'value': '{str(timezone.now().date().strftime('%Y-%m-%d'))}'"""
            in str(data_new_get.context)
        )


class EditContentTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.user = User.objects.create_user(**VIEW_USER["EditContent"])
        cls.daily = Daily(
            date=VIEW_DAILY["date"],
            content=VIEW_DAILY["content"],
            user=cls.user,
        )
        cls.daily.save()
        cls.url = reverse("edit_content", kwargs={"date": VIEW_DAILY["date"]})
        return super().setUpClass()

    def test_newcontent_without_login(self):
        without_login = self.client.get(self.url)
        self.assertEqual(without_login.status_code, HTTPStatus.FOUND.value)
        self.assertEqual(without_login.url, VIEW_LOGIN_REQUIRED_URL + self.url)

    def test_edit_get(self):
        self.client.post(reverse("login"), VIEW_USER["EditContent"])
        edit_get = self.client.get(self.url)
        self.assertTrue(f"""'value': '{VIEW_DAILY["date"]}'""" in str(edit_get.context))
        self.assertTrue(
            f"""'value': '{VIEW_DAILY["content"]}'""" in str(edit_get.context)
        )

    def test_edit_get_404(self):
        self.client.post(reverse("login"), VIEW_USER["EditContent"])
        edit_get_404 = self.client.get(
            reverse("edit_content", kwargs={"date": VIEW_OTHER_DATES["Date1"]})
        )
        self.assertEqual(edit_get_404.status_code, HTTPStatus.NOT_FOUND.value)

    def test_edit_post(self):
        self.client.post(reverse("login"), VIEW_USER["EditContent"])
        edit_post = self.client.post(
            self.url,
            {
                "date": VIEW_DAILY["date"],
                "content": VIEW_DAILY["content"] + " updated now",
            },
        )
        self.assertEqual(edit_post.status_code, HTTPStatus.FOUND.value)
        self.assertEqual(
            edit_post.url,
            reverse("view_specific_content", kwargs={"date": VIEW_DAILY["date"]}),
        )
        updated_data = Daily.objects.get(user=self.user, date=VIEW_DAILY["date"])
        self.assertEqual(updated_data.content, VIEW_DAILY["content"] + " updated now")


class DeleteContentTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.user = User.objects.create_user(**VIEW_USER["DeleteContent"])
        cls.daily = Daily(
            date=VIEW_DAILY["date"],
            content=VIEW_DAILY["content"],
            user=cls.user,
        )
        cls.daily.save()
        cls.url = reverse("delete_content", kwargs={"date": VIEW_DAILY["date"]})
        return super().setUpClass()

    def test_delete_without_login(self):
        no_login_delete = self.client.get(self.url)
        self.assertEqual(no_login_delete.status_code, HTTPStatus.FOUND.value)
        self.assertEqual(no_login_delete.url, VIEW_LOGIN_REQUIRED_URL + self.url)

    def test_delete_with_login(self):
        self.client.post(reverse("login"), VIEW_USER["DeleteContent"])
        self.assertTrue(Daily.objects.get(user=self.user, date=VIEW_DAILY["date"]))
        login_delete = self.client.get(self.url)
        self.assertEqual(login_delete.status_code, HTTPStatus.FOUND.value)
        self.assertEqual(login_delete.url, reverse("home"))
        self.assertFalse(Daily.objects.filter(user=self.user, date=VIEW_DAILY["date"]))

    def test_404_delete(self):
        self.client.post(reverse("login"), VIEW_USER["DeleteContent"])
        url = reverse(
            "delete_content",
            kwargs={"date": VIEW_OTHER_DATES["Date1"]},
        )
        delete_404 = self.client.get(url)
        self.assertEqual(delete_404.status_code, HTTPStatus.NOT_FOUND.value)


class RegisterTest(TestCase):
    def test_get_register(self):
        get_register = self.client.get(reverse("register"))
        self.assertTemplateUsed(get_register, VIEW_HTML_MAP["register"])
        self.assertEqual(get_register.status_code, HTTPStatus.OK.value)
        self.assertFalse(
            User.objects.filter(username=VIEW_USER["Register"]["username"])
        )

    def test_post_register(self):
        post_register = self.client.post(
            reverse("register"),
            {
                "username": VIEW_USER["Register"]["username"],
                "email": VIEW_USER["Register"]["email"],
                "password1": VIEW_USER["Register"]["password1"],
                "password2": VIEW_USER["Register"]["password2"],
            },
        )
        self.assertEqual(post_register.status_code, HTTPStatus.FOUND.value)
        self.assertEqual(post_register.url, reverse("login"))
        register_user = User.objects.get(username=VIEW_USER["Register"]["username"])
        self.assertFalse(register_user.is_active)
        self.assertEqual(register_user.username, VIEW_USER["Register"]["username"])
        self.assertEqual(register_user.email, VIEW_USER["Register"]["email"])
        self.assertNotEqual(register_user.password, VIEW_USER["Register"]["password1"])


class FeedbackTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.user = User.objects.create_user(**VIEW_USER["Feedback"])
        return super().setUpClass()

    def test_feedback_without_login(self):
        without_login = self.client.get(reverse("feedback"))
        self.assertEqual(without_login.status_code, HTTPStatus.FOUND.value)
        self.assertEqual(
            without_login.url, VIEW_LOGIN_REQUIRED_URL + reverse("feedback")
        )

    def test_feedback_get(self):
        self.client.post(reverse("login"), VIEW_USER["Feedback"])
        get_response = self.client.get(reverse("feedback"))
        self.assertTemplateUsed(get_response, VIEW_HTML_MAP["feedback"])
        self.assertEqual(get_response.status_code, HTTPStatus.OK.value)

    def test_feedback_post(self):
        self.client.post(reverse("login"), VIEW_USER["Feedback"])
        self.assertFalse(Feedback.objects.filter(user=self.user))
        post_response = self.client.post(reverse("feedback"), VIEW_FEEDBACK)
        self.assertEqual(post_response.status_code, HTTPStatus.FOUND.value)
        self.assertEqual(post_response.url, reverse("home"))
        feedback_content = Feedback.objects.get(user=self.user)
        self.assertEqual(feedback_content.subject, VIEW_FEEDBACK["subject"])
        self.assertEqual(feedback_content.your_feedback, VIEW_FEEDBACK["your_feedback"])


class BookmarkDateTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.user = User.objects.create_user(**VIEW_USER["BookmarkDate"])
        cls.daily = Daily(
            date=VIEW_DAILY["date"],
            content=VIEW_DAILY["content"],
            bookmark=VIEW_DAILY["bookmark"],
            user=cls.user,
        )
        cls.daily.save()
        cls.url = reverse("bookmark_date", kwargs={"date": VIEW_DAILY["date"]})
        return super().setUpClass()

    def test_bookmarkdate_without_login(self):
        without_login = self.client.get(self.url)
        self.assertEqual(without_login.status_code, HTTPStatus.FOUND.value)
        self.assertEqual(without_login.url, VIEW_LOGIN_REQUIRED_URL + self.url)

    def test_add_bookmark(self):
        self.client.post(reverse("login"), VIEW_USER["BookmarkDate"])
        self.assertFalse(
            Daily.objects.get(user=self.user, date=VIEW_DAILY["date"]).bookmark
        )
        add_bookmark = self.client.get(self.url)
        self.assertEqual(add_bookmark.status_code, HTTPStatus.FOUND.value)
        self.assertEqual(
            add_bookmark.url,
            reverse("view_specific_content", kwargs={"date": VIEW_DAILY["date"]}),
        )
        self.assertTrue(
            Daily.objects.get(user=self.user, date=VIEW_DAILY["date"]).bookmark
        )

    def test_remove_bookmark(self):
        self.client.post(reverse("login"), VIEW_USER["BookmarkDate"])
        self.daily.bookmark = True
        self.daily.save()
        self.assertTrue(
            Daily.objects.get(user=self.user, date=VIEW_DAILY["date"]).bookmark
        )
        remove_bookmark = self.client.get(self.url)
        self.assertEqual(remove_bookmark.status_code, HTTPStatus.FOUND.value)
        self.assertEqual(
            remove_bookmark.url,
            reverse("view_specific_content", kwargs={"date": VIEW_DAILY["date"]}),
        )
        self.assertFalse(
            Daily.objects.get(user=self.user, date=VIEW_DAILY["date"]).bookmark
        )

    def test_bookmark_404(self):
        self.client.post(reverse("login"), VIEW_USER["BookmarkDate"])
        bookmark_404 = self.client.get(
            reverse("bookmark_date", kwargs={"date": VIEW_OTHER_DATES["Date1"]})
        )
        self.assertEqual(bookmark_404.status_code, HTTPStatus.NOT_FOUND.value)


class ViewBookmarkTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.user = User.objects.create_user(**VIEW_USER["ViewBookmark"])
        cls.daily = Daily(
            date=VIEW_DAILY["date"],
            content=VIEW_DAILY["content"],
            bookmark=VIEW_DAILY["bookmark"],
            user=cls.user,
        )
        cls.daily.save()
        return super().setUpClass()

    def test_bookmarkview_without_login(self):
        without_login = self.client.get(reverse("view_bookmarks"))
        self.assertEqual(without_login.status_code, HTTPStatus.FOUND.value)
        self.assertEqual(
            without_login.url, VIEW_LOGIN_REQUIRED_URL + reverse("view_bookmarks")
        )

    def test_bookmarkview_false(self):
        self.client.post(reverse("login"), VIEW_USER["ViewBookmark"])
        bookmark_false = self.client.get(reverse("view_bookmarks"))
        self.assertEqual(bookmark_false.status_code, HTTPStatus.OK.value)
        self.assertTemplateUsed(bookmark_false, VIEW_HTML_MAP["bookmarks"])
        self.assertTrue("'bookmarks': <QuerySet []>" in str(bookmark_false.context))

    def test_bookmarkview_true(self):
        self.client.post(reverse("login"), VIEW_USER["ViewBookmark"])
        self.daily.bookmark = True
        self.daily.save()
        bookmark_true = self.client.get(reverse("view_bookmarks"))
        self.assertEqual(bookmark_true.status_code, HTTPStatus.OK.value)
        self.assertTemplateUsed(bookmark_true, VIEW_HTML_MAP["bookmarks"])
        self.assertTrue(
            f"""'bookmarks': <QuerySet [<Daily: {VIEW_USER["ViewBookmark"]['username']} - {VIEW_DAILY["date"]}>]>"""
            in str(bookmark_true.context)
        )


class LoginTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(**VIEW_USER["Login"])
        return super().setUpClass()

    def test_correct_login(self):
        login = self.client.post(reverse("login"), VIEW_USER["Login"])
        self.assertEqual(login.status_code, HTTPStatus.FOUND.value)
        self.assertEqual(login.url, reverse("home"))

        # view any page that requires login
        new_content = self.client.get(reverse("new_content"))
        self.assertEqual(new_content.status_code, HTTPStatus.OK.value)

    def test_wrong_username(self):
        wrong_username = self.client.post(
            reverse("login"),
            {
                "username": VIEW_USER["WrongLogin"]["username"],
                "password": VIEW_USER["Login"]["password"],
            },
        )
        self.assertNotEqual(wrong_username.status_code, HTTPStatus.FOUND.value)

        # view any page that requires login
        new_content = self.client.get(reverse("new_content"))
        self.assertNotEqual(new_content.status_code, HTTPStatus.OK.value)

    def test_wrong_password(self):
        wrong_password = self.client.post(
            reverse("login"),
            {
                "username": VIEW_USER["Login"]["username"],
                "password": VIEW_USER["WrongLogin"]["password"],
            },
        )
        self.assertNotEqual(wrong_password.status_code, HTTPStatus.FOUND.value)

        # view any page that requires login
        new_content = self.client.get(reverse("new_content"))
        self.assertNotEqual(new_content.status_code, HTTPStatus.OK.value)


class AccountActivationTest(TestCase):
    def test_correct_credential(self):
        post_register = self.client.post(
            reverse("register"),
            {
                "username": VIEW_USER["AccountActivation"]["username"],
                "email": VIEW_USER["AccountActivation"]["email"],
                "password1": VIEW_USER["AccountActivation"]["password1"],
                "password2": VIEW_USER["AccountActivation"]["password2"],
            },
        )
        for dicts in post_register.context:
            if "token" in dicts.keys():
                token = dicts["token"]
                uidb64 = dicts["uid"]
                break
        token = token if token else None
        uidb64 = uidb64 if uidb64 else None

        response = self.client.get(
            reverse("account_activation", kwargs={"token": token, "uidb64": uidb64})
        )
        self.assertEqual(response.status_code, HTTPStatus.OK.value)
        self.assertEqual(
            response.content,
            b"Thank you for your email confirmation. Now you can login your account.",
        )

    def test_wrong_credential(self):
        wrong_response = self.client.get(
            reverse(
                "account_activation",
                kwargs={"token": "wrong token", "uidb64": "wrong uid64"},
            )
        )
        self.assertEqual(wrong_response.status_code, HTTPStatus.OK.value)
        self.assertEqual(wrong_response.content, b"Activation link is invalid!")
