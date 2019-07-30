from Application.DB import DB
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import allure

class Base(DB):

    def __init__(self,app):
        """Init webdriver"""
        self.app=app
        self.driver=self.app.driver

    def pay_init_test_form(self,selector):
        """Init test_form on page
        With ActionChains we may unite some keywords in sequence"""
        self.app.wait_element_click(selector)
        element=self.driver.find_element_by_xpath(selector)
        action=ActionChains(self.driver)
        action.key_down(Keys.LEFT_SHIFT)
        action.click(element)
        action.key_up(Keys.LEFT_SHIFT)
        action.perform()

    def type_words(self,selector,word):
        """Enter words in form on page"""
        self.app.wait_element_vis(selector)
        self.driver.find_element_by_xpath(selector).send_keys(word)

    def next_window(self):
        """Go to next window"""
        self.driver.switch_to.window(self.driver.window_handles[1])

    def click_element(self,element):
        """Find and click on element
          Если указывается элемент-ключ, который присутствует в DB  - значение xpath берется из DB, иначе - просто ищется элемент"""
        for xpath in self.class_xpath:
            if element in xpath:
                element=xpath[element]
        self.app.wait_element_vis(element,timeout=5)
        self.app.wait_element_click(element)
        self.driver.find_element_by_xpath(element).click()

    def handler_form(self, selector_form,type_pay_test):
        """Handler for form_input"""
        if selector_form=="reg_pop":
            self.click_element(selector_form)
        if selector_form in self.global_xpath:
            selector_form=self.global_xpath[selector_form]
        if type_pay_test == "lander_form":
            self.pay_init_test_form(selector_form+self.global_xpath["test_field"])
            selector_form=self.global_xpath[type_pay_test]
        self.app.wait_element_vis(selector_form + self.global_xpath["test_field"])
        self.app.wait_element_click(selector_form + self.global_xpath["test_field"])
        self.cleaner_form(selector_form)
        return selector_form


    def cleaner_form(self,selector_form):
        """Clean fields name, email and phone"""
        for field in ("name_field","email_field","phone_field"):
            element=(selector_form +self.global_xpath[field])
            self.app.wait_element_vis(element)
            self.driver.find_element_by_xpath(element).clear()

    def assert_exist(self,*args):
        """Assert that element exist on page. Can take list elements
        If at least one element not exist - raise AssertionError and print bad selectors"""
        not_exist=[]
        for item in args:
            element=self.driver.find_elements_by_xpath(item) # Ищется сразу список элементов по данному селектору
            if len(element)==0:
                not_exist.append(item)
        if len(not_exist)>0:
            print((f' Данные элементы отсутствуют на странице: {not_exist}'))
        return not_exist

class Advanced(Base,DB):

    def __init__(self,app):
        self.app=app
        self.driver=self.app.driver

    @allure.step("Ввести данные в форму регистрации")
    def form_input(self, selector_form='', type_pay_test=''):
        """Filling in forms
        Если указывается элемент-ключ, который присутствует в DB - значение selector_form берется из DB, иначе - просто
        ищется на странице"""
        selector_form = self.handler_form(selector_form, type_pay_test)
        self.type_words(selector_form + self.global_xpath["name_field"], self.input_data["name"])
        self.type_words(selector_form + self.global_xpath["email_field"], self.input_data["email"])
        self.type_words(selector_form + self.global_xpath["phone_field"], self.input_data["phone"])
        if type_pay_test == "lander_form":
            self.type_words(selector_form + self.global_xpath["product_id_field"],
                            self.input_data["synergy_TEST_global_product"])
            self.click_element(selector_form + "//button")
        elif type_pay_test == "promocode":
            self.type_words(self.global_xpath["promocode_field"], self.input_data["promocode"])
        else:
            self.click_element(selector_form + self.global_xpath["button_submit"])

    @allure.step(f"Выбрать продукт")
    def choice_product(self,selector):
        if selector in self.product_xpath:
            selector=self.product_xpath[selector]
        self.click_element(selector)
        # self.click_element("//button[@class='form__button button button_red']") #----------------КОСТЫЛЬ!!!!!!!!!!!!!!

    @allure.step(f'Ввести данные в форму платежной системы')
    def pay_input_form(self,pay_sis=None):
        """
        Filling in pay forms. Now (in the test) there are only 2 options - IM and EPos
        TODO: The choice of payment system of bitrix, Убрать костыль 'time.sleep(10)'!!!!!!!!!!!!!!!!!!!!!!!!!
        """
        if len(self.driver.window_handles)>1:
            self.next_window()
        if pay_sis=="im":
            path=self.im_xpath
            self.driver.switch_to.frame(self.driver.find_element_by_xpath(path["iframe"]))
        elif pay_sis == 'epos':
            path=self.epos_xpath
            time.sleep(10)
            try:
                self.driver.switch_to.frame(self.driver.find_element_by_xpath(self.epos_xpath["epos_iframe"]))
            except:
                pass
        self.handler_pay_error()
        self.app.wait_element_vis(path["card_number_field"],timeout=10)
        self.type_words(path["card_number_field"], self.input_data["card_number"])
        self.type_words(path["card_date_field"], self.input_data["card_date"])
        self.type_words(path["card_holder_field"], self.input_data["card_holder"])
        self.type_words(path["card_cvv_field"], self.input_data["card_cvv"])
        self.click_element(path["submit"])
        self.driver.switch_to.default_content()

    @allure.step(f"Выбрать тип платежа")
    def choice_pay_type(self,type):
        time.sleep(1)
        self.click_element(self.global_xpath[type])
        time.sleep(1)
        if type=="invoice_payment":
            self.type_words(self.global_xpath["invoice_name_field"],self.input_data["name"])
            self.driver.find_element_by_xpath(self.global_xpath["invoice_name_field"]).submit()
            self.app.destroy()

    def handler_pay_error(self):
        if len(self.driver.find_elements_by_xpath(self.global_xpath["error_code_payment"]))!=0:
            self.driver.save_screenshot(f"Tests/reports/{self.global_xpath['error_code_payment']}.png")
            assert False,f'Found payment error => {self.driver.find_element_by_xpath(self.global_xpath["error_code_payment"]).text} ' \
                f'{self.driver.find_element_by_xpath(self.global_xpath["error_text_payment"]).text}'