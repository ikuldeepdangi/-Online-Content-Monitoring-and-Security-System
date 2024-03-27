import requests

def crawl_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return None

# Test Crawling
if __name__ == '__main__':
    url = 'https://example.com'
    html_content = crawl_url(url)
    print(html_content)
