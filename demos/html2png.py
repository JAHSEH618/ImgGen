#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML to PNG Converter
Supports converting from HTML file or HTML string to PNG image
"""

import sys
from pathlib import Path


def html_to_png_selenium(html_content, output_path, width=1920, height=1080):
    """
    Convert HTML to PNG using Selenium
    Installation: pip install selenium
    """
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    import time

    # Create temporary HTML file
    temp_html = Path("temp_convert.html")
    if not html_content.strip().startswith('<'):
        # If it's a file path
        temp_html = Path(html_content)
    else:
        # If it's HTML string
        temp_html.write_text(html_content, encoding='utf-8')

    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument(f'--window-size={width},{height}')

    # Create browser instance
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Load HTML file
        driver.get(f'file://{temp_html.absolute()}')
        time.sleep(1)  # Wait for page to load

        # Take screenshot
        driver.save_screenshot(output_path)
        print(f"Success: PNG saved to {output_path}")

    finally:
        driver.quit()
        # Clean up temporary file
        if html_content.strip().startswith('<') and temp_html.exists():
            temp_html.unlink()


def html_to_png_html2image(html_content, output_path, width=1920, height=1080):
    """
    Convert HTML to PNG using html2image (Recommended)
    Installation: pip install html2image
    """
    from html2image import Html2Image

    hti = Html2Image()
    hti.output_path = str(Path(output_path).parent)

    # Check if it's HTML string or file path
    if html_content.strip().startswith('<'):
        # HTML string
        hti.screenshot(
            html_str=html_content,
            save_as=Path(output_path).name,
            size=(width, height)
        )
    else:
        # HTML file path
        html_file = Path(html_content)
        if not html_file.exists():
            raise FileNotFoundError(f"HTML file not found: {html_content}")

        hti.screenshot(
            html_file=str(html_file),
            save_as=Path(output_path).name,
            size=(width, height)
        )

    print(f"Success: PNG saved to {output_path}")


def html_to_png_playwright(html_content, output_path, width=1920, height=1080):
    """
    Convert HTML to PNG using Playwright (Modern solution)
    Installation: pip install playwright && playwright install chromium
    """
    from playwright.sync_api import sync_playwright

    # Create temporary HTML file
    temp_html = Path("temp_convert.html")
    if not html_content.strip().startswith('<'):
        # If it's a file path
        temp_html = Path(html_content)
    else:
        # If it's HTML string
        temp_html.write_text(html_content, encoding='utf-8')

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': width, 'height': height})

        # Load HTML
        page.goto(f'file://{temp_html.absolute()}')

        # Take screenshot
        page.screenshot(path=output_path, full_page=True)

        browser.close()

    print(f"Success: PNG saved to {output_path}")

    # Clean up temporary file
    if html_content.strip().startswith('<') and temp_html.exists():
        temp_html.unlink()


def main():
    """Main function with usage examples"""

    # Example 1: Simple HTML string
    html_string = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .container {
                background: white;
                padding: 40px;
                border-radius: 10px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                text-align: center;
            }
            h1 {
                color: #667eea;
                margin: 0 0 20px 0;
            }
            p {
                color: #666;
                font-size: 18px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>HTML to PNG Example</h1>
            <p>This is a demo of converting HTML to PNG</p>
            <p>Supports CSS styles and layouts</p>
        </div>
    </body>
    </html>
    """

    print("HTML to PNG Converter\n")
    print("=" * 50)

    # Select method
    print("\nAvailable conversion methods:")
    print("1. html2image (Recommended, easy to use)")
    print("2. selenium (Requires Chrome browser)")
    print("3. playwright (Modern solution)")

    choice = input("\nSelect method (1/2/3) [default: 1]: ").strip() or "1"

    output_file = "output.png"

    try:
        if choice == "1":
            print("\nConverting with html2image...")
            html_to_png_html2image(html_string, output_file, width=1200, height=800)
        elif choice == "2":
            print("\nConverting with selenium...")
            html_to_png_selenium(html_string, output_file, width=1200, height=800)
        elif choice == "3":
            print("\nConverting with playwright...")
            html_to_png_playwright(html_string, output_file, width=1200, height=800)
        else:
            print("Invalid choice")
            return

        print(f"\nConversion successful! Check: {Path(output_file).absolute()}")

    except ImportError as e:
        print(f"\nMissing dependency: {e}")
        print("\nInstallation instructions:")
        print("  Method 1: pip install html2image")
        print("  Method 2: pip install selenium")
        print("  Method 3: pip install playwright && playwright install chromium")
    except Exception as e:
        print(f"\nConversion failed: {e}")


if __name__ == "__main__":
    # If command line arguments provided, use them
    if len(sys.argv) > 1:
        input_html = sys.argv[1]
        output_png = sys.argv[2] if len(sys.argv) > 2 else "output.png"

        # Use html2image by default
        try:
            if Path(input_html).exists():
                print(f"Converting file: {input_html} -> {output_png}")
                html_to_png_html2image(input_html, output_png)
            else:
                print(f"Converting HTML string -> {output_png}")
                html_to_png_html2image(input_html, output_png)
        except Exception as e:
            print(f"Conversion failed: {e}")
    else:
        # Interactive mode
        main()