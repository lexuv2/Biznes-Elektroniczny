from bs4 import BeautifulSoup
import requests
import json
import os
import re
from urllib.parse import urljoin

base_url = 'https://biferno.pl'
data_dir = 'data'
image_dir = os.path.join(data_dir, 'images')

class Scraper:
    def __init__(self):
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        if not os.path.exists(image_dir):
            os.makedirs(image_dir)
        self.product_count = 0

    def get_page_content(self, url):
        response = requests.get(url, timeout=5)
        content = BeautifulSoup(response.content, "html.parser")

        categories = self.get_categories(content, base_url)
        with open(os.path.join(data_dir, 'data.json'), 'w', encoding='utf-8') as f:
            json.dump(categories, f, ensure_ascii=False, indent=4)

        print(f"Total products saved: {self.product_count}")

    def get_categories(self, content, base_url):
        categories = {}
        category_list = content.find('ul', class_='menu-list large standard')

        if category_list:
            for category in category_list.find_all('li', class_='parent', recursive=False):
                category_name = category.find('a', class_='spanhover').text.strip()
                category_url = urljoin(base_url, category.find('a', class_='spanhover')['href'])
                if "Promocje" in category_name:
                    continue
                elif "więcej" in category_name:
                    continue

                subcategories = self.get_subcategories(category, category_name, base_url)

                categories[category_name] = {
                    "category_url": category_url,
                    "subcategories": subcategories
                }

        return categories

    def get_subcategories(self, category, category_name, base_url):
        subcategories = {}
        submenu_div = category.find('div', class_='submenu level1')

        if submenu_div:
            subcategory_list = submenu_div.find('ul', class_='level1')

            if subcategory_list:
                for subcategory in subcategory_list.find_all('li', recursive=False):
                    subcategory_name = subcategory.find('a').text.strip()
                    subcategory_url = urljoin(base_url, subcategory.find('a')['href'])

                    if category_name.lower() == "włóczki":
                        if "WŁÓCZKI WG GATUNKU" in subcategory_name.upper():
                            yarn_subcategories = self.get_yarn_subcategories(subcategory, base_url)
                            for yarn_subcategory_name, yarn_subcategory_url in yarn_subcategories.items():
                                products = self.get_products(yarn_subcategory_url)
                                subcategories[yarn_subcategory_name] = {
                                    "subcategory_url": yarn_subcategory_url,
                                    "products": products
                                }
                    else:
                        if subcategory_name.lower() == "polecamy na prezent":
                            continue
                        elif subcategory_name.lower() == "karty podarunkowe":
                            continue

                        products = self.get_products(subcategory_url)
                        subcategories[subcategory_name] = {
                            "subcategory_url": subcategory_url,
                            "products": products
                        }

        return subcategories

    def get_yarn_subcategories(self, subcategory, base_url):
        yarn_subcategories = {}
        yarn_subcategories_list = subcategory.find('ul', class_='level2')

        if yarn_subcategories_list:
            for yarn_subcategory in yarn_subcategories_list.find_all('li', recursive=False):
                yarn_subcategory_name = yarn_subcategory.find('a').text.strip()
                yarn_subcategory_url = urljoin(base_url, yarn_subcategory.find('a')['href'])
                yarn_subcategories[yarn_subcategory_name] = yarn_subcategory_url

        return yarn_subcategories

    def get_products(self, subcategory_link):
        products = {}
        page_number = 1
        product_count = 0
        max_products = 50

        while product_count < max_products:
            paginated_link = f"{subcategory_link}/{page_number}"
            print(f"Retrieving page {paginated_link}...")
            try:
                subcategory_content = requests.get(paginated_link, timeout=10)
                if subcategory_content.status_code != 200:
                    print(f"Failed to retrieve page {page_number} for {subcategory_link}")
                    break

                content = BeautifulSoup(subcategory_content.content, "html.parser")
                products_list = content.find('div', class_='products viewphot s-row')

                if not products_list:
                    break

                for product in products_list.find_all('div', class_='product s-grid-3 product-main-wrap'):
                    if product_count >= max_products:
                        break
                    product_url = urljoin(base_url, product.find('a', class_='prodimage')['href'])
                    product_details = self.get_product_details(product_url)
                    if 'product_name' in product_details:
                        products[product_details['product_name']] = product_details
                        self.product_count += 1
                        product_count += 1

                paginator = content.find('ul', class_='paginator')
                if paginator:
                    last_page = paginator.find('li', class_='last')
                    if last_page and not last_page.find('a'):
                        break
                else:
                    break

                page_number += 1
            except requests.RequestException as e:
                print(f"Error retrieving page {page_number} for {subcategory_link}: {e}")
                break

        return products

    def get_product_details(self, product_url):
        try:
            product_content = requests.get(product_url, timeout=10)
            if product_content.status_code != 200:
                print(f"Failed to retrieve product details for {product_url}")
                return {}

            content = BeautifulSoup(product_content.content, "html.parser")
            product_details = {}

            product_name = content.find('h1', class_='name')
            if product_name:
                product_details['product_name'] = product_name.text.strip()
            else:
                print(f"Product name not found for {product_url}")
                return {}

            product_price = content.find('em', class_='main-price')
            if product_price:
                product_details['product_price'] = product_price.text.strip()
            else:
                product_details['product_price'] = "No price available"
            
            product_description_tag = content.find('div', class_='resetcss', itemprop='description')
            product_description = product_description_tag.text.strip() if product_description_tag else "No description available"
            product_details['product_description'] = product_description
            
            other_details = {}

            color_row = content.find('td', class_='name', string='Kolor dominujący')
            if color_row:
                color_value = color_row.find_next_sibling('td', class_='value').text.strip()
                other_details['Kolor'] = color_value

            details_list_tag = content.find('div', class_='resetcss', itemprop='description')
            if details_list_tag:
                details_list = details_list_tag.find_all('li')
                for details in details_list:
                    details_text = details.text.strip()
                    if 'Skład:' in details_text:
                        other_details['Skład'] = details_text.replace('Skład:', '').strip()
                    elif 'Gramatura:' in details_text:
                        other_details['Gramatura'] = details_text.replace('Gramatura:', '').strip()

            product_details['other_qualities'] = other_details

            images = self.get_product_images(content, product_details['product_name'])
            product_details['images'] = images

            return product_details
        
        except requests.RequestException as e:
            print(f"Error retrieving product details for {product_url}: {e}")
            return {}
    
    def get_product_images(self, content, product_name):
        images = []
        li_elements = content.find_all('li', class_='r--l-flex r--l-flex-vcenter')

        if li_elements:
            for index in [0, 1]:
                if index < len(li_elements):
                    li_element = li_elements[index]
                    image_url = li_element.find('a')
                    image_url = urljoin(base_url, image_url['href'])
                    if image_url:
                        local_path = os.path.join(image_dir, self.sanitize_filename(f"{product_name}_{index}.jpg"))
                        self.download_image(image_url, local_path)
                        images.append({
                            "url": image_url,
                            "local_path": local_path
                        })
        else:
            main_image = content.find('div', class_='mainimg productdetailsimgsize row').find('img')
            if main_image:
                image_url = urljoin(base_url, main_image['src'])
                local_path = os.path.join(image_dir, self.sanitize_filename(f"{product_name}_main.jpg"))
                self.download_image(image_url, local_path)
                images.append({
                    "url": image_url,
                    "local_path": local_path
                })

        return images
    
    def sanitize_filename(self, filename):
        return re.sub(r'[\\/*?:"<>|]', "", filename)
    
    def download_image(self, img_url, local_path):
        if not os.path.exists(image_dir):
            os.makedirs(image_dir)
        
        try:
            response = requests.get(img_url, stream=True)
            with open(local_path, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
        except Exception as e:
            print(f"Error downloading image: {img_url}")
            print(e)

if __name__ == '__main__':
    scraper = Scraper()
    scraper.get_page_content(base_url)