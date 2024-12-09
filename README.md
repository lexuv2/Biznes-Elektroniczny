# Yarn Shop "Włóczki3" Implementation based on PrestaShop

This project is an open-source implementation of an online yarn shop inspired by the structure and functionality of biferno.pl. It leverages the PrestaShop platform for e-commerce capabilities and includes tools for product data scraping and integration.

## Features

- Web Scraper: A custom web scraper that extracts product information from the source store.

- PrestaShop API Integration: A script to upload scraped product data into a PrestaShop store using its API.

- Custom Configuration: Project-specific configuration designed to meet defined requirements.

- Deployment: The project is deployed using docker containers that are created by a docker-compose file.

## Quickstart

### 1. Generate ssl certificates

```bash
./generate_ssl.sh
```

### 2. Start the project

```bash
docker compose up
```

### 3. Admin panel and login

#### 1. Enter the following url
```
https://127.0.0.1/admin6787apny1
```

#### 2. Enter the following credentials
```
Login: demo@prestashop.com
Password: prestashop_demo
```

## Team Members

- Mikołaj Klikowicz 193264
- Adam Jakubowski 193352
- Hubert Wajda 193511
- Aleks Iwicki 193354
- Gracjan Grzech 193579
