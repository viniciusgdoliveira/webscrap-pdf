<!-- @format -->

# PDF Scraper

This Python script scrapes a repository of PDF documents from the Universidade Federal de Santa Catarina (UFSC) and downloads them to a specified directory.

## Libraries Used

- `requests`: For making HTTP requests.
- `beautifulsoup4`: For parsing HTML and extracting data.

## How It Works

1. **Set Up**: The script sets a base URL and the number of PDFs to fetch per page.
2. **Download PDF**: The `download_pdf` function handles downloading a PDF file given its URL and saving it to the specified directory.
3. **Scrape Page**: The `scrape_page` function scrapes a given page for article links and PDF download links.
4. **Multiple Pages**: The script continues to scrape multiple pages until no more articles are found.

## Usage

1. Ensure you have the required libraries installed. You can do this by running:

   ```bash
   pip install -r requirements.txt
   ```
2. Run the script
   ```bash
   python webscrap.py
   ```
The downloaded PDFs will be saved in the pdfs directory.
