import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import urllib
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
import time
import random

class SitemapGenerator:
    
    def __init__(self, root, filename):
        self.filename = filename
        self.urls = {}
        self.root = root
        self.hostname = urlparse(root).hostname
        self.max_depth = 2 # Set a maximum depth for crawling
        self.visited = set()  # To avoid duplicate requests

    def crawl(self, url, level, retries=3):
        if level > self.max_depth or url in self.visited:
            return

        print(f"Level: {level}/ Exploring: {url}")
        self.visited.add(url)

        for attempt in range(retries):
            try:
                # Set a custom User-Agent
                headers = {'User-Agent': 'SitemapGenerator/1.0'}
                with requests.Session() as session:
                    response = session.get(url, headers=headers, timeout=10)  # 10 seconds timeout
                    if response.status_code == 200:
                        url = urllib.parse.urldefrag(url)[0]

                        if url not in self.urls:
                            self.urls[url] = level
                            soup = BeautifulSoup(response.content, "html.parser")

                            links = []
                            for link in soup.findAll('a'):
                                href = link.get('href')
                                result = urlparse(href)
                                newurl = None

                                if result.hostname is None and href is not None:
                                    newurl = self.root + ("/", "")[href.startswith("/")] + href
                                elif result.hostname == self.hostname:
                                    newurl = href

                                if newurl is not None and newurl not in self.visited:
                                    links.append(newurl)

                            with ThreadPoolExecutor(max_workers=1) as executor:  # KEEP AT 1 TO AVOID RATE LIMIT/ACCIDENTAL DDOS
                                for newurl in links:
                                    executor.submit(self.crawl, newurl, level + 1)

                        break
                    else:
                        print(f"{url} unreachable with status {response.status_code}")
                        break
            except requests.Timeout:
                print(f"Timeout while requesting {url}. Attempt {attempt + 1} of {retries}.")
                if attempt + 1 == retries:  # If last attempt, log an error
                    print(f"Failed to retrieve {url} after {retries} attempts.")
            except requests.RequestException as e:
                print(f"Error while requesting {url}: {e}")
                break
            
            # Exponential backoff with a randomized delay
            time.sleep(random.uniform(1, 2 ** attempt))  # Randomized wait time for next retry

    def generatefile(self):
        urlsbylevel = {}
        maxlevel = 0
        
        for key, value in self.urls.items():
            maxlevel = max(maxlevel, value)
            urlsbylevel.setdefault(value, []).append(key)
        
        # Calculate priority based on levels
        step = 1 / (maxlevel * 2)
        root = ET.Element('urlset', xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')

        for key, value in urlsbylevel.items():
            priority = round(1 - step * key, 2)
            for item in value:
                url_elem = ET.SubElement(root, "url")
                ET.SubElement(url_elem, "loc").text = item
                ET.SubElement(url_elem, "priority").text = str(priority)

        # Write XML to file
        tree = ET.ElementTree(root)
        ET.indent(tree, '  ')
        tree.write(self.filename, encoding="utf-8", xml_declaration=True)

sitemapGenerator = SitemapGenerator("https://www.google.com", "sitemap.xml") # No trailing / !
sitemapGenerator.crawl("https://www.google.com", 0) # No trailing / !
sitemapGenerator.generatefile()
