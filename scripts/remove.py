import os
import requests
from bs4 import BeautifulSoup
import requests.auth
import warnings
import urllib3
from concurrent.futures import ThreadPoolExecutor

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
        with ThreadPoolExecutor(max_workers=10) as executor:
            # Submit delete tasks concurrently
            for product in products:
                executor.submit(delete_product, product['id'])

def get_products():
    response = requests.get(API_URL + "/products", auth=auth, verify=False)
    if response.status_code != 200:
        print(f"Failed to fetch products: {response.status_code} - {response.text}")
        exit(1)
    
    soup = BeautifulSoup(response.content, "xml")
    return soup.find_all("product")

def delete_product(product_id):
    url = f"{API_URL}/products/{product_id}"
    response = requests.delete(url, auth=auth, verify=False) 
    # Uncomment to log the results of the deletion attempt
    # if response.status_code == 200:
    #     print(f"Successfully deleted product with ID {product_id}")
    # else:
    #     print(f"Failed to delete product with ID {product_id}: {response.status_code} - {response.text}")

def remove_all_categories(categories):
    if not categories:
        print("No categories found.")
    else:
        print(f"Found {len(categories)} categories:")
        with ThreadPoolExecutor(max_workers=10) as executor:
            # Submit delete tasks concurrently, skipping root and home categories
            for category in categories:
                if category['id'] == "1" or category['id'] == "2":
                    print("Skipping root and home category")
                else:
                    executor.submit(delete_category, category['id'])

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
    # Uncomment to log the results of the deletion attempt
    # if response.status_code == 200:
    #     print(f"Successfully deleted category with ID {category_id}")
    # else:
    #     print(f"Failed to delete category with ID {category_id}: {response.status_code} - {response.text}")

def remove_all_product_features(features):
    if not features:
        print("No product features found.")
    else:
        print(f"Found {len(features)} product features:")
        with ThreadPoolExecutor(max_workers=10) as executor:
            # Submit delete tasks concurrently
            for feature in features:
                executor.submit(delete_product_feature, feature['id'])

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
    # Uncomment to log the results of the deletion attempt
    # if response.status_code == 200:
    #     print(f"Successfully deleted product feature with ID {feature_id}")
    # else:
    #     print(f"Failed to delete product feature with ID {feature_id}: {response.status_code} - {response.text}")

if __name__ == "__main__":
    products = get_products()
    categories = get_categories()
    features = get_product_features()

    # Use ThreadPoolExecutor to run the cleanup functions concurrently
    with ThreadPoolExecutor(max_workers=3) as executor:
        executor.submit(remove_all_products, products)
        executor.submit(remove_all_categories, categories)
        executor.submit(remove_all_product_features, features)
