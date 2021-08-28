from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import logout_then_login
from .views import home, view_specific_content, new_content, edit_content, delete_content, \
    register, feedback, bookmark_date, view_bookmarks, MyLoginView, account_activation

urlpatterns = [
    path('', home, name='home'),
    path('home/', home, name='home'),
    path('new_content/', new_content, name='new_content'),
    path('feedback/', feedback, name='feedback'),
    path('view_bookmarks/', view_bookmarks, name='view_bookmarks'),
    path('register/', register, name='register'),
    path('account-activation/<uidb64>/<token>', account_activation, name='account_activation'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', logout_then_login, name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='daytoday/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='daytoday/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='daytoday/password_reset_complete.html'), name='password_reset_complete'),
    path('password-reset-confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='daytoday/password_reset_confirm.html'), name='password_reset_confirm'),
    path('home/<date>', view_specific_content, name='view_specific_content'),
    path('home/<date>/edit/', edit_content, name='edit_content'),
    path('home/<date>/delete/', delete_content, name='delete_content'),
    path('home/<date>/bookmark_date/', bookmark_date, name='bookmark_date'),
]
