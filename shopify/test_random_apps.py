#!/usr/bin/env python3
"""
Test script for random Shopify apps with improved pricing extraction
"""

import sys
import os
import random
sys.path.append(os.path.dirname(__file__))

from shopify_app_scraper import ShopifyAppScraper

def load_random_urls(filename='example_urls.txt', count=5):
    """Load random URLs from the file"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]
        
        # Add Chinese locale to URLs
        urls_with_locale = []
        for url in urls:
            if '?' in url:
                url_with_locale = url + '&locale=zh-CN'
            else:
                url_with_locale = url + '?locale=zh-CN'
            urls_with_locale.append(url_with_locale)
        
        # Select random URLs
        selected_urls = random.sample(urls_with_locale, min(count, len(urls_with_locale)))
        return selected_urls
    
    except FileNotFoundError:
        print(f"File {filename} not found!")
        return []

def test_random_apps():
    """Test scraping random apps"""
    scraper = ShopifyAppScraper()
    
    # Load 5 random URLs
    urls = load_random_urls(count=5)
    
    if not urls:
        print("No URLs found to test!")
        return
    
    print(f"Testing {len(urls)} random Shopify apps...")
    print("=" * 80)
    
    for i, url in enumerate(urls, 1):
        app_name = url.split('/')[-1].split('?')[0].replace('-', ' ').title()
        print(f"\n[{i}/{len(urls)}] Testing: {app_name}")
        print(f"URL: {url}")
        print("-" * 60)
        
        result = scraper.extract_app_info(url)
        
        print(f"Name        : {result['name']}")
        print(f"Description : {result['description'][:100]}{'...' if len(result['description']) > 100 else ''}")
        print(f"Category    : {result['category']}")
        print(f"Pricing     : {result['pricing']}")
        print(f"Reviews     : {result['review_count']}")
        print(f"Rating      : {result['rating']}")
        
        if i < len(urls):
            print("\n" + "=" * 80)

if __name__ == "__main__":
    test_random_apps()