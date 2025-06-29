import requests
from bs4 import BeautifulSoup
import json
import time
from urllib.parse import urljoin, urlparse
import re

class WebsiteSpecificScraper:
    """Scraper with website-specific configurations"""
    
    def __init__(self, delay=2.0):
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
    
    def scrape_geeksforgeeks_article(self, url):
        """
        Scrape GeeksforGeeks articles
        Example URL: https://www.geeksforgeeks.org/python-programming-language/
        """
        try:
            print(f" Scraping GeeksforGeeks: {url}")
            response = self.session.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            data = {
                'url': url,
                'title': '',
                'content': '',
                'code_blocks': [],
                'related_articles': [],
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Extract title
            title_selectors = [
                'h1.entry-title',
                'h1',
                'title'
            ]
            for selector in title_selectors:
                title_elem = soup.select_one(selector)
                if title_elem:
                    data['title'] = title_elem.get_text().strip()
                    break
            
            # Extract main content
            content_selectors = [
                '.text',
                '.entry-content',
                'article',
                '.article-content'
            ]
            for selector in content_selectors:
                content_elem = soup.select_one(selector)
                if content_elem:
                    paragraphs = content_elem.find_all('p')
                    data['content'] = '\n\n'.join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])
                    break
            
            code_blocks = soup.find_all(['pre', 'code'])
            for i, code in enumerate(code_blocks):
                code_text = code.get_text().strip()
                if len(code_text) > 10:  
                    data['code_blocks'].append({
                        'index': i,
                        'language': code.get('class', [''])[0] if code.get('class') else 'unknown',
                        'code': code_text[:500] + '...' if len(code_text) > 500 else code_text
                    })
            
            related_links = soup.find_all('a', href=True)
            for link in related_links:
                href = link.get('href')
                if href and 'geeksforgeeks.org' in href and href.startswith('http'):
                    link_text = link.get_text().strip()
                    if link_text and len(link_text) > 5:
                        data['related_articles'].append({
                            'title': link_text,
                            'url': href
                        })
            
            seen_urls = set()
            unique_articles = []
            for article in data['related_articles']:
                if article['url'] not in seen_urls:
                    seen_urls.add(article['url'])
                    unique_articles.append(article)
            data['related_articles'] = unique_articles[:10]  
            
            print(f"   Successfully scraped GeeksforGeeks article")
            print(f"   Title: {data['title'][:50]}...")
            print(f"   Content length: {len(data['content'])} characters")
            print(f"   Code blocks: {len(data['code_blocks'])}")
            print(f"   Related articles: {len(data['related_articles'])}")
            
            return data
            
        except Exception as e:
            print(f" Error scraping GeeksforGeeks: {e}")
            return None
    
    def scrape_stackoverflow_question(self, url):
        """
        Scrape Stack Overflow questions
        Example URL: https://stackoverflow.com/questions/tagged/python
        """
        try:
            print(f" Scraping Stack Overflow: {url}")
            response = self.session.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            data = {
                'url': url,
                'questions': [],
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            question_elements = soup.find_all('div', class_='s-post-summary')
            
            for question in question_elements[:5]:  
                question_data = {}
                
                title_elem = question.find('h3')
                if title_elem:
                    link_elem = title_elem.find('a')
                    if link_elem:
                        question_data['title'] = link_elem.get_text().strip()
                        question_data['url'] = urljoin(url, link_elem.get('href', ''))
                
                tags = question.find_all('a', class_='post-tag')
                question_data['tags'] = [tag.get_text().strip() for tag in tags]
                
                stats_elem = question.find('div', class_='s-post-summary--stats')
                if stats_elem:
                    stats = stats_elem.find_all('span')
                    question_data['stats'] = [stat.get_text().strip() for stat in stats]
                
                excerpt_elem = question.find('div', class_='s-post-summary--content-excerpt')
                if excerpt_elem:
                    question_data['excerpt'] = excerpt_elem.get_text().strip()
                
                if question_data:
                    data['questions'].append(question_data)
            
            print(f" Successfully scraped {len(data['questions'])} Stack Overflow questions")
            return data
            
        except Exception as e:
            print(f" Error scraping Stack Overflow: {e}")
            return None
    
    def scrape_github_repo(self, url):
        """
        Scrape GitHub repository information
        Example URL: https://github.com/python/cpython
        """
        try:
            print(f" Scraping GitHub: {url}")
            response = self.session.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            data = {
                'url': url,
                'repo_name': '',
                'description': '',
                'stats': {},
                'languages': [],
                'recent_commits': [],
                'files': [],
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            name_elem = soup.find('strong', {'itemprop': 'name'})
            if name_elem:
                data['repo_name'] = name_elem.get_text().strip()
            
            desc_elem = soup.find('p', {'itemprop': 'about'})
            if desc_elem:
                data['description'] = desc_elem.get_text().strip()
            
            stats_elements = soup.find_all('a', class_='Link--muted')
            for stat in stats_elements:
                stat_text = stat.get_text().strip()
                if 'star' in stat_text.lower():
                    data['stats']['stars'] = stat_text
                elif 'fork' in stat_text.lower():
                    data['stats']['forks'] = stat_text
            
            lang_elements = soup.find_all('span', class_='color-fg-default')
            for lang in lang_elements:
                lang_text = lang.get_text().strip()
                if lang_text and len(lang_text) < 20:  
                    data['languages'].append(lang_text)
            
            file_elements = soup.find_all('a', class_='Link--primary')
            for file_elem in file_elements[:10]:  
                file_name = file_elem.get_text().strip()
                if file_name and '.' in file_name: 
                    data['files'].append(file_name)
            
            print(f"   Successfully scraped GitHub repo: {data['repo_name']}")
            print(f"   Description: {data['description'][:50]}...")
            print(f"   Languages: {len(data['languages'])}")
            print(f"   Files found: {len(data['files'])}")
            
            return data
            
        except Exception as e:
            print(f" Error scraping GitHub: {e}")
            return None
    
    def scrape_news_site(self, url):
        """
        Generic news site scraper
        Works with many news websites
        """
        try:
            print(f" Scraping news site: {url}")
            response = self.session.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            data = {
                'url': url,
                'headlines': [],
                'articles': [],
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            headline_selectors = [
                'h1', 'h2', 'h3',
                '.headline', '.title',
                '[class*="headline"]',
                '[class*="title"]'
            ]
            
            for selector in headline_selectors:
                headlines = soup.select(selector)
                for headline in headlines[:10]:  
                    text = headline.get_text().strip()
                    if text and len(text) > 10:
                        data['headlines'].append(text)
                if data['headlines']:
                    break
            
            article_links = soup.find_all('a', href=True)
            for link in article_links[:15]:  
                href = link.get('href')
                text = link.get_text().strip()
                if text and len(text) > 10 and href:
                    absolute_url = urljoin(url, href)
                    data['articles'].append({
                        'title': text,
                        'url': absolute_url
                    })
            
            print(f"   Successfully scraped news site")
            print(f"   Headlines: {len(data['headlines'])}")
            print(f"   Article links: {len(data['articles'])}")
            
            return data
            
        except Exception as e:
            print(f" Error scraping news site: {e}")
            return None

def demo_different_websites():
    """Demonstrate scraping different types of websites"""
    
    scraper = WebsiteSpecificScraper(delay=2.0)
    
    test_sites = {
        'GeeksforGeeks': 'https://www.geeksforgeeks.org/python-programming-language/',
        'Stack Overflow': 'https://stackoverflow.com/questions/tagged/python',
        'GitHub': 'https://github.com/python/cpython',
        'News Site': 'https://httpbin.org/html'  
    }
    
    results = {}
    
    for site_name, url in test_sites.items():
        print(f"\n{'='*60}")
        print(f" TESTING: {site_name}")
        print(f"{'='*60}")
        
        try:
            if 'geeksforgeeks' in url:
                result = scraper.scrape_geeksforgeeks_article(url)
            elif 'stackoverflow' in url:
                result = scraper.scrape_stackoverflow_question(url)
            elif 'github' in url:
                result = scraper.scrape_github_repo(url)
            else:
                result = scraper.scrape_news_site(url)
            
            if result:
                results[site_name] = result
                print(f" {site_name} scraped successfully!")
            else:
                print(f" {site_name} failed to scrape")
                
        except Exception as e:
            print(f" Error with {site_name}: {e}")
        
        time.sleep(2)
    
    if results:
        filename = 'multi_website_scraping_results.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n All results saved to: {filename}")
        print(f"Successfully scraped {len(results)} different websites")
        
        
        print(f"\n SUMMARY:")
        for site, data in results.items():
            print(f"   {site}: {len(str(data))} characters of data")

def test_single_url(url):
    """Test scraping a single URL"""
    print(f" Testing URL: {url}")
    
    try:
        response = requests.get(url, timeout=10)
        print(f" Status Code: {response.status_code}")
        print(f" Content Length: {len(response.content):,} bytes")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find('title')
        print(f" Title: {title.get_text() if title else 'No title found'}")
        
        paragraphs = len(soup.find_all('p'))
        links = len(soup.find_all('a'))
        images = len(soup.find_all('img'))
        
        print(f"   Elements found:")
        print(f"   Paragraphs: {paragraphs}")
        print(f"   Links: {links}")
        print(f"   Images: {images}")
        
        return True
        
    except Exception as e:
        print(f" Error: {e}")
        return False

if __name__ == "__main__":
    print(" Website-Specific Scraper Demo")
    print("="*50)
    
    
    print("\n TESTING INDIVIDUAL URLS:")
    test_urls = [
        "https://www.geeksforgeeks.org/",
        "https://stackoverflow.com/",
        "https://github.com/",
        "https://httpbin.org/html"
    ]
    
    for url in test_urls:
        print(f"\n{'-'*40}")
        success = test_single_url(url)
        if success:
            print(" This URL can be scraped!")
        else:
            print(" This URL might be blocked or have issues")
        time.sleep(1)
    
    print(f"\n{'='*60}")
    print(" RUNNING FULL SCRAPING DEMO")
    print(f"{'='*60}")
    demo_different_websites()