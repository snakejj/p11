from django.test import RequestFactory
from mixer.backend.django import mixer
from django import urls
from django.contrib.sessions.models import Session

from users.views import *
from .. import views
from django.contrib import messages

import pytest


def test_if_signup_view_is_working(client):
    signup_url = urls.reverse('users:signup')
    resp = client.get(signup_url)
    assert resp.status_code == 200, 'Is callable by anyone'


@pytest.mark.django_db
def test_if_signup_view_is_working_when_signing_up(client):
    signup_url = urls.reverse('users:signup')
    resp = client.post(signup_url,{
        'username': 'my_username',
        'first_name': 'firstname',
        'email': 'dsqijdsqdsq@mail.com',
        'password1': 'my_password123',
        'password2': 'my_password123'
    })

    assert resp.status_code == 302 and resp.url == urls.reverse('users:login'), 'Should redirect to the login page'



@pytest.mark.django_db
def test_if_login_view_is_working_with_improper_password(client):

    # Create a fake user
    user = mixer.blend('auth.User', username='my_username')
    user.set_password('my_password123')
    user.save()

    login_url = urls.reverse('users:login')
    resp = client.post(login_url, {
        'username': 'my_username',
        'password': 'improper_password'
    })

    assert resp.status_code == 200, 'Should refresh the page'
    assert not Session.objects.exists(), 'Should not be any session if login failed'

@pytest.mark.django_db
def test_if_login_view_is_working_with_improper_user(client):

    # Create a fake user
    user = mixer.blend('auth.User', username='my_username')
    user.set_password('my_password123')
    user.save()

    login_url = urls.reverse('users:login')
    resp = client.post(login_url, {
        'username': 'my_username_error',
        'password': 'my_password123'
    })

    assert resp.status_code == 200, 'Should refresh the page'
    assert not Session.objects.exists(), 'Should not be any session if login failed'

@pytest.mark.django_db
def test_if_login_view_is_working_with_proper_credentials(client):

    # Create a fake user
    user = mixer.blend('auth.User', username='my_username', is_active='True')
    user.set_password('my_password123')
    user.save()

    login_url = urls.reverse('users:login')
    resp = client.post(login_url, {
        'username': 'my_username',
        'password': 'my_password123'
    })

    assert resp.status_code == 302 and resp.url == urls.reverse('core:home'), 'Should redirect to the home page'
    assert Session.objects.count() == 1, 'Should create a session for the logged in users'

@pytest.mark.django_db
def test_if_login_view_is_working_with_proper_credentials_but_inactive(client):

    # Create a fake user
    user = mixer.blend('auth.User', username='my_username', is_active='False')
    user.set_password('my_password123')
    user.save()

    login_url = urls.reverse('users:login')
    resp = client.post(login_url, {
        'username': 'my_username',
        'password': 'my_password123'
    })

    assert resp.status_code == 302 and resp.url == urls.reverse('users:login'), 'Should redirect to the login page'
    assert Session.objects.count() == 0, 'Should not create a session for the logged in users'

def test_if_profile_view_is_working(client):
    profile_url = urls.reverse('users:profile')
    resp = client.get(profile_url)
    assert resp.status_code == 200, 'Is callable by anyone'


@pytest.mark.django_db
def test_if_logout_view_is_working(client):
    test_if_login_view_is_working_with_proper_credentials(client)
    assert Session.objects.count() == 1, 'The function called should results in a session before attempting logout'

    logout_url = urls.reverse('users:logout')
    resp = client.get(logout_url)

    # Similar to the login view, the logout view redirects to the login page
    assert resp.status_code == 302 and resp.url == urls.reverse('core:home'), 'Should redirect to the home page'
    assert not Session.objects.exists(), 'Should be no more sessions left after logging out'


@pytest.mark.django_db
class TestTokenGenerator:
    def test_account_activation_with_user_none(self, monkeypatch):

        def mock_check_token(user, token):
            return True

        monkeypatch.setattr(
            "users.views.generate_token.check_token",
            mock_check_token
        )


        req = RequestFactory().get('/activation')
        resp = views.account_activation(req, "MQ==", "dsqdsq54ds6q84dsq654dsq654dsq")

        assert resp.status_code == 401, \
        'Is not working without any account'

    def test_account_activation(self, monkeypatch):

        def mock_check_token(user, token):
            return True

        def mock_messages_success(req, message, fail_silently):
            pass

        monkeypatch.setattr(
            "users.views.generate_token.check_token",
            mock_check_token
        )
        monkeypatch.setattr(
            "users.views.messages.success",
            mock_messages_success
        )

        req = RequestFactory()
        req.user = mixer.blend('auth.User', id=1, username='my_username', is_active='False')

        # 'MQ==' is the number 1 encoded in base 64
        resp = views.account_activation(req, "MQ==", "token_exemple")

        assert resp.status_code == 302, \
            'Is redirecting when with an account'