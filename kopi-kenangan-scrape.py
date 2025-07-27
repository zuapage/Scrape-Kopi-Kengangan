from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import os
from datetime import datetime


def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver
    try:
        driver = webdriver.Chrome(options=chrome_options)
    except Exception as e:
        print(f"Error setting up Chrome driver: {e}")
        print("Pastikan ChromeDriver sudah terinstall dan ada di PATH")
        return None
    
    return driver

def find_elements_with_details(driver, url):
    """Fungsi untuk mengidentifikasi elemen-elemen di website"""
    
    print(f"Mengakses website: {url}")
    driver.get(url)
    

    time.sleep(5)
    
# Ambil screenshot pertama (full page)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_filename = f"kopi_kenangan_screenshot_{timestamp}.png"
    driver.save_screenshot(screenshot_filename)
    print(f"Screenshot disimpan: {screenshot_filename}")
    
    elements_found = []
    
# Daftar selector yang akan dicari
    selectors_to_find = [
        # Common HTML elements
        ("header", By.TAG_NAME, "header"),
        ("nav", By.TAG_NAME, "nav"),
        ("main", By.TAG_NAME, "main"),
        ("footer", By.TAG_NAME, "footer"),
        
        # Common class selectors
        ("logo", By.CLASS_NAME, "logo"),
        ("menu", By.CLASS_NAME, "menu"),
        ("navigation", By.CLASS_NAME, "navigation"),
        ("navbar", By.CLASS_NAME, "navbar"),
        ("content", By.CLASS_NAME, "content"),
        ("hero", By.CLASS_NAME, "hero"),
        ("banner", By.CLASS_NAME, "banner"),
        
        # Squarespace specific (karena website menggunakan Squarespace)
        ("squarespace", By.CSS_SELECTOR, "[class*='squarespace']"),
        ("sqs", By.CSS_SELECTOR, "[class*='sqs']"),
        
        # Form elements
        ("form", By.TAG_NAME, "form"),
        ("input", By.TAG_NAME, "input"),
        ("button", By.TAG_NAME, "button"),
        
        # Link elements
        ("links", By.TAG_NAME, "a"),
        
        # Image elements
        ("images", By.TAG_NAME, "img"),
        
        # Text elements
        ("headings_h1", By.TAG_NAME, "h1"),
        ("headings_h2", By.TAG_NAME, "h2"),
        ("headings_h3", By.TAG_NAME, "h3"),
        ("paragraphs", By.TAG_NAME, "p"),
        
        ("divs_with_id", By.CSS_SELECTOR, "div[id]"),
        ("divs_with_class", By.CSS_SELECTOR, "div[class]"),
    ]
    
    print("\n" + "="*50)
    print("ANALISIS ELEMEN WEBSITE KOPI KENANGAN")
    print("="*50)
    
    for name, by_method, selector in selectors_to_find:
        try:
            elements = driver.find_elements(by_method, selector)
            if elements:
                print(f"\n[{name.upper()}] - Ditemukan {len(elements)} elemen:")
                
                for i, element in enumerate(elements[:5]):  # Maksimal 5 elemen per kategori
                    try:
                        element_id = element.get_attribute("id")
                        element_class = element.get_attribute("class")
                        element_tag = element.tag_name
                        element_text = element.text[:50] + "..." if len(element.text) > 50 else element.text
                        
                        element_info = {
                            'category': name,
                            'index': i+1,
                            'tag': element_tag,
                            'id': element_id if element_id else "Tidak ada ID",
                            'class': element_class if element_class else "Tidak ada class",
                            'text': element_text.strip() if element_text.strip() else "Tidak ada text",
                            'xpath': driver.execute_script("return arguments[0].xpath || 'N/A';", element)
                        }
                        
                        elements_found.append(element_info)
                        
                        print(f"  {i+1}. Tag: {element_tag}")
                        print(f"      ID: {element_id if element_id else 'Tidak ada'}")
                        print(f"      Class: {element_class if element_class else 'Tidak ada'}")
                        print(f"      Text: {element_text.strip() if element_text.strip() else 'Tidak ada'}")
                        print(f"      ----")
                        
                    except Exception as e:
                        print(f"      Error mengambil detail elemen {i+1}: {e}")
                        
        except Exception as e:
            print(f"Error mencari elemen {name}: {e}")

    print(f"\n[PENCARIAN ID SPESIFIK]")
    potential_ids = [
        "header", "navigation", "nav", "menu", "logo", "main-content", 
        "content", "footer", "sidebar", "hero", "banner", "wrapper",
        "container", "main", "home", "page", "site"
    ]
    
    for potential_id in potential_ids:
        try:
            element = driver.find_element(By.ID, potential_id)
            print(f"  ✓ Ditemukan ID: '{potential_id}' - Tag: {element.tag_name}")
        except NoSuchElementException:
            continue
    
    return elements_found, screenshot_filename

def generate_report(elements_found, screenshot_filename):
    """Generate laporan dalam file text"""
    report_filename = f"kopi_kenangan_elements_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    with open(report_filename, 'w', encoding='utf-8') as f:
        f.write("="*60 + "\n")
        f.write("LAPORAN ANALISIS ELEMEN WEBSITE KOPI KENANGAN\n")
        f.write("="*60 + "\n")
        f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"URL: https://kopikenangan.com/\n")
        f.write(f"Screenshot: {screenshot_filename}\n")
        f.write(f"Total elemen ditemukan: {len(elements_found)}\n\n")
        
        current_category = ""
        for element in elements_found:
            if element['category'] != current_category:
                current_category = element['category']
                f.write(f"\n[{current_category.upper()}]\n")
                f.write("-" * 30 + "\n")
            
            f.write(f"Elemen #{element['index']}:\n")
            f.write(f"  Tag: {element['tag']}\n")
            f.write(f"  ID: {element['id']}\n")
            f.write(f"  Class: {element['class']}\n")
            f.write(f"  Text: {element['text']}\n")
            f.write("\n")
    
    print(f"\nLaporan detail disimpan: {report_filename}")
    return report_filename

def main():
    """Fungsi utama"""
    url = "https://kopikenangan.com/"
    
    driver = setup_driver()
    if not driver:
        return
    
    try:
        elements_found, screenshot_filename = find_elements_with_details(driver, url)
        
        report_filename = generate_report(elements_found, screenshot_filename)
        
        print(f"\n" + "="*50)
        print("RINGKASAN:")
        print(f"✓ Screenshot: {screenshot_filename}")
        print(f"✓ Laporan: {report_filename}")
        print(f"✓ Total elemen dianalisis: {len(elements_found)}")
        print("="*50)
        
        important_ids = [elem for elem in elements_found if elem['id'] != "Tidak ada ID"]
        if important_ids:
            print("\nID PENTING YANG DITEMUKAN:")
            for elem in important_ids[:10]:
                print(f"  - {elem['id']} ({elem['tag']})")
        
    except Exception as e:
        print(f"Error dalam proses utama: {e}")
    
    finally:
        # Tutup browser
        driver.quit()
        print("\nBrowser ditutup. Proses selesai!")

if __name__ == "__main__":
    main()
