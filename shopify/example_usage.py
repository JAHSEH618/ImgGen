#!/usr/bin/env python3
"""
Simple example of how to use the Shopify App Scraper
"""

from .shopify_app_scraper import ShopifyAppScraper

def test_single_url():
    """Test scraping a single URL"""
    scraper = ShopifyAppScraper()
    
    url = "https://apps.shopify.com/klaviyo-email-marketing"
    print(f"Scraping: {url}")
    
    result = scraper.extract_app_info(url)
    
    print("\nResults:")
    for key, value in result.items():
        print(f"{key}: {value}")

def test_batch_scraping():
    """Test scraping multiple URLs from file"""
    scraper = ShopifyAppScraper()
    
    # This will read from example_urls.txt and save to results.csv
    scraper.scrape_urls_from_file('example_urls.txt', 'results.csv')
    print("Batch scraping completed! Check results.csv")

if __name__ == "__main__":
    print("Testing single URL scraping...")
    test_single_url()
    
    print("\n" + "="*50)
    print("Testing batch scraping...")
    test_batch_scraping()