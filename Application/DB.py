class DB():

    input_data={
        "name":"testабвгдеёждв",
        "email":"dvvolkov@synergy.ru",
        "phone":"+71000000000",


    }
    global_xpath={
        "pay_pop":"//div[@class='popup-tickets__form']",
        "card_payment":"//button[@name='payment-type-online']",
        "invoice_payment":"//button[@name='payment-type-invoice']",
        "name_field":"//input[@name='name']",
        "phone_field":"//input[@name='phone']",
        "email_field":"//input[@name='email']",
        "button_submit":"//*[@type='submit']",
        "reg_pop":"//a[@href='#popup-registration']",
        "main_reg":"//div[@class='main__form ']",
        "lander_form":"//div[@id='lander-form-test-payments']",
        "invoice_name_field":"//input[@name='company']",
        "product_id_field":"//input[@name='product_id']",
        "tickets_count_field":"//input[@name='tickets_count']",
        "promocode_field":"//input[@name='promocode']",
        "test_field":"//input[@name='name']",
        "error_code_payment":"//*[@id='errorcode']",
        "error_text_payment":"//*[@id='errortext']",
    }
    epos_xpath={
        "epos_iframe":"//iframe[@id='secureFrame']",
        "card_number_field": "//input[@name='cardnum0']",
        "card_date_field": "//input[@id='month']",
        "card_holder_field": "//input[@id='card-holder']",
        "submit": "//*[@type='submit']",
        "card_cvv_field": "//input[@id='cvv2']",
    }
    im_xpath={
        "iframe":"//iframe[@class='fancybox-iframe']",
        "card_number_field": "//*[@data-validate='cardNumber']",
        "card_date_field": "//*[@data-validate='date']",
        "card_holder_field": "//*[@data-validate='name']",
        "submit": "//button[@class='button button__submit']",
        "card_cvv_field": "//*[@data-validate='cvc']",
    }
    class_xpath = (global_xpath, epos_xpath)

    product_xpath={
        "economy":"//*[@data-package='economy']"
    }