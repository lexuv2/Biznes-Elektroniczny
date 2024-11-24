import os
import requests
from bs4 import BeautifulSoup
import requests.auth
import warnings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


API_URL = "https://127.0.0.1/api"
API_KEY = "L382DZUQQJBLEU9CF6S6TIEH8HVHYBQJ"

if not API_KEY:
    raise ValueError("Please set the PRESTASHOP_KEY environment variable.")

auth = requests.auth.HTTPBasicAuth(API_KEY, "")

def remove_all_products(products):
    if not products:
            print("No products found.")
    else:
        print(f"Found {len(products)} products:")
        for product in products:
            # print(f"Delieting Product ID: {product['id']}")
            delete_product(product['id'])
            
def get_products():
    response = requests.get(API_URL+"/products", auth=auth, verify=False)
    if response.status_code != 200:
        print(f"Failed to fetch products: {response.status_code} - {response.text}")
        exit(1)
    
    soup = BeautifulSoup(response.content, "xml")
    return soup.find_all("product")

def delete_product(product_id):
    url = f"{API_URL}products/{product_id}"
    response = requests.delete(url, auth=auth, verify=False) 
    # if response.status_code == 200:
    #     print(f"Successfully deleted product with ID {product_id}")
    # else:
    #     print(f"Failed to delete product with ID {product_id}: {response.status_code} - {response.text}")

def remove_all_categories(categories):
    if not categories:
        print("No categories found.")
    else:
        print(f"Found {len(categories)} categories:")
        for category in categories:
            # print(f"Deleting Category ID: {category['id']}")
            if(category['id']=="1" or category['id']=="2"): 
               print("Skip deleting root and home category")
            else:
                delete_category(category['id'])
            
def get_categories():
    response = requests.get(API_URL + "/categories", auth=auth, verify=False)
    if response.status_code != 200:
        print(f"Failed to fetch categories: {response.status_code} - {response.text}")
        exit(1)
    
    soup = BeautifulSoup(response.content, "xml")
    return soup.find_all("category")

def delete_category(category_id):
    url = f"{API_URL}/categories/{category_id}"
    response = requests.delete(url, auth=auth, verify=False) 
    # if response.status_code == 200:
    #     print(f"Successfully deleted category with ID {category_id}")
    # else:
    #     print(f"Failed to delete category with ID {category_id}: {response.status_code} - {response.text}")

def remove_all_product_features(features):
    if not features:
        print("No product features found.")
    else:
        print(f"Found {len(features)} product features:")
        for feature in features:
            delete_product_feature(feature['id'])
            print(f"Deleting Product Feature ID: {feature['id']}")

def get_product_features():
    response = requests.get(API_URL + "/product_features", auth=auth, verify=False)
    if response.status_code != 200:
        print(f"Failed to fetch product features: {response.status_code} - {response.text}")
        exit(1)
    
    soup = BeautifulSoup(response.content, "xml")
    return soup.find_all("product_feature")

def delete_product_feature(feature_id):
    url = f"{API_URL}/product_features/{feature_id}"
    response = requests.delete(url, auth=auth, verify=False)
    # if response.status_code == 200:
    #     print(f"Successfully deleted product feature with ID {feature_id}")
    # else:
    #     print(f"Failed to delete product feature with ID {feature_id}: {response.status_code} - {response.text}")


if __name__ == "__main__": 
    products = get_products()
    remove_all_products(products=products)
    remove_all_categories(get_categories())
    remove_all_product_features(get_product_features())

    
