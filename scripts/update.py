import os
import requests
import requests.auth
import xml.etree.ElementTree as ET
import urllib3
import json
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader

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

URL_CATEGORIES = f'{API_URL}/categories'
URL_PRODUCTS = f'{API_URL}/products'

API_KEY = os.environ.get("PRESTASHOP_KEY") # you can hardcode your api_key 

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
        response = requests.post(API_URL+"/categories", auth=auth, verify=False, data=self.to_xml())
        if response.status_code == 201:
            soup = BeautifulSoup(response.text, 'xml')
            self.id=soup.find('id').text.strip()
            print(f"Successfully created category with ID {self.id}")
        else:
            print(f"Failed to create category with ID {self.id}: {response.status_code} - {response.text}")
   
class Product:
    """
    A class representing a product  in the store.
    """
    template = env.get_template(TEMPLATE_PRODUCT)
    def __init__(self, id: int, name: str, price:any, img_path: str, category: Category, description: str):
        self.id = id
        self.name = name
        self.price = price
        self.img_path = img_path
        self.category = category
        self.descritpion = description

    def to_dict(self):
        """
        Converts the Product object to a dictionary.
        """
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "img_path": self.img_path,
            "category": self.category.id
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
    def send(self):
        response = requests.post(API_URL+"/products", auth=auth, verify=False, data=self.to_xml())
        if response.status_code == 201:
            soup = BeautifulSoup(response.text, 'xml')
            self.id=soup.find('id').text.strip()
            print(f"Successfully created product with ID {self.id}")
        else:
            print(f"Failed to create product with ID {self.id}: {response.status_code} - {response.text}")        

class Product_feature:
    """
    A class representing products feature.
    """
    def __init__(self, id: int , name: str):
        self.id = id
        self.name = name

class Product_featur_value:
    """
    A class representig value of product feature
    """
    def __init__(self, id: int , value: str, feature: Product_feature):
        self.id = id
        self.value = value
        self.featue = feature

def create(data): 
    """
    Creates a tree structure of categories, subcategories and products with features.
    """
    categories = []
    for category_name, category_data in data.items():
        category = Category(id=-1, id_parent=2, name=category_name)
        # category.send()
        categories.append(category)

        for sub_category_name, sub_category_data in category_data.get('subcategories', {}).items():
            sub_category = Category(id=len(categories)+3, id_parent=category.id, name=sub_category_name)
            # sub_category.send()
            categories.append(sub_category)
            for product_name, products_data in sub_category_data.get('products', {}).items():
                print(product_name)
                create_products_for_category(category=sub_category, products=products_data)
    

def create_products_for_category(category: Category, products):
    """
    products jest obiektem przechowującym wszystkie dane trzeba sparsowac, na podstawie "images" wyciagnac z niego sciezke img oraz na podstawie "other_qualities" tworzyć product_features (trzeba sprawdzić czy juz nie zostaly wczesniej takie stworzone product_features i product_feature_values)
    """
    product = Product(id=-1, name=products['product_name'], price=products['product_name'], img_path="", category=category, description=products['product_description'])
    print(product.to_json())
    


if __name__ == "__main__": 
    with open('../data/data.json', 'r',encoding='utf-8') as file:
        data = json.load(file)

    # formatted_data = format_json_with_depth(data, max_depth=6)
    # print(json.dumps(formatted_data, indent=4, ensure_ascii=False))
    
    categories = create(data)        



