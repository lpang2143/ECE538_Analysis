import requests

def fetch_cdns(website_url):
    try:
        response = requests.get(website_url)
        cdns = response.headers.get('CDN')
        return cdns.split(',') if cdns else []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching CDNs: {e}")
        return []
