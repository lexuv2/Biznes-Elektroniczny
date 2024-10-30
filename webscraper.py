from bs4 import BeautifulSoup
import requests
import json
import os
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


    def get_page_content(self, url):
        response = requests.get(url, timeout=5)
        content = BeautifulSoup(response.content, "html.parser")

        categories = self.get_categories(content, base_url)
        #print(json.dumps(categories, indent=4, ensure_ascii=False))

    def get_categories(self, content, base_url):
        categories = []
        category_list = content.find('ul', class_='menu-list large standard')

        if category_list:
            for category in category_list.find_all('li', class_='parent', recursive=False):
                category_name = category.find('a', class_='spanhover').text.strip()
                category_url = urljoin(base_url, category.find('a', class_='spanhover')['href'])
                if "Promocje" in category_name:
                    continue

                subcategories = self.get_subcategories(category, category_name, base_url)

                categories.append({
                    "category_name": category_name,
                    "category_url": category_url,
                    "subcategories": subcategories
                })

        return categories

    def get_subcategories(self, category, category_name, base_url):
        subcategories = []
        submenu_div = category.find('div', class_='submenu level1')

        if submenu_div:
            subcategory_list = submenu_div.find('ul', class_='level1')

            if subcategory_list:
                for subcategory in subcategory_list.find_all('li', recursive=False):
                    subcategory_name = subcategory.find('a').text.strip()
                    subcategory_url = urljoin(base_url, subcategory.find('a')['href'])

                    if category_name.lower() == "włóczki":
                        if "WŁÓCZKI WG GATUNKU" in subcategory_name.upper():
                            yarn_subcategories, yarn_subcategories_url = self.get_yarn_subcategories(subcategory, base_url)
                            subcategories.extend(yarn_subcategories)
                            for url in yarn_subcategories_url:
                                self.get_products(url)
                            

                    else:
                        if subcategory_name.lower() == "polecamy na prezent":
                            continue
                        subcategories.append({
                            "subcategory_name": subcategory_name,
                            "subcategory_url": subcategory_url
                        })
                        #self.get_products(subcategory_url)

        return subcategories

    def get_yarn_subcategories(self, subcategory, base_url):
        yarn_subcategories = []
        yarn_subcategories_urls = []
        yarn_subcategories_list = subcategory.find('ul', class_='level2')

        if yarn_subcategories_list:
            for yarn_subcategory in yarn_subcategories_list.find_all('li', recursive=False):
                yarn_subcategory_name = yarn_subcategory.find('a').text.strip()
                yarn_subcategory_url = urljoin(base_url, yarn_subcategory.find('a')['href'])
                yarn_subcategories_urls.append(yarn_subcategory_url)
                yarn_subcategories.append({
                    "subcategory_name": yarn_subcategory_name,
                    "subcategory_url": yarn_subcategory_url
                })

        return yarn_subcategories, yarn_subcategories_urls

    def get_products(self, subcategory_link):
        subcategory_content = requests.get(subcategory_link, timeout=5)
        content = BeautifulSoup(subcategory_content.content, "html.parser")
        products = []
        products_list = content.find('div', class_='products viewphot s-row')

        if products_list:
            for product in products_list.find_all('div', class_='product s-grid-3 product-main-wrap'):
                product_url = urljoin(base_url, product.find('a', class_='prodimage')['href'])
                product_details = self.get_product_details(product_url)
                products.append(product_details)

        #print(json.dumps(products, indent=4, ensure_ascii=False))

    def get_product_details(self, product_url):
        product_content = requests.get(product_url, timeout=5)
        content = BeautifulSoup(product_content.content, "html.parser")
        product_details = {}

        product_name = product_name = content.find('h1', class_='name').text.strip()
        product_details['product_name'] = product_name
        
        product_price = content.find('em', class_='main-price').text.strip()
        product_details['product_price'] = product_price
        
        product_description = content.find('div', class_='resetcss', itemprop='description').text.strip()
        product_details['product_description'] = product_description
        
        other_details = {}

        color_row = content.find('td', class_='name', string='Kolor dominujący')
        if color_row:
            color_value = color_row.find_next_sibling('td', class_='value').text.strip()
            other_details['Kolor'] = color_value

        details_list = content.find('div', class_='resetcss', itemprop='description').find_all('li')
        for details in details_list:
            details_text = details.text.strip()
            if 'Skład:' in details_text:
                other_details['Skład'] = details_text.replace('Skład:', '').strip()
            elif 'Gramatura:' in details_text:
                other_details['Gramatura'] = details_text.replace('Gramatura:', '').strip()

        product_details['other_qualities'] = other_details

        images = self.get_product_images(content, product_name)
        product_details['images'] = images
        print(json.dumps(product_details, indent=4, ensure_ascii=False))

        return product_details
    
    def get_product_images(self, content, product_name):
        images = []
        image_divs = content.find_all('div', class_='mainimg productdetailsimgsize row')
        for index in [0, 2]:  
            if index < len(image_divs):
                img_tag = image_divs[index].find('img')
                if img_tag and img_tag['src']:
                    img_url = urljoin(base_url, img_tag['src'])
                    alt_text = img_tag.get('alt', product_name).replace(' ', '_')
                    local_path = os.path.join(image_dir, f"{alt_text}_{index}.jpg").replace('\\', '/')
                    self.download_image(img_url, local_path)
                    images.append({
                        "url": img_url,
                        "local_path": local_path
                    })
        return images
    
    def download_image(self, img_url, local_path):
        if not os.path.exists(image_dir):
            os.makedirs(image_dir)
        response = requests.get(img_url, stream=True)
        if response.status_code == 200:
            with open(local_path, 'wb') as file:
                for chunk in response:
                    file.write(chunk)

if __name__ == '__main__':
    scraper = Scraper()
    scraper.get_page_content(base_url)