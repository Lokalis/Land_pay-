from selenium import webdriver
from Pages.SynergySteps import Advanced
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import allure
from selenium.webdriver.common.action_chains import ActionChains
from sys import platform
import time

class App():

    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument("--window-size=1010,200")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument("--disable-extensions")
        if platform =="win32":
            self.driver = webdriver.Chrome("Application/chromedriver.exe",options=chrome_options)
        elif platform=="linux" or platform=='linux32':
            self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(3)
        self.base=Advanced(self)

    @allure.step("Открыть тестируемую страницу")
    def open_page(self,url):
        self.driver.get(url)

    def destroy(self):
        self.driver.quit()

    def scroll_lazy_load(self,locator):
        """Allows testing land with lazy load. Scrolls to element"""
        action= ActionChains(self.driver)
        element=self.driver.find_element_by_xpath(locator)
        action.move_to_element(element).perform()

    def wait_element_vis(self, locator, timeout=2):
        """Waiting element vision on page"""
        try:
            WebDriverWait(self.driver,timeout).until(EC.presence_of_element_located((By.XPATH,locator)))
        except:
            assert False,f' Unable to locate element => {locator} on this page {self.driver.current_url}'

    def wait_element_click(self,locator,timeout=3):
        """Waiting element clickable on page, with lazy load handler"""
        try:
            WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable((By.XPATH,locator)))
        except:
            try:
                self.scroll_lazy_load(locator)
                WebDriverWait(self.driver, timeout/2).until(EC.element_to_be_clickable((By.XPATH, locator)))
            except:
                assert False,f" Unable to click element => {locator} on this page {self.driver.current_url}"

    def screenshot(self,name):
        self.driver.save_screenshot(f"Tests/reports/screenshots_failed/{name}_{(time.strftime('%d.%m %H:%M:%S',time.gmtime()))}.png")
