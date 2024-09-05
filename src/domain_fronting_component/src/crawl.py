from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os, time
import json
from urllib.parse import urlparse
from multiprocessing import Pool, cpu_count
import random

def initialize_webdriver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.binary_location = '/usr/bin/google-chrome'
    chromedriver_path = '/usr/local/bin/chromedriver'  
    driver = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)
    return driver

def crawl_static_file_urls(driver, output_folder_path, cdn_vendor,domain,num_urls_to_crawl):
    try:
        base_domain = f"https://{domain}"
        driver.get(base_domain)


        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.TAG_NAME, 'a')))
    


        time.sleep(1)

        static_file_urls = set()
        num_urls_crawled = 0

        elements = driver.find_elements(By.TAG_NAME, 'a')
        for element in elements:
            href = element.get_attribute('href')
            if is_valid_url(href, domain) and (href.endswith('.js') or href.endswith('.css') or href.endswith('.html') or href.endswith('.htm') or href.endswith('.xml') 
                        or href.endswith('.jpg') or href.endswith('.png') or href.endswith('.gif') or href.endswith('.bmp') or href.endswith('.svg') 
                        or href.endswith('.json')):
                static_file_urls.add(href)
                num_urls_crawled += 1

                if num_urls_crawled >= num_urls_to_crawl:
                    break  
        if not os.path.exists(output_folder_path):
            os.makedirs(output_folder_path)
        cdn_folder_path = os.path.join(output_folder_path, cdn_vendor)
        if not os.path.exists(cdn_folder_path):
            os.makedirs(cdn_folder_path)
        txt_file_path = os.path.join(cdn_folder_path, f"{domain}.txt")
        if len(static_file_urls) > 0: 
            with open(txt_file_path, 'w') as file:
                for url in static_file_urls:
                    file.write(url + '\n')
    except Exception as e:
        print(e)

def read_json_file(input_folder_path, file_name):
    file_path = os.path.join(input_folder_path, file_name)
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def process_domain(cdn_vendor, domain, num_urls_to_crawl, target_domain_urls_folder_path):
    driver = initialize_webdriver()
    crawl_static_file_urls(driver, target_domain_urls_folder_path, cdn_vendor, domain, num_urls_to_crawl)
    driver.quit()



def get_static_file_urls(cdn_vendor,cral_domain_num,num_urls_to_crawl=10,target_domain_urls_folder_path="Target_Domain_Urls",CDN_Serverd_Domain_List_folder_path="CDN_Serverd_Domain_List"):
    data = read_json_file(input_folder_path=CDN_Serverd_Domain_List_folder_path, file_name=f"{cdn_vendor}.json")
    cdn_served_domain_list = data[cdn_vendor]
    cdn_served_domain_list = cdn_served_domain_list[:1000]
    random.shuffle(cdn_served_domain_list)
    driver = initialize_webdriver()
    cdn_target_domain_urls_folder_paht = os.path.join(target_domain_urls_folder_path,cdn_vendor )
    for domain in cdn_served_domain_list:
        print(domain)
        valid_domain_num = count_files_in_folder(folder_path=cdn_target_domain_urls_folder_paht)
        if valid_domain_num == cral_domain_num:
            break
        else:
            crawl_static_file_urls(driver, target_domain_urls_folder_path, cdn_vendor, domain, num_urls_to_crawl)

    driver.quit()

def is_valid_url(url, domain):
    parsed_url = urlparse(url)
    return parsed_url.netloc == domain


def count_files_in_folder(folder_path):
    try:
        # List all files in the folder
        files = os.listdir(folder_path)
        
        # Count the number of files
        file_count = len(files)
        

        return file_count
    except Exception as e:

        return 0

# if __name__ == "__main__":
#     # output_folder_path = "Target_Domain_Urls"
#     # cdn_vendor = "TencentCloud"
#     # num_urls_to_crawl = 10
#     # data = read_json_file(input_folder_path="CDN_Serverd_Domain_List", file_name="TencentCloud.json")
#     # urls = data[cdn_vendor][:3]

#     # # Initialize WebDriver
#     # driver = initialize_webdriver()
#     # for url in urls:
#     #     # Crawl URLs
#     #     crawl_static_file_urls(driver, output_folder_path, cdn_vendor, url, num_urls_to_crawl)

#     # # Quit the WebDriver when done with all URLs
#     # driver.quit()
#     # get_static_file_urls(cdn_vendor="TencentCloud")
#     get_static_file_urls(cdn_vendor="BunnyCDN",cral_domain_num=10, num_urls_to_crawl=10, target_domain_urls_folder_path="Target_Domain_Urls", CDN_Serverd_Domain_List_folder_path="CDN_Serverd_Domain_List")