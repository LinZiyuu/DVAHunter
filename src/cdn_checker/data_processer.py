import os
import json
from cdn_map import cname_mapping, ns_mapping, check_CNAME, check_NS

class DataProcessor:
    def __init__(self, dns_record_folder_path , cdn_dns_record_folder_path, cdn_ip_folder_path, cdn_hosted_FQDN_folder_path):
        self.dns_record_folder_path = dns_record_folder_path
        self.cdn_dns_record_folder_path = cdn_dns_record_folder_path
        self.cdn_ip_folder_path = cdn_ip_folder_path
        self.cdn_hosted_FQDN_folder_path = cdn_hosted_FQDN_folder_path
        

    def process_folder_to_get_cdn_dns_record(self):
        if not os.path.exists(self.cdn_dns_record_folder_path):
            os.makedirs(self.cdn_dns_record_folder_path)

        txt_files = [f for f in os.listdir(self.dns_record_folder_path) if f.endswith('.json')]

        for txt_file in txt_files:
            file_path = os.path.join(self.dns_record_folder_path, txt_file)

            self.get_cdn_dns_record(input_json_file_path=file_path)

    def get_cdn_dns_record(self, input_json_file_path):
        result_dict = {}  

        with open(input_json_file_path, 'r') as json_file:
            data = json.load(json_file)

        sld, _ = os.path.splitext(os.path.basename(input_json_file_path))

        for subdomain, subdomain_info in data.items():
            ns_records = subdomain_info.get("ns", [])  
            cname_records = subdomain_info.get("cname", []) 
            a_records = subdomain_info.get("A", []) 
            cname_err = subdomain_info.get("cname_err", [])  
            ns_err = subdomain_info.get("ns_err", [])  
            cdn_provider_cname = check_CNAME(cname_records)

            if cdn_provider_cname != "None":
                result_dict[subdomain] = {
                "method": "cname",
                "cdn" : cdn_provider_cname,
                "ns": ns_records,
                "cname": cname_records,
                "A": a_records,
                "cname_err": cname_err,
                "ns_err": ns_err
            }
            else:
                cdn_provider_ns = check_NS(ns_records)
                if cdn_provider_ns != "None":
                    result_dict[subdomain] = {
                    "method": "ns",
                    "cdn" : cdn_provider_ns,
                    "ns": ns_records,
                    "cname": cname_records,
                    "A": a_records,
                    "cname_err": cname_err,
                    "ns_err": ns_err
                }


        json_file_path = os.path.join(self.cdn_dns_record_folder_path, f"{sld}.json")
        if result_dict != {}:
            with open(json_file_path, 'w') as json_file:
                json.dump(result_dict, json_file, indent=2)

    def classify_ip_by_cdn_vendors(self):
        if not os.path.exists(self.cdn_ip_folder_path):
            os.makedirs(self.cdn_ip_folder_path)

        grouped_a_records = {}

        for filename in os.listdir(self.cdn_dns_record_folder_path):
            if filename.endswith(".json"):
                file_path = os.path.join(self.cdn_dns_record_folder_path, filename)

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
            json_file_path = os.path.join(self.cdn_ip_folder_path, f"{key}.json")
            deduplicated_ip = list(set(value))
            with open(json_file_path, 'w') as json_file:
                json.dump({key: deduplicated_ip}, json_file, indent=2)



    def classify_domain_names_by_cdn_vendors(self):
        if not os.path.exists(self.cdn_hosted_FQDN_folder_path):
            os.makedirs(self.cdn_hosted_FQDN_folder_path)

        classified_subdomain = {}

        for filename in os.listdir(self.cdn_dns_record_folder_path):
            if filename.endswith(".json"):
                file_path = os.path.join(self.cdn_dns_record_folder_path, filename)
                with open(file_path, 'r') as json_file:
                    data = json.load(json_file)
                for subdomain, subdomain_info in data.items():
                    cdn = subdomain_info.get("cdn", [])
                    if cdn in classified_subdomain:
                        classified_subdomain[cdn].append(subdomain)
                    else:
                        classified_subdomain[cdn] = []
                        classified_subdomain[cdn].append(subdomain)
                
        for key, value in classified_subdomain.items():
            cdn_host_FQDN_json_file_path = os.path.join(self.cdn_hosted_FQDN_folder_path, f"{key}.json")
            with open(cdn_host_FQDN_json_file_path, 'w') as json_file:
                json.dump({key: value}, json_file, indent=2)
