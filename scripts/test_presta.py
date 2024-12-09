import pytest 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import faker
from selenium.webdriver.chrome.options import Options
import random
import time

DEFAULT_WAIT_TIME = 1


faker = faker.Faker()



def create_account(driver: webdriver.Firefox,name,surname):
    driver.get("https://localhost")
    print(driver.title) 
    driver.implicitly_wait(10)
    ## find by title "Zaloguj się do swojego konta klienta"
    log_in_button = driver.find_element(by=By.XPATH, value="/html/body/main/header/nav/div/div/div[1]/div[2]/div[2]/div/a")
    log_in_button.click()
    driver.implicitly_wait(DEFAULT_WAIT_TIME)
    no_account_button = driver.find_element(by=By.XPATH, value='/html/body/main/section/div/div/section/div/div/a')
    # no_account_link = no_account_div.find_element(by=By.TAG_NAME, value="a")
    no_account_button.click()

    gender_button = driver.find_element(by=By.XPATH, value='//*[@id="field-id_gender-1"]')
    gender_button.click()

    first_name_input = driver.find_element(by=By.XPATH, value='//*[@id="field-firstname"]')
    first_name_input.send_keys(name)

    surname_input = driver.find_element(by=By.XPATH, value='//*[@id="field-lastname"]')
    surname_input.send_keys(surname)

    email_input = driver.find_element(by=By.XPATH, value='//*[@id="field-email"]')
    email_input.send_keys(faker.email())

    password_input = driver.find_element(by=By.XPATH, value='//*[@id="field-password"]')
    password_input.send_keys("test123")

    accept_privacy_policy = driver.find_element(by=By.XPATH, value='/html/body/main/section/div/div/section/div/section/form/div/div[10]/div[1]/span/label/input')
    accept_privacy_policy.click()

    tos_checkbox = driver.find_element(by=By.XPATH, value='/html/body/main/section/div/div/section/div/section/form/div/div[8]/div[1]/span/label/input')
    tos_checkbox.click()

    sign_up_button = driver.find_element(by=By.XPATH, value='/html/body/main/section/div/div/section/div/section/form/footer/button')
    sign_up_button.click()

    driver.implicitly_wait(DEFAULT_WAIT_TIME)

    url = driver.current_url
    # assert url == "https://127.0.0.1/"

    account_name = driver.find_element(by=By.XPATH, value='/html/body/main/header/nav/div/div/div[1]/div[2]/div[2]/div/a[2]/span')
    return account_name.text




def get_categories(driver: webdriver.Firefox):
    driver.get("https://localhost")
    driver.implicitly_wait(10)
    categories_raw = driver.find_elements(by=By.CLASS_NAME, value="category")
    categories = [category for category in categories_raw if category.accessible_name != ""]
    return categories

def get_products(driver: webdriver.Firefox):
    products_row = driver.find_element(by=By.XPATH, value='/html/body/main/section/div/div[2]/section/section/div[3]/div[1]')
    ### all children of products row are products
    products = products_row.find_elements(by=By.TAG_NAME, value="article")
    return products
    

def add_products_to_cart(driver: webdriver,n_products=2,n_categories=2):
    for i in range(n_categories):
        for j in range(n_products):
            categories = get_categories(driver)
            categories[i].click()
            driver.implicitly_wait(DEFAULT_WAIT_TIME)
            products = get_products(driver)
            products[j].click()
            # driver.implicitly_wait(DEFAULT_WAIT_TIME)
            # WebDriverWait(driver, 10).until(lambda driver: driver.find_element(by=By.XPATH, value='/html/body/main/section/div/div/section/div[1]/div[2]/div[2]/div[2]/form/div[2]/div/div[1]/div/span[3]/button[1]'))
            # set load strategy to eager


            add_multiple_button = driver.find_element(by=By.XPATH, value='/html/body/main/section/div/div/section/div[1]/div[2]/div[2]/div[2]/form/div[2]/div/div[1]/div/span[3]/button[1]')
            add_less = driver.find_element(by=By.XPATH, value='/html/body/main/section/div/div/section/div[1]/div[2]/div[2]/div[2]/form/div[2]/div/div[1]/div/span[3]/button[2]')
            it = 0
            for k in range(random.randint(1,10)):
                add_multiple_button.click()
                too_much = 0
                # find text: Nie ma wystarczającej ilości produktów w magazynie
                try:
                    time.sleep(0.05)
                    too_much = driver.find_element(by=By.XPATH, value='//*[@id="product-availability"]')
                except:
                    pass
                
                if too_much:
                    if "brak" in too_much.text or "niedostępny" in too_much.text or "wystarczającej" in too_much.text or "dostępny" in too_much.text or "ilości" in too_much.text:
                        add_less.click()
                        break
                it += 1
            if it > 0:
                add_to_cart_button = driver.find_element(by=By.XPATH, value='/html/body/main/section/div/div/section/div[1]/div[2]/div[2]/div[2]/form/div[2]/div/div[2]/button')
                add_to_cart_button.click()


    
def test_delete_from_cart(driver,n_delete=1):
    # add_products_to_cart(driver,n_delete+1,1)
    driver.get("https://localhost")
    driver.implicitly_wait(10)
    cart_button = driver.find_element(by=By.XPATH, value='/html/body/main/header/nav/div/div/div[1]/div[2]/div[3]/div/div/a')
    cart_button.click()
    for i in range(n_delete):
        # delete_button = driver.find_element(by=By.CLASS_NAME, value
        time.sleep(1)
        driver.implicitly_wait(DEFAULT_WAIT_TIME)
        delete_buttons = driver.find_elements(by=By.LINK_TEXT, value="delete")
        delete_buttons[0].click()
    
    # for i in range(n_delete):
    #     delete_buttons[i].click()
    #     # driver.implicitly_wait(DEFAULT_WAIT_TIME)
    return






def test_create_account():
    name = faker.first_name()
    surname = faker.last_name()
    driver = webdriver.Firefox()
    acc_name = create_account(driver,name, surname)
    assert acc_name == name + " " + surname


    

def order_products(driver):
    # create_account(driver,"test","test")
    # add_products_to_cart(driver,2,2)
    driver.get("https://localhost")
    cart_button = driver.find_element(by=By.XPATH, value='/html/body/main/header/nav/div/div/div[1]/div[2]/div[3]/div/div/a')
    cart_button.click()
    driver.implicitly_wait(DEFAULT_WAIT_TIME)


    ### delete not avaliable products 
    try:
        while True:
            time.sleep(2)
            not_avaliable_text = driver.find_element(by=By.XPATH, value='/html/body/main/section/aside/div/article/ul/li')
            if "wybierzesz" in not_avaliable_text.text:
                ## find text betwen "Produkt" and "w Twoim koszyku"
                product_name = not_avaliable_text.text.split("Produkt")[1].split("w Twoim koszyku")[0]
                product_name = product_name.strip()
                # print(product_name)
                all_producs = driver.find_elements(by=By.CLASS_NAME, value="cart-item")
                for product in all_producs:
                    # print(product.text.split("\n"))
                    # print(product_name)
                    if product_name in product.text.split("\n"):
                        delete_button = product.find_element(by=By.CLASS_NAME, value="remove-from-cart")
                        delete_button.click()
                        # print("deleting:  " + product_name)
                        break
            else:
                break

        
    except:
        pass




    relize_order_button = driver.find_element(by=By.XPATH, value='/html/body/main/section/div/div/section/div/div[2]/div[1]/div[2]/div/a')
    relize_order_button.click()

    addres_input = driver.find_element(by=By.XPATH, value='//*[@id="field-address1"]')
    addres_input.send_keys(faker.street_address())

    postal_code = driver.find_element(by=By.XPATH, value='//*[@id="field-postcode"]')
    pl_postal_code = "00-000"
    postal_code.send_keys(pl_postal_code)

    city_input = driver.find_element(by=By.XPATH, value='//*[@id="field-city"]')
    city_input.send_keys(faker.city())

    next_button = driver.find_element(by=By.XPATH, value='/html/body/main/section/div/div/section/div/div[1]/section[2]/div/div/form/div/div/footer/button')
    next_button.click()

    delivery_button = driver.find_element(by=By.XPATH, value='//*[@id="delivery_option_6"]')
    delivery_button.click()
    
    next_button = driver.find_element(by=By.XPATH, value='/html/body/main/section/div/div/section/div/div[1]/section[3]/div/div[2]/form/button')
    next_button.click()

    tos_button = driver.find_element(by=By.XPATH, value='//*[@id="conditions_to_approve[terms-and-conditions]"]')
    tos_button.click()

    bank_wire_button = driver.find_element(by=By.XPATH, value='//*[@id="payment-option-2"]')
    bank_wire_button.click()

    place_order_button = driver.find_element(by=By.XPATH, value='/html/body/main/section/div/div/section/div/div[1]/section[4]/div/div[3]/div[1]/button')
    place_order_button.click()

    # driver.implicitly_wait(DEFAULT_WAIT_TIME)
    # download_invoice_button = driver.find_element(by=By.XPATH, value='/html/body/main/section/div/div/section/section[1]/div/div/div/p/a')
    # download_invoice_button.click()

    
def cehck_order_status(driver):
    driver.get("https://127.0.0.1/moje-konto")
    driver.implicitly_wait(DEFAULT_WAIT_TIME)
    # my_account_button = driver.find_element(by=By.XPATH, value='/html/body/main/header/nav/div/div/div[1]/div[2]/div[3]/div/a[2]')
    # my_account_button.click()
    driver.implicitly_wait(DEFAULT_WAIT_TIME)
    order_history_button = driver.find_element(by=By.XPATH, value='//*[@id="history-link"]')
    order_history_button.click()
    driver.implicitly_wait(DEFAULT_WAIT_TIME)
    download_invoice_button = driver.find_element(by=By.XPATH, value='/html/body/main/section/div/div/section/section/table/tbody/tr/td[5]/a')
    download_invoice_button.click()
    driver.implicitly_wait(DEFAULT_WAIT_TIME)



def add_to_cart_by_name(driver,name):
    driver.get("https://localhost")
    driver.implicitly_wait(10)
    search_input = driver.find_element(by=By.XPATH, value='/html/body/main/header/div[2]/div/div[1]/div[2]/div[2]/form/input[2]')
    search_input.send_keys(name)
    search_input.send_keys(Keys.RETURN)
    driver.implicitly_wait(DEFAULT_WAIT_TIME)
    porducts_row = driver.find_element(by=By.XPATH, value='/html/body/main/section/div/div/section/section/div[3]/div[1]')
    products = porducts_row.find_elements(by=By.TAG_NAME, value="article")
    random.choice(products).click()
    add_to_cart_button = driver.find_element(by=By.XPATH, value='/html/body/main/section/div/div/section/div[1]/div[2]/div[2]/div[2]/form/div[2]/div/div[2]/button')
    add_to_cart_button.click()

def check_order_details(driver):
    driver.get("https://localhost")
    driver.implicitly_wait(DEFAULT_WAIT_TIME)

    my_account_button = driver.find_element(by=By.XPATH, value='/html/body/main/header/nav/div/div/div[1]/div[2]/div[2]/div/a[2]')
    my_account_button.click()
    driver.implicitly_wait(DEFAULT_WAIT_TIME)

    details_button = driver.find_element(by=By.XPATH, value='//*[@id="history-link"]')
    details_button.click()
    driver.implicitly_wait(DEFAULT_WAIT_TIME)

    order_details_button = driver.find_element(by=By.XPATH, value='/html/body/main/section/div/div/section/section/table/tbody/tr/td[6]/a[1]')
    
    order_details_button.click()
    driver.implicitly_wait(DEFAULT_WAIT_TIME)

    
    return


Options = webdriver.FirefoxOptions()
Options.page_load_strategy = 'eager'
driver = webdriver.Firefox(options=Options)

print("create account")
create_account(driver,"test","test")
# order_products(driver)

print("add 10 to cart")
add_products_to_cart(driver,10,2)

print("add to cart by name")
add_to_cart_by_name(driver,"print")


print("delete from cart")
test_delete_from_cart(driver,3)

print ("order products")
order_products(driver)

print   ("check order status")
cehck_order_status(driver)




### TODO: wybor metody płatności przy odbiorze, wybor przewoźnikow, faktura vat