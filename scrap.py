import requests
from bs4 import BeautifulSoup
import openpyxl

def scrape_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extracting title
        title_entry = soup.find('h1', class_='entry-title')
        if title_entry:
            title = title_entry.text.strip()
        else:
            title_tdb = soup.find('h1', class_='tdb-title-text')
            title = title_tdb.text.strip() if title_tdb else None
        
        # Extracting content
        content_div = None
        div_classes = [
            'td-post-content tagdiv-type',
            'td-pb-row',
            'td_block_wrap tdb_single_content tdi_130 td-pb-border-top td_block_template_1 td-post-content tagdiv-type',
            'tdb-block-inner td-fix-index'
        ]
        for div_class in div_classes:
            content_div = soup.find('div', class_=div_class)
            if content_div:
                break
        
        content = content_div.text.strip() if content_div else ""
        return title, content
    else:
        print(f"Failed to scrape data from {url}")
        return None, None

def main():
    # Load Excel file
    workbook = openpyxl.load_workbook('Input.xlsx')
    sheet = workbook.active

    for row in sheet.iter_rows(min_row=2, values_only=True):
        url_id, url = row
        title, content = scrape_data(url)
        if title and content:
            with open(f"{url_id}.txt", "w", encoding="utf-8") as file:
                file.write(f"{title}\n")
                file.write(f"\n{content}")

if __name__ == "__main__":
    main()
