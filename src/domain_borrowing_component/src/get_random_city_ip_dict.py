import os
import json
import random

def get_random_city_ip_dict(cdn_ingress_ip_gourped_by_city_folder_path,num_selected_nodes=1,cdn_vendor="Fastly"):

    file_path = os.path.join(cdn_ingress_ip_gourped_by_city_folder_path, f"{cdn_vendor}.json")
    with open(file_path, 'r') as file:
        data = json.load(file)

    cdn_ingress_ips = data.get(cdn_vendor, {})

    random_city_ip_dict = {}

    num_selected_nodes = 1 

    for city, ips in cdn_ingress_ips.items():

        selected_ips = random.sample(ips, num_selected_nodes) if ips else []

        random_city_ip_dict[city] = selected_ips


    return random_city_ip_dict


# if __name__ == "__main__":
#     cdn_ingress_ip_gourped_by_city_folder_path =  os.path.join(os.getcwd(), "data/cdn_ingress_ip_gourped_by_city")
#     random_city_ip_dict= get_random_city_ip_dict(cdn_ingress_ip_gourped_by_city_folder_path=cdn_ingress_ip_gourped_by_city_folder_path,num_selected_nodes=1,cdn_vendor="CDN77")
#     print(random_city_ip_dict)