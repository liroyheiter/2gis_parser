import requests
from bs4 import BeautifulSoup
import json
import time
import os

base_url = 'https://2gis.kz/astana/search/%D0%9F%D0%BE%D0%B5%D1%81%D1%82%D1%8C'
restaurant_data = []
max_items = 1000
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def fetch_page(url):
    response = requests.get(url, headers=headers)
    response.raise_for_status()  
    return response.text

def parse_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    restaurants = soup.find_all('div', class_='_1kf6gff')
    for restaurant in restaurants:
        if len(restaurant_data) >= 1000:
            break
        name = restaurant.find('div', class_='_zjunba').get_text() if restaurant.find('div', class_='_zjunba') else None
        average_check = restaurant.find('div', class_='_d76pv4').get_text() if restaurant.find('div', class_='_d76pv4') else None
        address = restaurant.find('div', class_='_klarpw').get_text() if restaurant.find('div', class_='_klarpw') else None
        restaurant_data.append({
            'name': name,
            'average check': average_check,
            'address': address
        })

def main():
    directory = os.path.dirname(__file__)  # Получаем путь к директории текущего файла
    output_filename = os.path.join(directory, 'restaurants_parsed.json')
    current_page = 1
    url = base_url
    while len(restaurant_data) < 1000:
        url = f"{base_url}/page/{current_page}"
        html = fetch_page(url)
        parse_page(html)
        current_page += 1 
        
       
    
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(restaurant_data, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    main()
