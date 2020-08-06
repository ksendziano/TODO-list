from django.contrib.auth.models import AnonymousUser
from django.test import TestCase
from django.urls import reverse

from users.forms import FormLogin, SignUpForm
from users.models import User

# Create your tests here.

USER_EMAIL = 'user@user.com'
USER_PASSWORD = 'User12345'
USER_NAME = 'user'

USER_EMAIL_2 = 'user2@user2.com'
USER_PASSWORD_2 = 'User123456'
USER_NAME_2 = 'user 2'

LOGIN_URL = 'auth:login'
SIGN_UP_URL = 'auth:sign_up'


class WorkLoginPageTest(TestCase):

    def setUp(self):
        user = User.objects.create_user(email=USER_EMAIL, password=USER_PASSWORD)
        user.name = USER_NAME
        user.save()

    def test_get_login_page(self):
        response = self.client.get(reverse('main-page'), follow=True)
        self.assertURLEqual((response.redirect_chain[0][0]), reverse(LOGIN_URL))
        self.assertTemplateUsed(response, 'LoginPage.html')
        self.assertIsInstance(response.context['form'], FormLogin)

    def test_login_user(self):
        response = self.client.post(reverse(LOGIN_URL), {'email': USER_EMAIL,
                                                         'password': USER_PASSWORD}, follow=True)
        self.assertURLEqual(response.redirect_chain[0][0], reverse('main-page'))
        self.assertEquals(response.context['user'].email, USER_EMAIL)
        self.assertTemplateUsed(response, 'BoardList.html')
        self.client.logout()

    def test_login_incorrect_data(self):
        response = self.client.post(reverse(LOGIN_URL), {'email': USER_EMAIL,
                                                         'password': USER_PASSWORD_2}, follow=True)
        self.assertURLEqual(response.redirect_chain[0][0], reverse(LOGIN_URL))
        self.assertIsInstance(response.context['user'], AnonymousUser)
        messages = list(response.context['messages'])
        self.assertEquals(str(messages[0]), 'Incorrect email or password')


class WorkSignUpPage(TestCase):

    def test_get_sign_up_page(self):
        response = self.client.get(reverse(SIGN_UP_URL), follow=True)
        self.assertTemplateUsed(response, 'SignUp.html')
        self.assertIsInstance(response.context['form'], SignUpForm)

    def test_sign_up_user(self):
        self.assertEqual(User.objects.all().count(), 0)
        response = self.client.post(reverse(SIGN_UP_URL), {'username': USER_NAME,
                                                           'email': USER_EMAIL,
                                                           'password': USER_PASSWORD}, follow=True)
        self.assertEqual(User.objects.all().count(), 1)
        self.assertURLEqual(response.redirect_chain[0][0], reverse(LOGIN_URL))
        user = User.objects.get(email=USER_EMAIL)
        self.assertEquals(user.is_moderator, False)
        response = self.client.post(reverse(SIGN_UP_URL), {'username': USER_NAME_2,
                                                           'email': USER_EMAIL_2,
                                                           'password': USER_PASSWORD_2,
                                                           'moderator': True}, follow=True)
        self.assertEqual(User.objects.all().count(), 2)
        self.assertURLEqual(response.redirect_chain[0][0], reverse(LOGIN_URL))
        user = User.objects.get(email=USER_EMAIL_2)
        self.assertEquals(user.is_moderator, True)

    def test_validate_sign_up_data(self):
        response = self.client.post(reverse(SIGN_UP_URL), {'username': USER_NAME,
                                                           'email': 'user@user',
                                                           'password': USER_PASSWORD}, follow=True)
        self.assertEquals(User.objects.all().count(), 0)
        messages = list(response.context['messages'])
        self.assertEquals(str(messages[0]), 'Incorrect email format')
        self.assertURLEqual(response.redirect_chain[0][0], reverse(SIGN_UP_URL))
        response = self.client.post(reverse(SIGN_UP_URL), {'username': USER_NAME,
                                                           'email': USER_EMAIL,
                                                           'password': 'simple'}, follow=True)
        self.assertEquals(User.objects.all().count(), 0)
        self.assertURLEqual(response.redirect_chain[0][0], reverse(SIGN_UP_URL))
        messages = list(response.context['messages'])
        self.assertEquals(str(messages[0]), 'Password is simple')
        response = self.client.post(reverse(SIGN_UP_URL), {'username': USER_NAME,
                                                           'email': USER_EMAIL,
                                                           'password': '123456789'}, follow=True)
        self.assertEquals(User.objects.all().count(), 0)
        self.assertURLEqual(response.redirect_chain[0][0], reverse(SIGN_UP_URL))
        messages = list(response.context['messages'])
        self.assertEquals(str(messages[0]), 'Password is simple')

    def test_sign_up_not_unique_email(self):
        user = User.objects.create_user(email=USER_EMAIL, password=USER_PASSWORD)
        user.name = USER_NAME
        user.save()
        response = self.client.post(reverse(SIGN_UP_URL), {'username': USER_NAME_2,
                                                           'email': USER_EMAIL,
                                                           'password': USER_PASSWORD_2}, follow=True)
        self.assertURLEqual(response.redirect_chain[0][0], reverse(SIGN_UP_URL))
        messages = list(response.context['messages'])
        self.assertEquals(str(messages[0]), 'That email has already taken')
