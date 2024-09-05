import json
from geoip2.database import Reader
import os
import subprocess
def get_ip_location(ip_address, database_path="src/domain_borrowing_component/src/GeoLite2-City.mmdb"):
     with Reader(database_path) as reader:
        try:
            response = reader.city(ip_address)
            city = response.city.name
            return city
        except Exception as e:
            print(f"Error: {e}")
            return None
        

def process_ips(input_file_path,cdn_vendor,cdn_ingress_ip_gourped_by_city_folder_path):
    
    if not os.path.exists(cdn_ingress_ip_gourped_by_city_folder_path):
        os.makedirs(cdn_ingress_ip_gourped_by_city_folder_path)
    output_file_path = os.path.join(cdn_ingress_ip_gourped_by_city_folder_path, f"{cdn_vendor}.json")
    print(output_file_path)
    with open(input_file_path, "r") as file:
        json_data = json.load(file)
    result = {}
    for provider, ips in json_data.items():
        result[provider] = {}
        for ip in ips:
            city = get_ip_location(ip)
            if city is not None:
                if city not in result[provider]:
                    result[provider][city] = []
                result[provider][city].append(ip)
    with open(output_file_path, "w") as file:
        json.dump(result, file, indent=2)
    return result

def check_valid_ip(input_file_name, output_file_name):
    input_file_path = os.path.join(os.getcwd(), input_file_name)
    output_file_path = os.path.join(os.getcwd(), output_file_name)
    with open(input_file_path, 'r') as file:
        data = json.load(file)
    invalid_ips = set()
    for provider, locations in data.items():
        for location, ips in locations.items():
            for ip in ips:
                curl_command = f'curl -I http://{ip}/'

                try:
                    result = subprocess.check_output(curl_command, shell=True, stderr=subprocess.STDOUT)
                    result = result.decode('utf-8')
                    # TODO 
                    if 'Server: CFS 1124' not in result:
                        print(f'IP {ip} 不符合条件: {result}')
                        invalid_ips.add(ip)
                    
                except subprocess.CalledProcessError as e:
                    print(f'发生错误: {e}')

    for provider, locations in data.items():
        for location, ips in locations.items():
            data[provider][location] = [ip for ip in ips if ip not in invalid_ips]

    for provider, locations in data.items():
        locations_to_delete = [location for location, ips in locations.items() if not ips]
        for location in locations_to_delete:
            del locations[location]
        
    with open(output_file_path, 'w') as file:
        json.dump(data, file, indent=2)


# if __name__ == "__main__":
#     cdn_ingress_ip_folder_path = os.path.join(os.getcwd(), "data/cdn_ingress_ip")
#     cdn_ingress_ip_gourped_by_city_folder_path =  os.path.join(os.getcwd(), "data/cdn_ingress_ip_gourped_by_city")
#     file_name = "Qiniu.json"
#     file_path = os.path.join(cdn_ingress_ip_folder_path,file_name)
#     print(file_path)
#     process_ips(input_file_path=file_path,output_file_name=file_name)