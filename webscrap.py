import requests
from bs4 import BeautifulSoup
import os
import re

# Set the base URL and number of PDFs per page
base_url = "https://repositorio.ufsc.br/handle/123456789/76395/recent-submissions?offset="
pdfs_per_page = 20  # Number of PDFs to fetch per page

# Function to download PDF
def download_pdf(pdf_url, save_dir, pdf_name):
    # Remove invalid characters for filenames
    pdf_name = re.sub(r'[\/:*?"<>|]', '', pdf_name)

    # Remove any query parameters from the filename
    pdf_name = pdf_name.split('?')[0]  # Split on '?' and take the first part

    # Ensure the file name ends with .pdf
    if not pdf_name.lower().endswith('.pdf'):
        pdf_name += '.pdf'  # Append .pdf if it's not already there
    
    response = requests.get(pdf_url)
    if response.status_code == 200:
        with open(os.path.join(save_dir, pdf_name), 'wb') as file:
            file.write(response.content)
        print(f"Downloaded {pdf_name}")
    else:
        print(f"Failed to download {pdf_name}")

# Function to scrape a page and download all PDFs
def scrape_page(offset, save_dir):
    url = base_url + str(offset)
    print(f"Scraping page: {url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all artifact-title divs
    articles = soup.find_all('div', class_='artifact-title')

    if not articles:
        print("No more articles found on this page.")
        return False  # Indicates no more articles

    for article in articles:
        article_url = 'https://repositorio.ufsc.br' + article.find('a')['href']
        print(f"Opening article: {article_url}")
        article_response = requests.get(article_url)
        article_soup = BeautifulSoup(article_response.text, 'html.parser')

        pdf_link = article_soup.find('a', href=lambda href: href and "bitstream" in href)
        if pdf_link:
            pdf_url = 'https://repositorio.ufsc.br' + pdf_link['href']
            pdf_name = pdf_url.split('/')[-1]
            download_pdf(pdf_url, save_dir, pdf_name)
        else:
            print("No PDF link found in the article.")
    
    return True  # Indicates that articles were found

# Scraping multiple pages
save_directory = "./pdfs"
os.makedirs(save_directory, exist_ok=True)

offset = 0
while True:
    if not scrape_page(offset, save_directory):
        break  # Exit the loop if no more articles are found
    offset += pdfs_per_page  # Increment the offset by the number of PDFs per page
