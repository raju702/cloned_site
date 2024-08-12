import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def download_file(url, folder):
    response = requests.get(url)
    filepath = os.path.join(folder, os.path.dirname(url[len(urljoin(url, '/')):]))
    os.makedirs(filepath, exist_ok=True)
    basename = os.path.basename(url)
    if not basename:
        basename = 'index.html'
    filename = os.path.join(filepath, basename)
    with open(filename, 'wb') as file:
        file.write(response.content)
      
def clone_page(url, folder):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    main_page = os.path.join(folder, 'index.html')
    with open(main_page, 'w', encoding='utf-8') as file:
        file.write(str(soup))
    for tag in soup.find_all(['img', 'script', 'link']):
        attr = 'src' if tag.name == 'img' or tag.name == 'script' else 'href'
        resource_url = tag.get(attr)
        
        if resource_url:
            resource_url = urljoin(url, resource_url)
            download_file(resource_url, folder)

def main():
    url = input("Enter the URL of the website to clone: ")
    folder = 'cloned_site'
    
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    clone_page(url, folder)
    print("Website cloned successfully!")

if __name__ == "__main__":
    main()
