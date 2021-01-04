import re

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from mixer.backend.django import mixer

from django.core import mail


class FunctionalTests(StaticLiveServerTestCase):

    def setUp(self):
        cap = DesiredCapabilities().FIREFOX
        cap["marionette"] = True
        self.browser = webdriver.Firefox(capabilities=cap, executable_path='/usr/local/bin/geckodriver/geckodriver')

    def tearDown(self):
        pass

    def test_sign_up_process_and_login(self):
        self.browser.get(self.live_server_url)
        WebDriverWait(self.browser, 10)

        assert "Page d'accueil" in self.browser.title

        # Go to the login page
        try:
            link_to_login_page = WebDriverWait(self.browser, 10).until(
                expected_conditions.presence_of_element_located((By.ID, "login"))
            )
            link_to_login_page.click()

        except:
            print("The page loading was greater than 10 seconds, hence the test was stopped")
            self.browser.quit()

        # Go to the sign up page
        try:
            link_to_signup_page = WebDriverWait(self.browser, 10).until(
                expected_conditions.presence_of_element_located((By.ID, "signup"))
            )

            link_to_signup_page.click()

        except:
            print("The page loading was greater than 10 seconds, hence the test was stopped")
            self.browser.quit()

        # Filling the form

        self.browser.find_element_by_name('username').send_keys('test_username')
        self.browser.find_element_by_name('first_name').send_keys('test_first_name')
        self.browser.find_element_by_name('last_name').send_keys('test_last_name')
        self.browser.find_element_by_name('email').send_keys('test@mail.com')
        self.browser.find_element_by_name('password1').send_keys('password654sq%')
        self.browser.find_element_by_name('password2').send_keys('password654sq%')

        # Submitting the form

        self.browser.find_element_by_id("button_send").click()

        WebDriverWait(self.browser, 10)

        assert "Login" in self.browser.title

        # Filling the login form

        self.browser.find_element_by_name('username').send_keys('test_username')
        self.browser.find_element_by_name('password').send_keys('password654sq%')

        # Submitting the form to test if the warning about unvalidated account is active, and thus redirect to login

        self.browser.find_element_by_id("button_send").click()

        WebDriverWait(self.browser, 10)

        assert "Login" in self.browser.title
        assert "Merci de cliquer sur le lien envoyé dans votre boite mail !" in \
               self.browser.page_source

        assert len(mail.outbox) is 1
        mailbody = mail.outbox[0].body
        print(mailbody)
        assert "Merci de cliquer sur le lien de verification ci dessous afin de terminer votre inscription" in mailbody

        link_regex = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
        confirmation_link_raw = re.search(link_regex, mailbody)
        confirmation_link = confirmation_link_raw[0]
        print(confirmation_link)
        self.browser.get(confirmation_link)

        assert "Votre compte à été validé avec succès" in self.browser.page_source


        # Go to the login page
        try:
            link_to_login_page = WebDriverWait(self.browser, 10).until(
                expected_conditions.presence_of_element_located((By.ID, "login"))
            )
            link_to_login_page.click()

        except:
            print("The page loading was greater than 10 seconds, hence the test was stopped")
            self.browser.quit()

        # Filling the login form

        self.browser.find_element_by_name('username').send_keys('test_username')
        self.browser.find_element_by_name('password').send_keys('password654sq%')

        # Submitting the form to test if the warning about unvalidated account is active, and thus redirect to login

        self.browser.find_element_by_id("button_send").click()

        WebDriverWait(self.browser, 10)

        assert "Bienvenue test_username !" in \
               self.browser.page_source


    def test_reset_password(self):

        user = mixer.blend('auth.User', username='my_username', email='test@passwordreset.com', is_active='True')
        user.set_password('my_password123')
        user.save()

        self.browser.get(self.live_server_url)
        WebDriverWait(self.browser, 10)

        assert "Page d'accueil" in self.browser.title

        # Go to the login page
        try:
            link_to_login_page = WebDriverWait(self.browser, 10).until(
                expected_conditions.presence_of_element_located((By.ID, "login"))
            )
            link_to_login_page.click()

        except:
            print("The page loading was greater than 10 seconds, hence the test was stopped")
            self.browser.quit()

        # Go to the sign up page
        try:
            link_to_password_reset_page = WebDriverWait(self.browser, 10).until(
                expected_conditions.presence_of_element_located((By.ID, "lostpassword"))
            )
            link_to_password_reset_page.click()

        except:
            print("The page loading was greater than 10 seconds, hence the test was stopped")
            self.browser.quit()

        # Filling the form

        self.browser.find_element_by_name('email').send_keys('test@passwordreset.com')

        # Submitting the form

        self.browser.find_element_by_id("button_send").click()

        WebDriverWait(self.browser, 10)

        assert "Password reset sent" in self.browser.title

        assert len(mail.outbox) is 1
        mailbody = mail.outbox[0].body
        print(mailbody)
        assert "Pour réinitialiser pour votre compte PurBeurre, cliquez sur le lien ci dessous:" in mailbody

        link_regex = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
        confirmation_link_raw = re.search(link_regex, mailbody)
        confirmation_link = confirmation_link_raw[0]
        print(confirmation_link)
        self.browser.get(confirmation_link)

        assert "Enter new password" in self.browser.title

        # Filling the new password form

        self.browser.find_element_by_name('new_password1').send_keys('new_password+123')
        self.browser.find_element_by_name('new_password2').send_keys('new_password+123')

        # Submitting the form to test if the warning about unvalidated account is active, and thus redirect to login

        self.browser.find_element_by_id("button_send").click()

        assert "Password reset complete" in self.browser.title

        # Go to the login page
        try:
            link_to_login_page = WebDriverWait(self.browser, 10).until(
                expected_conditions.presence_of_element_located((By.ID, "login"))
            )
            link_to_login_page.click()

        except:
            print("The page loading was greater than 10 seconds, hence the test was stopped")
            self.browser.quit()

        # Filling the login form

        self.browser.find_element_by_name('username').send_keys('my_username')
        self.browser.find_element_by_name('password').send_keys('new_password+123')

        # Submitting the form to test if the warning about unvalidated account is active, and thus redirect to login

        self.browser.find_element_by_id("button_send").click()

        WebDriverWait(self.browser, 10)

        assert "Bienvenue my_username !" in \
               self.browser.page_source