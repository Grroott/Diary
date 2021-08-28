from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import NewContentForm, ContentEditForm, UserRegisterForm, FeedbackForm, MyLoginAuthForm
from .models import Daily
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.contrib.auth.models import User


# Create your views here.
@login_required()
def home(request):
    if request.method == 'GET':
        context = {
            'date': timezone.now().date().strftime('%Y-%m-%d')
        }
        return render(request, 'daytoday/home.html', context=context)
    elif request.method == 'POST':
        if request.POST.get('selected_date') != '':
            return redirect('view_specific_content', date=request.POST.get('selected_date'))
        else:
            return HttpResponse("No date selected!")


@login_required()
def view_specific_content(request, date):
    qs = Daily.objects.filter(date=date, user=request.user)
    if not qs:
        return render(request, 'daytoday/dairy_not_written.html')
    else:
        context = {
            'posts': qs[0]  # get first index data
        }
        return render(request, 'daytoday/view.html', context)


@login_required()
def new_content(request):
    qs = Daily.objects.filter(user=request.user, date=request.POST.get('date'))
    if not qs:
        if request.method == "POST":
            form = NewContentForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = request.user
                instance.save()
                messages.success(request, f'Well done {request.user}, Good night!')
                return redirect('view_specific_content', date=request.POST.get('date'))
        else:
            form = NewContentForm()
        return render(request, 'daytoday/new_content.html', {'form': form})
    else:
        messages.warning(request, f'You already written dairy for this date!')
        return redirect('view_specific_content', date=request.POST.get('date'))


@login_required()
def edit_content(request, date):
    content = get_object_or_404(Daily, date=date)

    if request.method == 'POST':

        edit_form = ContentEditForm(request.POST, instance=content)
        if edit_form.is_valid():
            edit_form.save()
            messages.success(request, f'Your changes has been updated successfully!!')
            return HttpResponseRedirect(content.get_absolute_url())
    else:
        edit_form = ContentEditForm(instance=content)

    context = {
        'edit_form': edit_form,
    }

    return render(request, 'daytoday/edit_content.html', context)


@login_required()
def delete_content(request, date):
    content = get_object_or_404(Daily, date=date)
    content.delete()
    messages.success(request, f'Content deleted successfully!')

    return redirect('home')


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            hostname = get_current_site(request)
            email_id = form.cleaned_data.get('email')
            try:
                email_body = render_to_string('daytoday/account_activation.html',
                                              {'hostname': hostname, 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                               'token': account_activation_token.make_token(user), 'username': user})
                response = send_mail("Activate your Diary account!", email_body, settings.EMAIL_HOST_USER, [email_id],
                                     fail_silently=False, html_message=email_body)
                if response == 1:
                    messages.success(request,
                                     f'Your account has been created! Activation link is sent to your email address.')

                    return redirect('login')
                else:
                    messages.error(request, f'Problem while creating account, please try again in sometime.')
            except Exception as exe:
                print(exe)
                messages.error(request, f'Problem while creating account, please try again in sometime.')
    else:
        form = UserRegisterForm()
    return render(request, 'daytoday/register.html', {'form': form})


@login_required()
def feedback(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            messages.success(request, f'Thank you for sharing your feedback!')
            return redirect('home')
    else:
        form = FeedbackForm()
    return render(request, 'daytoday/feedback.html', {'form': form})


@login_required()
def bookmark_date(request, date):
    content = get_object_or_404(Daily, date=date, user=request.user)
    if content:
        if content.bookmark:
            content.bookmark = False
            content.save()
            messages.success(request, f'Bookmark removed successfully!')
        else:
            content.bookmark = True
            content.save()
            messages.success(request, f'Bookmark added successfully!')
        return redirect('view_specific_content', date=date)


@login_required()
def view_bookmarks(request):
    bookmarks = Daily.objects.filter(bookmark=True, user=request.user).order_by('-date')
    context = {
        'bookmarks': bookmarks
    }
    return render(request, 'daytoday/bookmarks.html', context=context)


class MyLoginView(LoginView):
    authentication_form = MyLoginAuthForm
    template_name = 'daytoday/login.html'


def account_activation(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = User.objects.get(pk=uid)

    except Exception as exe:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')
