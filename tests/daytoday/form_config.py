FORM_FIELDS = {
    "login": ["username", "password"],
    "new_content": ["date", "content", "bookmark"],
    "edit_content": ["date", "content", "bookmark"],
    "register": ["username", "email", "password1", "password2"],
    "feedback": ["subject", "your_feedback"],
}

FORM_USER = {
    "Login": {
        "username": "FormTestUser",
        "password": "Testpassword$*1",
        "email": "formtestemaillogin@gmail.com",
    },
    "Register": {
        "username": "FormTestUser1",
        "email": "formtestemaillogin1@gmail.com",
        "password1": "Testpassword$*1",
        "password2": "Testpassword$*1",
    },
    "WrongRegister": {
        "short_user": "12",
        "long_user": "FormTestUserLongRegister",
        "sp_chars_user": "testt1@",
        "empty_user": "",
        "wrong_email": "formtestemaillogin1",
        "wrong_password1": "125",
        "wrong_password2": "Testpassword$*11",
    },
}

FORM_NEW_CONTENT = {"date": "2022-05-15", "content": "test day to day routines"}

FORM_EDIT_CONTENT = {"date": "2022-05-18", "content": "test day to day routines"}

FORM_FEEDBACK = {
    "subject": "test feedback subject",
    "your_feedback": "test feedback content",
}
