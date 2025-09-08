#!/usr/bin/env python3
"""
Test script for the updated Shopify App Scraper
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from shopify_app_scraper import ShopifyAppScraper

def test_klaviyo():
    """Test scraping Klaviyo specifically"""
    scraper = ShopifyAppScraper()
    
    # Use Chinese locale URL
    url = "https://apps.shopify.com/klaviyo-email-marketing?locale=zh-CN"
    print(f"Testing updated scraper with Chinese locale: {url}")
    print("=" * 60)
    
    result = scraper.extract_app_info(url)
    
    print("Results:")
    for key, value in result.items():
        print(f"{key:15}: {value}")
    
    print("\n" + "=" * 60)
    print("Expected results:")
    print(f"{'category':15}: 电子邮件营销、短信营销 (or similar)")
    print(f"{'review_count':15}: 2484 (or similar)")
    print(f"{'rating':15}: 4.7 (or similar)")

if __name__ == "__main__":
    test_klaviyo()