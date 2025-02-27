from selenium.webdriver.common.by import By

from .framework import (
    selenium_test,
    SeleniumTestCase,
)


class SignOutTestCase(SeleniumTestCase):
    @selenium_test
    def test_sign_out(self):
        email = self._get_random_email()
        self.register(email)
        self.click_masthead_user()
        self.components.masthead.preferences.wait_for_and_click()
        self.components.preferences.sign_out.wait_for_and_click()
        self.components.sign_out.cancel_button.wait_for_and_click()
        assert self.is_logged_in()
        new_email = self.driver.find_element(By.ID, "user-preferences-current-email").text
        self.assertTrue(email == new_email)
        self.components.preferences.sign_out.wait_for_and_click()
        self.components.sign_out.sign_out_button.wait_for_and_click()
        self.sleep_for(self.wait_types.UX_TRANSITION)
        assert not self.is_logged_in()
