from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions

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

    def test_reset_password(self):
        pass
        # self.assertEqual(len(mail.outbox), 1)
