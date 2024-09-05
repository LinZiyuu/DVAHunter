import os
import random
import json

def read_file_into_list(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return [line.strip('\n') for line in lines]

def generate_a_tuple(dt, domain_list,cdn_folder_path):

    df = dt
    while df == dt:
        df = random.choice(domain_list)

    dt_file_path = os.path.join(cdn_folder_path, f"{dt}.txt")   

    # Read the URLs from the dt file into a list
    url_list = read_file_into_list(dt_file_path)

    # Ensure there is at least 1 URL
    if len(url_list) < 1:
        raise ValueError("No URLs in the dt file.")

    # Randomly select a URL
    ut = random.choice(url_list)
    # print(f"Selected URL: {ut}")
    # Remove 'https://dt' from the URL
    ut = ut.replace(f'https://{dt}', '')

    # print(f"Modified URL: {ut}")
    return (df, dt, ut)

def generate_tuple(cdn_vendor, fronting_test_case_num, target_domain_urls_folder_path):

    if not os.path.exists(target_domain_urls_folder_path):
        os.makedirs(target_domain_urls_folder_path)
    cdn_folder_path = os.path.join(target_domain_urls_folder_path, cdn_vendor)
    if not os.path.exists(cdn_folder_path):
        os.makedirs(cdn_folder_path)

    txt_files = [f for f in os.listdir(cdn_folder_path) if f.endswith(".txt")]

    domains_file_path = os.path.join(target_domain_urls_folder_path, f"{cdn_vendor}_domains.txt")

    valid_domain_num = len(txt_files)
    if valid_domain_num < fronting_test_case_num:
        fronting_test_case_num = valid_domain_num

    with open(domains_file_path, "w") as domains_file:
        for txt_file in txt_files:

            domain_name = os.path.splitext(txt_file)[0]
            domains_file.write(domain_name + "\n")

    Valid_CDN_Serverd_Domain_path = os.path.join(target_domain_urls_folder_path, f"{cdn_vendor}_domains.txt")

    domain_list = read_file_into_list(Valid_CDN_Serverd_Domain_path)


    tuple_list = []
    for domain in domain_list:
        dt = domain
        fronting_test_tuple = generate_a_tuple(dt, domain_list,cdn_folder_path)

        tuple_list.append(fronting_test_tuple)
    return tuple_list

def write_tuples_to_json(cdn_vendor, tuples, tuple_folder_path="Tuple"):
    if not os.path.exists(tuple_folder_path):
        os.makedirs(tuple_folder_path)
    json_file_path = os.path.join(tuple_folder_path, f"{cdn_vendor}.json")
    with open(json_file_path, "w") as json_file:
        json.dump(tuples, json_file, indent=2)


def get_tuples_from_json(cdn_vendor, tuple_folder_path="Tuple"):
    json_file_path = os.path.join(tuple_folder_path, f"{cdn_vendor}.json")
    with open(json_file_path, "r") as json_file:
        tuples = json.load(json_file)
    return tuples




# if __name__ == "__main__":
#     tuples = generate_tuple(cdn_vendor="TencentCloud", target_domain_urls_folder_path="Target_Domain_Urls")
#     print(tuples)
#     write_tuples_to_json(tuples=tuples,tuple_folder_path="Tuple", cdn_vendor="TencentCloud")