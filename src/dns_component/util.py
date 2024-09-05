import os
import glob
from tqdm import tqdm
import dns.resolver
import socket
import json
from cdn_map import cname_mapping, ns_mapping, check_CNAME, check_NS
from concurrent.futures import ThreadPoolExecutor

def get_dns_records(domain, dns_server=["8.8.8.8"]):
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [dns_server]

    try:
        ns_records = [str(record) for record in resolver.query(domain, 'NS')]
    except dns.exception.DNSException:
        ns_records = []

    try:
        cname_records = [str(record) for record in resolver.query(domain, 'CNAME')]

    except dns.exception.DNSException as e:
        print(f"Error querying CNAME records for domain {domain}: {str(e)}")
        cname_records = []

    try:
        a_records = [ip for ip in socket.gethostbyname_ex(domain)[2]]

    except socket.gaierror:
        a_records = []
    return ns_records, cname_records, a_records



def process_txt_file_to_get_dns_record(file_path, output_folder_path="dns_record"):

    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)
        
    result_dict = {}

    sld = os.path.splitext(os.path.basename(file_path))[0]

    with open(file_path, 'r') as file:
        lines = file.readlines()

        for line in lines:
            subdomain = line.strip('\n')
            ns_records, cname_records, a_records = get_dns_records(subdomain)

            result_dict[subdomain] = {
                "ns": ns_records,
                "cname": cname_records,
                "A": a_records
            }
    
    json_file_path = os.path.join(output_folder_path, f"{sld}.json")

    with open(json_file_path, 'w') as json_file:
        json.dump(result_dict, json_file, indent=2)


def process_folder_to_get_dns_record(input_folder_path, output_folder_path,n_thread):
    txt_files = [f for f in os.listdir(input_folder_path) if f.endswith('.txt')]
    total_files = len(txt_files)
    with ThreadPoolExecutor(max_workers=n_thread) as executor:
            for txt_file in tqdm(txt_files, desc="Processing Files", unit="file"):
                file_path = os.path.join(input_folder_path, txt_file)
                executor.submit(process_txt_file_to_get_dns_record, file_path,output_folder_path)

 



def get_cdn_ingeress_ip(input_json_file_path, output_folder_path="cdn_ingress_ip"):
    with open(input_json_file_path, 'r') as json_file:
        data = json.load(json_file)
    result_dict = {}

    sld = os.path.splitext(os.path.basename(input_json_file_path))[0]

    for subdomain, subdomain_info in data.items():
        
        ns_records = subdomain_info.get("ns", [])
        cname_records = subdomain_info.get("cname", [])
        a_records = subdomain_info.get("A", [])
        cdn_provider_cname = check_CNAME(cname_records)
        if cdn_provider_cname != "None":
            result_dict[subdomain] = {
                "method": "cname",
                "cdn" : cdn_provider_cname,
                "ns": ns_records,
                "cname": cname_records,
                "A": a_records
            }
        else:
            cdn_provider_ns = check_NS(ns_records)
            if cdn_provider_ns != "None":
              result_dict[subdomain] = {
                "method": "ns",
                "cdn" : cdn_provider_ns,
                "ns": ns_records,
                "cname": cname_records,
                "A": a_records
            }
              
    json_file_path = os.path.join(output_folder_path, f"{sld}.json")
    if result_dict != {}:
        with open(json_file_path, 'w') as json_file:
            json.dump(result_dict, json_file, indent=2)

def process_folder_to_get_cdn_ingress_ip(input_folder_path, output_folder_path="cdn_ingress_ip"):
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)
        

    txt_files = [f for f in os.listdir(input_folder_path) if f.endswith('.json')]

    for txt_file in txt_files:
        file_path = os.path.join(input_folder_path, txt_file)
        get_cdn_ingeress_ip(input_json_file_path=file_path, output_folder_path=output_folder_path)



def group_and_write_cdn_ip(input_folder_path, output_folder_path):
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    grouped_a_records = {}

    for filename in os.listdir(input_folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(input_folder_path, filename)

            with open(file_path, 'r') as json_file:
                data = json.load(json_file)

            for subdomain, subdomain_info in data.items():
                cdn = subdomain_info.get("cdn", [])
                a_records = subdomain_info.get("A", [])
                if cdn in grouped_a_records:
                    grouped_a_records[cdn] += a_records
                else:
                    grouped_a_records[cdn] = a_records
            
    for key, value in grouped_a_records.items():

        modified_key = key.replace('/', '_')
        
        json_file_path = os.path.join(output_folder_path, f"{modified_key.replace(' ', '_')}.json")
        Deduplicate_ip = list(set(value))
        with open(json_file_path, 'w') as json_file:
            json.dump({key: Deduplicate_ip}, json_file, indent=2)

    print("JSON file have been writen")




# if __name__ == "__main__":
#     process_folder_to_get_dns_record(folder_path="subdomain")
#     process_folder_to_get_cdn_ingress_ip(folder_path="dns_record")
#     group_and_write_cdn_ip(input_folder_path="cdn_ingress_ip", output_folder_path="grouped_cdn_ip")

