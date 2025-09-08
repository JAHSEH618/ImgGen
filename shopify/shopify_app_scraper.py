#!/usr/bin/env python3
"""
Shopify App Store Scraper

This script scrapes Shopify app information including:
- App name
- Description
- Category
- Pricing
- Review count
- Rating

Usage:
    python shopify_app_scraper.py input.txt output.csv

Input file format: One URL per line
"""

import requests
from bs4 import BeautifulSoup
import csv
import re
import time
import argparse
from urllib.parse import urljoin
import logging

class ShopifyAppScraper:
    def __init__(self):
        self.session = requests.Session()
        
        # Rotate through multiple realistic user agents
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15'
        ]
        
        # Set comprehensive headers to mimic real browser
        self.session.headers.update({
            'User-Agent': self._get_random_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'Connection': 'keep-alive'
        })
        
        # Request count for rotation
        self.request_count = 0
    
    def _get_random_user_agent(self):
        """Get a random user agent for rotation"""
        import random
        return random.choice(self.user_agents)
    
    def _add_random_delay(self):
        """Add random delay between requests"""
        import random
        delay = random.uniform(1.5, 4.0)  # Random delay between 1.5-4 seconds
        time.sleep(delay)
        
    def extract_app_info(self, url):
        """Extract app information from a Shopify app page"""
        try:
            # Rotate user agent for each request
            self.request_count += 1
            if self.request_count % 3 == 0:  # Change every 3 requests
                self.session.headers['User-Agent'] = self._get_random_user_agent()
            
            # Add random delay to avoid being detected
            self._add_random_delay()
            
            # Make request with timeout and retries
            for attempt in range(3):  # Max 3 attempts
                try:
                    response = self.session.get(url, timeout=15)
                    response.raise_for_status()
                    break
                except requests.exceptions.RequestException as e:
                    if attempt == 2:  # Last attempt
                        raise e
                    time.sleep(2 ** attempt)  # Exponential backoff
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract app name
            name = self._extract_name(soup)
            
            # Extract description (enhanced)
            description = self._extract_description(soup)
            
            # Extract category
            category = self._extract_category(soup)
            
            # Extract pricing
            pricing = self._extract_pricing(soup)
            
            # Extract review count and rating
            review_count, rating = self._extract_reviews_and_rating(soup)
            
            return {
                'url': url,
                'name': name,
                'description': description,
                'category': category,
                'pricing': pricing,
                'review_count': review_count,
                'rating': rating
            }
            
        except Exception as e:
            logging.error(f"Error scraping {url}: {str(e)}")
            return {
                'url': url,
                'name': 'Error',
                'description': 'Error',
                'category': 'Error',
                'pricing': 'Error',
                'review_count': 'Error',
                'rating': 'Error'
            }
    
    def _extract_name(self, soup):
        """Extract app name"""
        selectors = [
            'h1',
            '.app-listing-hero__title',
            '[data-testid="app-title"]',
            '.heading--1'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text(strip=True)
        
        return "Not found"
    
    def _extract_description(self, soup):
        """Extract app description (prioritize detailed Chinese content)"""
        detailed_descriptions = []
        
        # Look for comprehensive description sections
        description_sections = [
            '.app-description',
            '.app-listing-hero__description', 
            '.description-content',
            '[data-testid="app-description"]',
            '.app-details',
            '.app-overview',
            '.product-description'
        ]
        
        # First: Extract from structured description sections
        for selector in description_sections:
            elements = soup.select(selector)
            for element in elements:
                text = element.get_text(strip=True)
                if text and len(text) > 20:
                    chinese_ratio = len(re.findall(r'[\u4e00-\u9fff]', text)) / len(text) if text else 0
                    if chinese_ratio > 0.2:
                        detailed_descriptions.append((text, chinese_ratio, len(text)))
        
        # Second: Look for detailed Chinese description patterns in full text
        page_text = soup.get_text()
        
        # Enhanced Chinese patterns for more detailed content
        detailed_chinese_patterns = [
            r'通过[^。]*。[^。]*。[^。]*。?',  # 3 sentences starting with "通过"
            r'[\u4e00-\u9fff][^。]*电子邮件[^。]*。[^。]*。[^。]*。?',  # 3 sentences with "电子邮件"
            r'[\u4e00-\u9fff][^。]*营销[^。]*。[^。]*短信[^。]*。[^。]*。?',  # Marketing + SMS content
            r'[\u4e00-\u9fff][^。]*增长[^。]*。[^。]*店铺[^。]*。[^。]*。?',  # Growth + Store content
            r'[\u4e00-\u9fff][^。]*个性化[^。]*。[^。]*自动化[^。]*。[^。]*。?',  # Personalization + Automation
            # Multi-sentence patterns
            r'[\u4e00-\u9fff][^。]*。[\u4e00-\u9fff][^。]*。[\u4e00-\u9fff][^。]*。[\u4e00-\u9fff][^。]*。',
            r'[\u4e00-\u9fff][^。]*。[\u4e00-\u9fff][^。]*。[\u4e00-\u9fff][^。]*。'
        ]
        
        for pattern in detailed_chinese_patterns:
            matches = re.findall(pattern, page_text)
            for match in matches:
                if len(match) > 50 and len(match) < 800:  # More detailed content
                    chinese_ratio = len(re.findall(r'[\u4e00-\u9fff]', match)) / len(match)
                    if chinese_ratio > 0.3:
                        detailed_descriptions.append((match.strip(), chinese_ratio, len(match)))
        
        # Third: Look for feature descriptions and benefits sections
        feature_sections = soup.find_all(['div', 'section'], string=re.compile(r'[功能特点优势介绍说明]', re.I))
        for section in feature_sections:
            if section.parent:
                container = section.parent
                container_text = container.get_text(strip=True)
                if len(container_text) > 100 and len(container_text) < 1000:
                    chinese_ratio = len(re.findall(r'[\u4e00-\u9fff]', container_text)) / len(container_text)
                    if chinese_ratio > 0.3:
                        detailed_descriptions.append((container_text, chinese_ratio, len(container_text)))
        
        # Fourth: Look for paragraphs with substantial Chinese content
        paragraphs = soup.find_all(['p', 'div'], string=re.compile(r'[\u4e00-\u9fff]'))
        paragraph_texts = []
        for p in paragraphs:
            text = p.get_text(strip=True)
            if len(text) > 30:
                paragraph_texts.append(text)
        
        # Combine related paragraphs
        if len(paragraph_texts) >= 2:
            combined_text = ' '.join(paragraph_texts[:4])  # Combine up to 4 paragraphs
            if len(combined_text) > 100 and len(combined_text) < 1000:
                chinese_ratio = len(re.findall(r'[\u4e00-\u9fff]', combined_text)) / len(combined_text)
                if chinese_ratio > 0.3:
                    detailed_descriptions.append((combined_text, chinese_ratio, len(combined_text)))
        
        # Select the best description based on Chinese ratio and length
        if detailed_descriptions:
            # Sort by Chinese ratio (descending) and then by length (descending)
            detailed_descriptions.sort(key=lambda x: (x[1], x[2]), reverse=True)
            best_description = detailed_descriptions[0][0]
            
            # Clean up the description
            best_description = re.sub(r'\s+', ' ', best_description)  # Normalize whitespace
            best_description = re.sub(r'[\n\r\t]+', ' ', best_description)  # Remove line breaks
            
            return best_description
        
        # Fallback: Try original selectors for any content
        fallback_selectors = [
            'meta[name="description"]',
            '.app-listing-hero__description',
            '.app-listing-hero p'
        ]
        
        for selector in fallback_selectors:
            if selector.startswith('meta'):
                element = soup.select_one(selector)
                if element:
                    content = element.get('content', '').strip()
                    if content:
                        return content
            else:
                element = soup.select_one(selector)
                if element:
                    content = element.get_text(strip=True)
                    if content:
                        return content
        
        return "Not found"
    
    def _extract_category(self, soup):
        """Extract app categories from the specific xpath location"""
        categories = []
        
        # Method 1: Target the specific xpath /html/body/main/div[1]/div/div[2]/section/div[5]/div/div
        # Navigate through the DOM structure step by step
        body = soup.find('body')
        if body:
            main = body.find('main')
            if main:
                # Get the first div under main
                main_div = main.find('div')
                if main_div:
                    # Get the nested div structure
                    nested_div = main_div.find('div')
                    if nested_div:
                        # Get div[2] (third div, 0-indexed)
                        div_children = nested_div.find_all('div', recursive=False)
                        if len(div_children) >= 3:
                            target_div2 = div_children[2]
                            # Look for section within this div
                            section = target_div2.find('section')
                            if section:
                                # Navigate to div[5]/div/div
                                section_divs = section.find_all('div', recursive=False)
                                if len(section_divs) >= 6:
                                    div5 = section_divs[5]  # div[5] is index 5
                                    inner_div = div5.find('div')
                                    if inner_div:
                                        final_div = inner_div.find('div')
                                        if final_div:
                                            # Extract category information from this final div
                                            category_links = final_div.find_all('a')
                                            for link in category_links:
                                                href = link.get('href', '')
                                                text = link.get_text(strip=True)
                                                
                                                if 'categories' in href and text:
                                                    categories.append(text)
                                            
                                            # Also check for direct text content
                                            if not categories:
                                                text_content = final_div.get_text(strip=True)
                                                if text_content and len(text_content) < 100:
                                                    # Split by common delimiters and filter
                                                    potential_categories = re.split(r'[,、。;]', text_content)
                                                    for cat in potential_categories:
                                                        clean_cat = cat.strip()
                                                        if clean_cat and len(clean_cat) < 30:
                                                            categories.append(clean_cat)
        
        # Method 2: Alternative approach - look for main > div structure directly
        if not categories:
            main_element = soup.select_one('main')
            if main_element:
                # Try to navigate using CSS selectors for the path
                target_elements = main_element.select('div div:nth-child(3) section div:nth-child(6) div div')
                for element in target_elements:
                    # Look for category links
                    links = element.find_all('a')
                    for link in links:
                        href = link.get('href', '')
                        text = link.get_text(strip=True)
                        if 'categories' in href and text:
                            categories.append(text)
        
        # Method 3: Look for section elements with category information
        if not categories:
            sections = soup.find_all('section')
            for section in sections:
                # Look for divs that might contain category info
                div_containers = section.find_all('div')
                for div in div_containers:
                    links = div.find_all('a')
                    for link in links:
                        href = link.get('href', '')
                        text = link.get_text(strip=True)
                        
                        if ('categories' in href and 
                            text and 
                            len(text) < 30 and
                            re.search(r'[\u4e00-\u9fff]', text)):  # Contains Chinese
                            categories.append(text)
                            
                    # Limit to avoid too many results
                    if len(categories) >= 5:
                        break
                if len(categories) >= 5:
                    break
        
        # Method 4: Fallback - search for common category patterns
        if not categories:
            # Look for specific category-related sections or divs
            page_text = soup.get_text()
            
            # Common Shopify app categories in Chinese
            category_patterns = [
                r'电子邮件营销',
                r'短信营销',
                r'邮件营销',
                r'营销与转化',
                r'商店设计',
                r'销售渠道',
                r'客户服务',
                r'订单和发货',
                r'商店管理',
                r'产品管理',
                r'库存管理',
                r'支付处理',
                r'运输配送',
                r'分析报告',
                r'社交证明',
                r'广告营销',
                r'增销交叉销售',
                r'收集反馈',
                r'购物车优化'
            ]
            
            for pattern in category_patterns:
                if re.search(pattern, page_text):
                    categories.append(pattern)
                    if len(categories) >= 3:
                        break
        
        # Method 5: Last resort - look for any category links
        if not categories:
            category_links = soup.find_all('a', href=re.compile(r'/categories/'))
            for link in category_links[:10]:  # Limit to first 10
                text = link.get_text(strip=True)
                if (text and 
                    len(text) < 25 and 
                    re.search(r'[\u4e00-\u9fff]', text) and  # Contains Chinese
                    not any(exclude in text.lower() for exclude in ['browse', '浏览', 'more', '更多', 'all', '全部'])):
                    categories.append(text)
                    if len(categories) >= 3:
                        break
        
        # Clean and deduplicate categories
        unique_categories = []
        seen = set()
        
        for category in categories:
            if category and len(category.strip()) > 1:
                clean_category = category.strip()
                if clean_category not in seen and len(clean_category) < 40:
                    seen.add(clean_category)
                    unique_categories.append(clean_category)
        
        # Return top 3 categories
        final_categories = unique_categories[:3]
        return '、'.join(final_categories) if final_categories else "Not found"
    
    def _extract_pricing(self, soup):
        """Extract comprehensive pricing information with multiple strategies"""
        page_text = soup.get_text()
        
        # Use multiple extraction strategies
        pricing_results = []
        
        # Strategy 1: Look for structured pricing sections
        structured_pricing = self._extract_structured_pricing(soup)
        if structured_pricing:
            pricing_results.extend(structured_pricing)
        
        # Strategy 2: Extract from page text with patterns
        text_pricing = self._extract_pricing_from_page_text(page_text)
        if text_pricing:
            pricing_results.extend(text_pricing)
        
        # Strategy 3: Find pricing near specific keywords
        contextual_pricing = self._extract_contextual_pricing(page_text)
        if contextual_pricing:
            pricing_results.extend(contextual_pricing)
        
        # Clean and format results
        final_pricing = self._clean_pricing_results(pricing_results)
        
        if final_pricing:
            return ' | '.join(final_pricing)
        
        return "Not found"
    
    def _extract_structured_pricing(self, soup):
        """Extract pricing from structured HTML elements"""
        pricing_info = []
        
        # Look for pricing containers
        pricing_selectors = [
            '.price', '.pricing', '.plan', '.subscription', '.cost',
            '[data-price]', '[class*="price"]', '[class*="plan"]',
            '.pricing-card', '.price-card', '.plan-card'
        ]
        
        for selector in pricing_selectors:
            elements = soup.select(selector)
            for element in elements:
                text = element.get_text(strip=True)
                if self._is_pricing_content(text):
                    clean_text = self._clean_pricing_text(text)
                    if clean_text and len(clean_text) > 3:
                        pricing_info.append(clean_text)
        
        return pricing_info[:5]  # Limit to 5 items
    
    def _extract_pricing_from_page_text(self, page_text):
        """Extract pricing using comprehensive regex patterns"""
        pricing_matches = []
        
        # Comprehensive pricing patterns
        patterns = [
            # Free patterns
            r'(免费安装)',
            r'(免费试用)',
            r'(Free[\s\w]*(?:plan|tier|install|trial)?)',
            r'(免费[^。，]{0,30})',
            
            # Dollar amounts with context
            r'(\$\d+(?:\.\d{2})?[\s/]*(?:月|年|month|year|mo)[^。，]{0,50})',
            r'(\$\d+(?:\.\d{2})?[^。，]{0,30}(?:月|年|month|year))',
            r'(\$\d+(?:\.\d{2})?[^\n。，]{0,80})',
            
            # Chinese currency patterns  
            r'(每月[^\n。，]{0,50}\$\d+)',
            r'(从\s*\$\d+[^\n。，]{0,50})',
            
            # Usage-based pricing
            r'(按[^。，]*使用[^。，]{0,30}收费)',
            r'(per[\s\w]*\$\d+)',
            
            # Plans and tiers
            r'([A-Z][\w\s]*(?:plan|tier|package)[^。，]{0,50}\$\d+)',
            r'(\$\d+[^。，]*(?:plan|tier|package)[^。，]{0,30})',
            
            # Contact/usage limits with pricing
            r'(最多[^\n。，]{0,50}\$\d+)',
            r'(up\s*to[^\n。，]{0,50}\$\d+)',
            r'(\d+[\s]*(?:联系人|用户|users?|contacts?)[^\n。，]{0,50})',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, page_text, re.IGNORECASE)
            for match in matches:
                clean_match = re.sub(r'\s+', ' ', match).strip()
                if len(clean_match) >= 3 and len(clean_match) <= 150:
                    pricing_matches.append(clean_match)
        
        return pricing_matches[:8]  # Limit to 8 matches
    
    def _extract_contextual_pricing(self, page_text):
        """Extract pricing by looking around key contexts"""
        contextual_pricing = []
        
        # Define contexts to search around
        contexts = [
            '价格', 'pricing', 'price', '费用', 'cost', '方案', 'plan', 
            '订阅', 'subscription', '付费', 'payment', '免费', 'free',
            'starter', 'basic', 'premium', 'pro', 'enterprise'
        ]
        
        for context in contexts:
            # Look for text around the context
            context_pattern = f'(.{{0,100}}{re.escape(context)}.{{0,100}})'
            matches = re.findall(context_pattern, page_text, re.IGNORECASE)
            
            for match in matches:
                # Check if this context contains pricing info
                if '$' in match or '免费' in match or re.search(r'\d+[\s]*(?:月|年|month|year)', match):
                    clean_match = re.sub(r'\s+', ' ', match).strip()
                    if len(clean_match) > 10 and len(clean_match) < 200:
                        # Extract the most relevant part
                        relevant_part = self._extract_relevant_pricing_part(clean_match)
                        if relevant_part:
                            contextual_pricing.append(relevant_part)
        
        return contextual_pricing[:6]  # Limit to 6 items
    
    def _extract_relevant_pricing_part(self, text):
        """Extract the most relevant pricing part from a longer text"""
        # Look for key pricing indicators
        price_indicators = [
            r'\$\d+(?:\.\d{2})?[^\n。，]{0,40}',
            r'免费[^\n。，]{0,30}',
            r'Free[\s\w]{0,30}',
            r'\d+[\s]*(?:月|年|month|year)[^\n。，]{0,30}',
        ]
        
        for pattern in price_indicators:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                return matches[0].strip()
        
        # If no specific pattern, return a cleaned version of the original
        return text[:80].strip() if len(text) > 80 else text.strip()
    
    def _is_pricing_content(self, text):
        """Check if text contains pricing-related content"""
        if not text or len(text) < 3:
            return False
        
        pricing_keywords = [
            '$', '免费', '价格', '费用', 'free', 'price', 'cost', 
            '月', '年', 'month', 'year', 'plan', '方案', 'subscription', 
            '订阅', 'trial', '试用', 'starter', 'basic', 'premium', 'pro'
        ]
        
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in pricing_keywords)
    
    def _clean_pricing_text(self, text):
        """Clean and format pricing text"""
        if not text:
            return None
        
        # Remove excessive whitespace
        clean_text = re.sub(r'\s+', ' ', text).strip()
        
        # Remove common noise
        noise_patterns = [
            r'^[^A-Za-z\u4e00-\u9fff\$\d]*',  # Leading non-alphanumeric
            r'[^A-Za-z\u4e00-\u9fff\$\d]*$',  # Trailing non-alphanumeric
        ]
        
        for pattern in noise_patterns:
            clean_text = re.sub(pattern, '', clean_text)
        
        return clean_text if len(clean_text) >= 3 else None
    
    def _clean_pricing_results(self, pricing_results):
        """Clean, deduplicate and prioritize pricing results"""
        if not pricing_results:
            return []
        
        # Clean and deduplicate
        cleaned_results = []
        seen = set()
        
        for item in pricing_results:
            if not item or len(item) < 3:
                continue
            
            # Normalize for comparison
            normalized = re.sub(r'[^A-Za-z\u4e00-\u9fff\d\$]', '', item.lower())
            if normalized not in seen and len(normalized) > 2:
                seen.add(normalized)
                cleaned_results.append(item)
        
        # Prioritize results
        prioritized = self._prioritize_pricing_results(cleaned_results)
        
        return prioritized[:4]  # Return top 4 results
    
    def _prioritize_pricing_results(self, results):
        """Prioritize pricing results by relevance"""
        def priority_score(item):
            score = 0
            item_lower = item.lower()
            
            # Higher score for free plans
            if '免费' in item_lower or 'free' in item_lower:
                score += 10
            
            # Higher score for items with dollar amounts
            if '$' in item:
                score += 8
            
            # Higher score for monthly/yearly pricing
            if any(term in item_lower for term in ['月', '年', 'month', 'year']):
                score += 6
            
            # Higher score for plan names
            if any(term in item_lower for term in ['plan', '方案', 'starter', 'basic', 'premium', 'pro']):
                score += 5
            
            # Prefer shorter, more concise descriptions
            score -= len(item) // 20
            
            return score
        
        sorted_results = sorted(results, key=priority_score, reverse=True)
        return sorted_results
    
    def _parse_pricing_plan(self, element):
        """Parse a single pricing plan element"""
        text = element.get_text(strip=True)
        if not text or len(text) < 10:
            return None
            
        plan_info = {}
        
        # Look for plan name
        plan_names = re.findall(r'(免费版?|基础版?|标准版?|专业版?|Free|Basic|Standard|Premium|Pro|Enterprise)', text, re.I)
        if plan_names:
            plan_info['name'] = plan_names[0]
        
        # Look for price
        price_patterns = [
            r'\$(\d+(?:\.\d{2})?)/?(月|年|month|year)?',
            r'(免费|$0|Free)',
            r'(免费安装)'
        ]
        
        for pattern in price_patterns:
            matches = re.findall(pattern, text, re.I)
            if matches:
                if isinstance(matches[0], tuple):
                    plan_info['price'] = matches[0][0] + ('/月' if matches[0][1] else '')
                else:
                    plan_info['price'] = matches[0]
                break
        
        # Look for features/services
        feature_indicators = [
            r'(包含|includes?)[:]：?\s*([^。、]+)',
            r'(功能|features?)[:]：?\s*([^。、]+)',
            r'(联系人|contact)\s*(\d+[,\d]*)',
            r'(短信|SMS)\s*(\d+[,\d]*)',
            r'(邮件|email)\s*(不限|无限|unlimited|\d+[,\d]*)',
        ]
        
        features = []
        for pattern in feature_indicators:
            matches = re.findall(pattern, text, re.I)
            for match in matches:
                if isinstance(match, tuple) and len(match) >= 2:
                    features.append(match[1])
        
        if features:
            plan_info['features'] = ', '.join(features[:3])  # Limit features
        
        # Format the plan info
        if 'name' in plan_info or 'price' in plan_info:
            parts = []
            if 'name' in plan_info:
                parts.append(plan_info['name'])
            if 'price' in plan_info:
                parts.append(plan_info['price'])
            if 'features' in plan_info:
                parts.append(f"({plan_info['features']})")
            
            return '-'.join(parts)
        
        return None
    
    def _parse_pricing_table(self, table):
        """Parse pricing information from a table"""
        plans = []
        table_text = table.get_text()
        
        # Look for rows that contain pricing info
        rows = table.select('tr, .row, .pricing-row')
        for row in rows:
            row_text = row.get_text(strip=True)
            if '$' in row_text or '免费' in row_text or 'Free' in row_text:
                plan = self._parse_pricing_plan(row)
                if plan:
                    plans.append(plan)
        
        return plans
    
    def _extract_pricing_from_text(self, soup):
        """Extract pricing from page text with context"""
        pricing_info = []
        page_text = soup.get_text()
        
        # Comprehensive pricing patterns for all plans
        pricing_patterns = [
            # Free plans - multiple variations
            r'(电子邮件永远免费[^。，]*250[^。，]*联系人)',
            r'(短信免费[^。，]*150[^。，]*SMS[^。，]*积分)',
            r'(免费安装[^。，]*)',
            
            # $15 SMS Plan
            r'(\$15[/／]?月[^。，]*1250[^。，]*SMS[^。，]*积分[^。，]*)',
            r'(最多1250个SMS/MMS积分[^。，]*运营商费用[^。，]*)',
            r'(\$15[^。，]*短信[^。，]*)',
            
            # $20 Email Plan
            r'(\$20[/／]?月[^。，]*251-500[^。，]*联系人[^。，]*)',
            r'(251-500个联系人[^。，]*)',
            r'(\$20[^。，]*电子邮件[^。，]*)',
            
            # General pricing patterns
            r'(\$\d+[/／]?月[^。，]*)',
            r'(免费[^。，]*联系人[^。，]*)',
        ]
        
        found_plans = []
        
        for pattern in pricing_patterns:
            matches = re.findall(pattern, page_text, re.DOTALL)
            for match in matches:
                clean_match = re.sub(r'\s+', ' ', match).strip()
                if len(clean_match) > 8 and clean_match not in found_plans:
                    found_plans.append(clean_match)
        
        # Try to find the three main plans by searching for specific sections
        plan_sections = [
            # Look for sections that mention specific pricing
            r'免费[\s\S]{0,200}250[\s\S]{0,200}联系人',
            r'\$15[\s\S]{0,200}SMS[\s\S]{0,200}1250',
            r'\$20[\s\S]{0,200}电子邮件[\s\S]{0,200}500'
        ]
        
        for pattern in plan_sections:
            matches = re.findall(pattern, page_text, re.DOTALL | re.IGNORECASE)
            for match in matches:
                # Extract key information from the section
                clean_match = re.sub(r'\s+', ' ', match).strip()
                # Summarize the key points
                if '免费' in clean_match and '250' in clean_match:
                    summary = '免费方案: 电子邮件250个联系人 + 短信150积分'
                elif '$15' in clean_match and 'SMS' in clean_match:
                    summary = '$15/月方案: 1250个SMS/MMS积分(含运营商费用)'
                elif '$20' in clean_match and ('电子邮件' in clean_match or '500' in clean_match):
                    summary = '$20/月方案: 电子邮件251-500个联系人 + 高级功能'
                else:
                    summary = clean_match[:80] + '...' if len(clean_match) > 80 else clean_match
                
                if summary not in found_plans:
                    found_plans.append(summary)
        
        # If we still don't have enough details, try a broader search
        if len(found_plans) < 3:
            broader_patterns = [
                r'\$15[^\n]*',
                r'\$20[^\n]*', 
                r'免费[^\n]*250[^\n]*',
                r'最多1250个SMS[^\n]*'
            ]
            
            for pattern in broader_patterns:
                matches = re.findall(pattern, page_text)
                for match in matches:
                    clean_match = match.strip()
                    if len(clean_match) > 5 and clean_match not in found_plans:
                        found_plans.append(clean_match)
        
        # Return the best plans found
        return found_plans[:3] if found_plans else ['定价信息未找到']
    
    def _extract_reviews_and_rating(self, soup):
        """Extract review count and rating"""
        review_count = "Not found"
        rating = "Not found"
        
        # First try to extract from JSON-LD structured data
        script_tags = soup.find_all('script', type='application/ld+json')
        for script in script_tags:
            try:
                import json
                data = json.loads(script.string)
                if isinstance(data, dict):
                    # Look for ratingCount
                    if 'ratingCount' in data:
                        review_count = str(data['ratingCount'])
                    if 'aggregateRating' in data and isinstance(data['aggregateRating'], dict):
                        if 'ratingValue' in data['aggregateRating']:
                            rating = str(data['aggregateRating']['ratingValue'])
                        if 'reviewCount' in data['aggregateRating']:
                            review_count = str(data['aggregateRating']['reviewCount'])
                elif isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict) and 'ratingCount' in item:
                            review_count = str(item['ratingCount'])
                        if isinstance(item, dict) and 'aggregateRating' in item:
                            agg_rating = item['aggregateRating']
                            if isinstance(agg_rating, dict):
                                if 'ratingValue' in agg_rating:
                                    rating = str(agg_rating['ratingValue'])
                                if 'reviewCount' in agg_rating:
                                    review_count = str(agg_rating['reviewCount'])
            except:
                continue
        
        # If we got both from JSON-LD, return early
        if review_count != "Not found" and rating != "Not found":
            return review_count, rating
        
        # Look for rating and review count in the same vicinity
        rating_containers = [
            '.rating-container',
            '.reviews-section',
            '.app-rating',
            '.rating-summary',
            '.review-summary',
            '[data-testid*="rating"]',
            '[class*="rating"]',
            '[class*="review"]'
        ]
        
        # Try to find rating containers first
        rating_elements = []
        for selector in rating_containers:
            elements = soup.select(selector)
            rating_elements.extend(elements)
        
        # If no specific containers, look for elements with rating/review keywords
        if not rating_elements:
            all_elements = soup.find_all(['div', 'section', 'span', 'p'], 
                                       string=re.compile(r'(?:rating|review|star)', re.I))
            rating_elements.extend(all_elements)
        
        # Search in rating vicinity for both rating and review count
        for element in rating_elements:
            if not element:
                continue
                
            # Get the parent container to search in a broader area
            parent = element.parent if element.parent else element
            container_text = parent.get_text(strip=True)
            
            # Look for rating in this container
            if rating == "Not found":
                rating_patterns = [
                    r'(\d+\.\d+)\s*(?:out\s*of\s*5|/5|stars?|★)',
                    r'(\d+\.\d+)\s*(?:stars?|★)',
                    r'Rating[:\s]*(\d+\.\d+)',
                    r'(\d+\.\d+)'
                ]
                
                for pattern in rating_patterns:
                    rating_match = re.search(pattern, container_text, re.IGNORECASE)
                    if rating_match:
                        potential_rating = float(rating_match.group(1))
                        if 0 <= potential_rating <= 5:
                            rating = rating_match.group(1)
                            break
            
            # Look for review count in the same container
            if review_count == "Not found":
                review_patterns = [
                    r'\((\d+(?:,\d+)*)\)\s*(?:reviews?|评论)',  # "(2,484) reviews"
                    r'Reviews?\s*\((\d+(?:,\d+)*)\)',  # "Reviews (2,484)"
                    r'(\d+(?:,\d+)*)\s*reviews?',      # "2484 reviews"
                    r'(\d+(?:,\d+)*)\s*评论',        # "2484 评论"
                    r'\((\d+(?:,\d+)*)\)',             # Just "(2484)"
                    r'Based\s*on\s*(\d+(?:,\d+)*)\s*reviews?',
                    r'(\d{3,})(?=\s|$|[^\d%])'        # 3+ digits not followed by % 
                ]
                
                for pattern in review_patterns:
                    matches = re.findall(pattern, container_text, re.IGNORECASE)
                    for match in matches:
                        potential_count = int(match.replace(',', ''))
                        # Reasonable range for review counts
                        if 10 <= potential_count <= 100000:
                            review_count = str(potential_count)
                            break
                    if review_count != "Not found":
                        break
            
            # If we found both in this container, we're done
            if rating != "Not found" and review_count != "Not found":
                break
        
        # Fallback: search the entire page if still not found
        if review_count == "Not found":
            text = soup.get_text()
            # More aggressive patterns for the full page
            review_patterns = [
                r'Reviews?\s*\((\d+(?:,\d+)*)\)',
                r'\((\d+(?:,\d+)*)\)\s*(?:reviews?|评论)',
                r'(\d+(?:,\d+)*)\s*(?:total\s*)?(?:reviews?|评论)',
                r'(\d{4})(?!\s*[%$€£¥])',  # 4 digit numbers not followed by currency/percent
            ]
            
            for pattern in review_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    potential_count = int(match.replace(',', ''))
                    if 100 <= potential_count <= 50000:  # Reasonable range
                        review_count = str(potential_count)
                        break
                if review_count != "Not found":
                    break
        
        # Fallback for rating if still not found
        if rating == "Not found":
            rating_selectors = [
                '[data-testid="rating"]',
                '.rating',
                '.stars-rating',
                '.rating-value',
                '.app-rating',
                '.star-rating'
            ]
            
            for selector in rating_selectors:
                element = soup.select_one(selector)
                if element:
                    text = element.get_text(strip=True)
                    rating_match = re.search(r'(\d+\.\d+)', text)
                    if rating_match:
                        potential_rating = float(rating_match.group(1))
                        if 0 <= potential_rating <= 5:
                            rating = rating_match.group(1)
                            break
        
        return review_count, rating
    
    def scrape_urls_from_file(self, input_file, output_file):
        """Scrape multiple URLs from input file and save to CSV"""
        urls = []
        
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                urls = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"Input file {input_file} not found!")
            return
        
        results = []
        
        print(f"Found {len(urls)} URLs to scrape...")
        
        for i, url in enumerate(urls, 1):
            print(f"Scraping {i}/{len(urls)}: {url}")
            
            result = self.extract_app_info(url)
            results.append(result)
            
            # Add delay to be respectful to the server
            time.sleep(1)
        
        # Save results to CSV
        fieldnames = ['url', 'name', 'description', 'category', 'pricing', 'review_count', 'rating']
        
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
        
        print(f"Results saved to {output_file}")
        return results

def main():
    parser = argparse.ArgumentParser(description='Scrape Shopify app information')
    parser.add_argument('input_file', help='Input file with URLs (one per line)')
    parser.add_argument('output_file', help='Output CSV file')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose logging')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    
    scraper = ShopifyAppScraper()
    scraper.scrape_urls_from_file(args.input_file, args.output_file)

if __name__ == "__main__":
    main()