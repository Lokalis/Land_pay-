TODO: Добавить описание работы теста + необходимые входные данные

Проект написан на Python 3.72 ,использованы следующие библиотеки: 

Allure
pytest
requests
Selenium webdriver

Входные данные для теста : pytest Tests/test_land.py --land-url {url тестируемого ленда} --alluredir=Tests/reports

{Tests/test_land.py} - совершает запуск тестов из данной директории

{--alluredir=Tests/reports} - указывает куда положить json файлы сформированного отчета Allure

Тест кейсы, на основе которых происходит написание автоматизированных тестов находятся в папке Tests/test_case


У проекта есть возможность встройки в Gitlab CI. Все настройки находятся в файле .gitlab-ci.yml и werf.yaml




В тестах присутствует несколько переменных, а именно:

open_page(url) : - url тестируемого ленда.

choice_product(locator): - locator - ключ товара, который хранится в Pages/DB или локатор xpath необходимого продукта

form_input(selector_form,type_pay_test): - selector_form - указание на окружение локатора (начальная точка) формы для введения необходимых 
данных 
-type_pay_test - указание типа необходимой формы   
     
        --selector_form может быть представлен: pay_pop - начало искомой формы находится в попапе 
                                                reg_pop - начало искомой формы находится на регистрационной форме
                                                пустое - искомая форма единственная на странице (по умолчанию)
                                                xpath - указан локатор "начала" необходимой формы
       
        --type_pay_test может быть представлен: lander_form - вызывает "тестовую форму" (shift+лкм по форме)
                                                пустое - применяется обычная форма с ленда (по умолчанию)
                                                
choice_pay_type(pay_type): -pay_type - тип оплаты 
                           
          --pay_type может быть представлен: card_payment - оплата по карте
                                             invoice_payment - выставление счета 

pay_input_form(pay_sis) - pay_sis - тип платежной системы 
    
          --pay_sis может быть  представлен: epos - платежная система Epos
                                             im - платежная система Intellect Money
                                             
                                             
Пример теста:

    def test_land_pay(synergypay,land_url):
        client=synergypay
        url=land_url
        client.open_page(url)
        client.base.form_input("main_reg")
        client.base.choice_product("economy")
        client.base.form_input('pay_pop','')
        client.base.choice_pay_type('card_payment')
        if pay_type!="invoice_payment":
            client.base.pay_input_form('epos')
            
Указанный выше тест совершит следующие действия:
    
    1.Откроет указанную страницу (передается в параметрах, при запуске)
    2.Введет необходимую информацию в "основную форму" на ленде (пример основной формы - http://prntscr.com/ojf5xp)
    3.Выберет продукт "economy" (При переходе в Pages/DB видим, что у ключа 'economy' значение - "//*[@data-package='economy']"
    4.Введет необходимую информацию в попап форму 
    5.Выберет для оплаты - оплата по карте 
    6.Заполнит форму на странице платежной системы 