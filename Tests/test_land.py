import requests as r
import time
import pytest
from Application.SynergyApp import App

@pytest.mark.parametrize("selector_form,type_pay_test,pay_type,pay_sis",[('pay_pop','','card_payment','epos')])
def test_land_pay(synergypay,selector_form,type_pay_test,land_url,pay_type,pay_sis):
    client=App()
    client.open_page(land_url)
    client.base.form_input("main_reg")
    client.base.choice_product("economy")
    client.base.form_input(selector_form,type_pay_test)
    client.base.choice_pay_type(pay_type)

# ("pay_pop","lander_form",'card_payment','epos'), - для тест-формы ,('pay_pop',"",'invoice_payment','')


