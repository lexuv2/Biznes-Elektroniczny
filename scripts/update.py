import os
import requests
import requests.auth
import xml.etree.ElementTree as ET
import urllib3
import json
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader
import random
from pathlib import Path


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

"""
Wymagania: 

 -> Część produktów ma być niedostępna. Stany magazynowe proszę ustawić tak, aby liczba dostępnych produktów każdego rodzaju nie przekraczała 10 szt. 
 -> Nazwy, opisy, zdjęcia, ceny i podatki określone dla każdego produktu muszą odpowiadać rzeczywistym danym pobranym ze sklepu źródłowego. Polskie znaki muszą się prawidłowo wyświetlać.
 -> W sklepie zarejestrowano conajmniej 4 kategorie i w każdej z nich conajmniej 2 podkategorie. Żadna z podkategorii nie może być pusta.
"""

API_URL = "https://127.0.0.1/api"


TEMPLATE_DIR = "./xml_templates/"
TEAMPLATE_CATEOGRY = 'category.xml'
TEMPLATE_PRODUCT = 'product.xml'
TEMPLATE_PRODUCT_FEAUTRE = 'product_feature.xml'
TEMPLATE_PRODUCT_FEATURE_VALUE = 'product_feature_value.xml'
TEMPLATE_STOCK = 'stock.xml'

URL_CATEGORIES = f'{API_URL}/categories'
URL_PRODUCTS = f'{API_URL}/products'

API_KEY = os.environ.get("PRESTASHOP_KEY") # you can hardcode your api_key 
API_KEY = "4JUYGWQ4HJ5IEXCFG9GAQIQ5PIQSNSE2"

env = Environment(loader=FileSystemLoader(TEMPLATE_DIR), autoescape=True)
auth = requests.auth.HTTPBasicAuth(API_KEY, "")

def format_json_with_depth(data, max_depth, current_depth=0):
    if current_depth >= max_depth:
        return "..."
    
    if isinstance(data, dict):
        return {key: format_json_with_depth(value, max_depth, current_depth + 1) for key, value in data.items()}
    
    if isinstance(data, list):
        return [format_json_with_depth(item, max_depth, current_depth + 1) for item in data]
    
    return data  

class Category:
    """
    A class representing a category or subcategory in the store.
    """
    template = env.get_template(TEAMPLATE_CATEOGRY)

    def __init__(self, id: int, id_parent: int, name: str):
        self.id = id
        self.id_parent = id_parent
        self.name = name

    def to_dict(self):
        """
        Converts the Category object to a dictionary.
        """
        return {
            "id": self.id,
            "id_parent": self.id_parent,
            "name": self.name
        }

    def to_json(self):
        """
        Converts the Category object to a JSON string.
        """
        return json.dumps(self.to_dict(), ensure_ascii=False)
    
    def to_xml(self):
            """
            Generates XML for the category using the Jinja2 template.
            """
            category_data = self.to_dict()  # Get category data as dictionary
            return Category.template.render(category=category_data) 
    
    def send(self):
        response = requests.post(API_URL+"/categories", auth=auth, verify=False, data=self.to_xml().encode('utf-8'))
        if response.status_code == 201:
            soup = BeautifulSoup(response.text, 'xml')
            self.id=soup.find('id').text.strip()
            # print(f"Successfully created category with ID {self.id}")
        else:
            print(f"Failed to create category with ID {self.id}: {response.status_code} - {response.text}")
   
class Product:
    """
    A class representing a product  in the store.
    """
    template = env.get_template(TEMPLATE_PRODUCT)
    def __init__(self, id: int, name: str, price:any, img_path: list, category: Category, description: str, product_feature_id:int,product_feature_value_id: int):
        self.id = id
        self.name = name
        self.price = float(price.replace('\xa0zł', '').replace(',', '.'))
        self.img_path = img_path
        self.category = category
        self.descritpion = description
        self.product_feature_id = product_feature_id
        self.product_feature_value_id = product_feature_value_id,

    def to_dict(self):
        """
        Converts the Product object to a dictionary.
        """
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "img_path": self.img_path,
            "category": self.category.id,
            "descritpion": self.descritpion,
            "product_feature_id": self.product_feature_id,
            "product_feature_value_id": self.product_feature_value_id
        }
    def to_json(self):
        """
        Converts the Product object to a JSON string.
        """
        return json.dumps(self.to_dict(), ensure_ascii=False)
    def to_xml(self):
        """
        Generates XML for the product using the Jinja2 template.
        """
        product_data = self.to_dict()
        return Product.template.render(product=product_data)
    

    def set_image(self):
        """
        Uploads images for the product to the API.
        """
        for img in self.img_path:
            # Upewnij się, że ścieżka do obrazu jest zgodna z systemem plików
            image_path = img.replace("\\", "/")  # Popraw dla systemów Windows/MacOS
            if not os.path.isfile(image_path):
                print(f"Image file {image_path} not found.")
                continue
            
            # Otwórz plik obrazu w trybie binarnym
            with open(image_path, 'rb') as img_file:
                files = {
                    'image': (os.path.basename(image_path), img_file, 'image/jpg')
                }

                
                # Wysłanie żądania POST do API w celu załadowania obrazu
                response = requests.post(
                    f"{API_URL}/images/products/{self.id}",
                    auth=auth,
                    files=files,
                    verify=False
                )

                # # Obsługa odpowiedzi
                # if response.status_code == 200:
                #     print(f"Successfully uploaded image for product {self.name}")
                # else:
                #     print(f"Failed to upload image for product {self.name}: {response.status_code} - {response.text}")

    def send(self):
        response = requests.post(API_URL+"/products", auth=auth, verify=False, data=self.to_xml().encode('utf-8'))
        if response.status_code == 201:
            soup = BeautifulSoup(response.text, 'xml')
            self.id=soup.find('id').text.strip()
            # print(f"Successfully created product with ID {self.id}")
        else:
            print(self.to_xml())
            # print(self.to_dict())
            print(f"Failed to create product with ID {self.id}: {response.status_code} - {response.text}")        

class Product_feature:
    template = env.get_template(TEMPLATE_PRODUCT_FEAUTRE)

    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }

    def to_json(self):
        return json.dumps(self.to_dict(), ensure_ascii=False)

    def to_xml(self):
        product_feature_data = self.to_dict()
        return Product_feature.template.render(product_feature=product_feature_data)

    def send(self):
        response = requests.post(API_URL + "/product_features", auth=auth, verify=False, data=self.to_xml().encode('utf-8'))
        if response.status_code == 201:
            soup = BeautifulSoup(response.text, 'xml')
            self.id = soup.find('id').text.strip()
            # print(f"Successfully created product feature with ID {self.id}")
        else:
            print(f"Failed to create product feature with ID {self.id}: {response.status_code} - {response.text}")

class Product_featur_value:
    template = env.get_template(TEMPLATE_PRODUCT_FEATURE_VALUE)

    def __init__(self, id: int, value: str, product_feature: Product_feature):
        self.id = id
        self.value = value
        self.product_feature = product_feature

    def to_dict(self):
        return {
            "id": self.id,
            "value": self.value,
            "product_feature": self.product_feature.id
        }

    def to_json(self):
        return json.dumps(self.to_dict(), ensure_ascii=False)

    def to_xml(self):
        product_feature_value_data = self.to_dict()
        return Product_featur_value.template.render(product_feature_value=product_feature_value_data)

    def send(self):
        response = requests.post(API_URL + "/product_feature_values", auth=auth, verify=False, data=self.to_xml().encode('utf-8'))
        if response.status_code == 201:
            soup = BeautifulSoup(response.text, 'xml')
            self.id = soup.find('id').text.strip()
            # print(f"Successfully created product feature value with ID {self.id}")
        else:
            print(f"Failed to create product feature value with ID {self.id}: {response.status_code} - {response.text}")

class Stock:
    template = env.get_template(TEMPLATE_STOCK)

    def __init__(self, id: int, product: Product, quantity: int):
        self.id = id
        self.product = product
        self.quantity = quantity

    def to_dict(self):
        """
        Converts the Stock object to a dictionary.
        """
        return {
            "id": self.id,
            "product": self.product.id,
            "quantity": self.quantity
        }

    def to_json(self):
        """
        Converts the Stock object to a JSON string.
        """
        return json.dumps(self.to_dict(), ensure_ascii=False)

    def to_xml(self):
        """
        Generates XML for the stock using the Jinja2 template.
        """
        stock_data = self.to_dict()
        return Stock.template.render(stock=stock_data)

    def update_quantity(self, new_quantity: int):
        """
        Updates the stock quantity.
        """
        self.quantity = new_quantity
        response = requests.put(API_URL + f"/stock_availables/{self.id}", auth=auth, verify=False, data=self.to_xml().encode('utf-8'))
        # if response.status_code == 200:
        #     print(f"Successfully updated stock quantity for ID {self.id} to {self.quantity}")
        # else:
        #     print(f"Failed to update stock quantity for ID {self.id}: {response.status_code} - {response.text}")  
    
def create(data): 
    """
    Creates a tree structure of categories, subcategories and products with features.
    """
    categories = []
    products = []
    product_features = []
    product_feature_values = []
    for category_name, category_data in data.items():
        category = Category(id=-1, id_parent=2, name=category_name)
        category.send()
        categories.append(category)
       
        for sub_category_name, sub_category_data in category_data.get('subcategories', {}).items():
            sub_category = Category(id=len(categories)+3, id_parent=category.id, name=sub_category_name)
            sub_category.send()
            categories.append(sub_category)

            for product_name, products_data in sub_category_data.get('products', {}).items():
                img = []
                for image in products_data['images']:
                    img.append("../"+image['local_path'])

                product = Product(id=1, name=product_name, price=products_data['product_price'], img_path=img, category=sub_category, description=products_data['product_description'],product_feature_id=0, product_feature_value_id=0)

              
                for name_quality, qualities_data in products_data.get('other_qualities',{}).items():
                    product_feature = next((pf for pf in product_features if pf.name == name_quality), None)
                    
                    if not product_feature:
                        product_feature = Product_feature(id=1, name=name_quality)
                        product_feature.send()
                        product_features.append(product_feature)  # Add to the list

                    product_feature_value = next((pfv for pfv in product_feature_values 
                                                 if pfv.value == qualities_data), None)
                    
                    if not product_feature_value:
                        product_feature_value = Product_featur_value(id=1, value=qualities_data, product_feature=product_feature)
                        product_feature_value.send()
                        product_feature_values.append(product_feature_value)  
                product.product_feature_id = product_feature.id
                product.product_feature_value_id = product_feature_value.id
                product.send()
                products.append(product)
                product.set_image()
    return products

def get_stock_xml(product_id: int):
        return requests.get(f"http://127.0.0.1/api/stock_availables?filter[id_product]={product_id}&display=full", auth=auth, verify=False).text

def set_stocks(products):
    for product in products:
        stock_xml = get_stock_xml(product_id=product.id)
        root = ET.fromstring(stock_xml)
        stock_id = int(root.find("stock_availables/stock_available/id").text)

        if not stock_id:
            print(f"Stock not found for product ID {product.id}")
            continue
        # print(stock_id)

        weights = [0.05] + [0.095] * 10
        stock_quantity = random.choices(range(11), weights=weights, k=1)[0]  
        stock = Stock(id=stock_id, product=product, quantity=stock_quantity)
        # print(stock.to_xml())
        # print(stock_quantity)
        stock.update_quantity(new_quantity=stock_quantity)


def remove_80_percent_products(data):
    for category, category_data in data.items():
        subcategories = category_data.get('subcategories', {})
        for subcategory, subcategory_data in subcategories.items():
            products = subcategory_data.get('products', {})
            product_keys = list(products.keys())
            
            # Oblicz ile produktów zostawić (20%)
            num_to_keep = int(len(product_keys) * 0.05)
            
            # Wybierz losowe produkty, które zostaną (20% pierwszych produktów)
            products_to_keep = random.sample(product_keys, num_to_keep)
            
            # Usuń produkty, które nie zostały wybrane
            for product_key in product_keys:
                if product_key not in products_to_keep:
                    del products[product_key]
            
            # Zaktualizuj produkty w podkategorii
            subcategory_data['products'] = products

    return data

if __name__ == "__main__": 
 # Otwieramy plik w trybie odczytu
    with open('../data/data.json', 'r', encoding='utf-8') as file:
        # Ładujemy dane JSON
        data = json.load(file)

    # updated_data = remove_80_percent_products(data)

    # # Zapisz zmodyfikowane dane do nowego pliku JSON
    # with open('../data/data_reduced.json', 'w', encoding='utf-8') as file:
    #     json.dump(updated_data, file, ensure_ascii=False, indent=4)

    
    created_products = create(data)    
    set_stocks(created_products)    


