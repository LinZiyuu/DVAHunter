import os
import json
from cdn_map import cname_mapping, ns_mapping, check_CNAME, check_NS

class DataProcessor:
    def __init__(self, dns_record_folder_path , cdn_dns_record_folder_path, cdn_hosted_FQDN_folder_path):
        # Constructor method to initialize the DataProcessor class with input and output folder paths
        # self.input_folder_path = input_folder_path

        # self.output_folder_path = output_folder_path

        self.dns_record_folder_path = dns_record_folder_path
        self.cdn_dns_record_folder_path = cdn_dns_record_folder_path
        # self.cdn_ip_folder_path = cdn_ip_folder_path
        self.cdn_hosted_FQDN_folder_path = cdn_hosted_FQDN_folder_path
        

    def process_folder_to_get_cdn_dns_record(self):
        # Method to process the input folder and get the CDN ingress IP
        if not os.path.exists(self.cdn_dns_record_folder_path):
            os.makedirs(self.cdn_dns_record_folder_path)

        txt_files = [f for f in os.listdir(self.dns_record_folder_path) if f.endswith('.json')]
        # Get a list of all the .json files in the input folder

        # total_files = len(txt_files)  # Get the total number of .json files

        for txt_file in txt_files:
            file_path = os.path.join(self.dns_record_folder_path, txt_file)
            # Get the full file path by joining the input folder path and the file name

            self.get_cdn_dns_record(input_json_file_path=file_path)
            # Call the get_cdn_dns_record method with the file path as an argument

    def get_cdn_dns_record(self, input_json_file_path):
        # Method to get the CDN ingress IP from the input JSON file
        result_dict = {}  # Create an empty dictionary to store the results

        with open(input_json_file_path, 'r') as json_file:
            data = json.load(json_file)
            # Open the JSON file and load its contents into the data variable

        sld, _ = os.path.splitext(os.path.basename(input_json_file_path))
        # Get the base name of the file (without the extension) and assign it to the sld variable

        for subdomain, subdomain_info in data.items():
            # Iterate over each subdomain and its corresponding information in the data dictionary
            ns_records = subdomain_info.get("ns", [])  # Get the NS records for the subdomain
            cname_records = subdomain_info.get("cname", [])  # Get the CNAME records for the subdomain
            a_records = subdomain_info.get("A", [])  # Get the A records for the subdomain
            cname_err = subdomain_info.get("cname_err", [])  # Get the A records for the subdomain
            ns_err = subdomain_info.get("ns_err", [])  # Get the A records for the subdomain
            cdn_provider_cname = check_CNAME(cname_records)
            # Check if the subdomain has a CDN provider based on the CNAME records

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
              
        # Generate JSON file path based on output folder and SLD
        json_file_path = os.path.join(self.cdn_dns_record_folder_path, f"{sld}.json")
        if result_dict != {}:
            with open(json_file_path, 'w') as json_file:
                json.dump(result_dict, json_file, indent=2)

    # # def group_and_write_cdn_ip(self):
    # def classify_ip_by_cdn_vendors(self):
    #     # Method to group and write CDN IP addresses
    #     if not os.path.exists(self.cdn_ip_folder_path):
    #         os.makedirs(self.cdn_ip_folder_path)

    #     grouped_a_records = {}

    #     for filename in os.listdir(self.cdn_dns_record_folder_path):
    #         if filename.endswith(".json"):
    #             file_path = os.path.join(self.cdn_dns_record_folder_path, filename)

    #             with open(file_path, 'r') as json_file:
    #                 data = json.load(json_file)

    #             for subdomain, subdomain_info in data.items():
    #                 cdn = subdomain_info.get("cdn", [])
    #                 a_records = subdomain_info.get("A", [])
    #                 if cdn in grouped_a_records:
    #                     grouped_a_records[cdn] += a_records
    #                 else:
    #                     grouped_a_records[cdn] = a_records

    #     for key, value in grouped_a_records.items():
    #         # !这句fix CNAME MAP之后应该不要了
    #         # modified_key = key.replace('/', '_')
    #         # json_file_path = os.path.join(self.output_folder_path, f"{modified_key.replace(' ', '_')}.json")
    #         json_file_path = os.path.join(self.cdn_ip_folder_path, f"{key}.json")
    #         deduplicated_ip = list(set(value))
    #         with open(json_file_path, 'w') as json_file:
    #             json.dump({key: deduplicated_ip}, json_file, indent=2)


    # * 对FQDN按照CDN 厂商分类
    def classify_domain_names_by_cdn_vendors(self):
        # input = cdn_dns_record_folder_path
        # output = cdn_hosted_FQDN_folder_path
        # Create output folder if it doesn't exist
        if not os.path.exists(self.cdn_hosted_FQDN_folder_path):
            os.makedirs(self.cdn_hosted_FQDN_folder_path)

        # Dictionary to store A records grouped by (cdn_cname)
        classified_subdomain = {}

        # Iterate through JSON files in the input folder
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
            # * cdn_host_FQDN_json_file_path 表示每个cdn厂商的托管的域名列表
            cdn_host_FQDN_json_file_path = os.path.join(self.cdn_hosted_FQDN_folder_path, f"{key}.json")
            with open(cdn_host_FQDN_json_file_path, 'w') as json_file:
                json.dump({key: value}, json_file, indent=2)





    

if __name__ == "__main__":
    # This block of code will be executed only if the script is run directly (not imported as a module)
    print("starting")
 
    # dns_record_folder_path = os.path.join(os.getcwd(), "data/dns_record")
    # cdn_dns_record_folder_path = os.path.join(os.getcwd(), "data/cdn_dns_record")
    # cdn_ip_folder_path = os.path.join(os.getcwd(), "data/cdn_ingress_ip")
    # cdn_hosted_FQDN_folder_path = os.path.join(os.getcwd(), "data/cdn_hosted_FQDN")
    dns_record_folder_path = os.path.join(os.getcwd(), "data/tranco-top-1k-dns_record")
    cdn_dns_record_folder_path = os.path.join(os.getcwd(), "data/tranco-top-1k-cdn_dns_record")
    cdn_ip_folder_path = os.path.join(os.getcwd(), "data/tranco-top-1k-cdn_ingress_ip")
    cdn_hosted_FQDN_folder_path = os.path.join(os.getcwd(), "data/tranco-top-1k-cdn_hosted_FQDN")
    print(cdn_dns_record_folder_path)
    print(dns_record_folder_path)
    print(cdn_ip_folder_path)
    print(cdn_hosted_FQDN_folder_path)
    # input_folder_path="data/dns_record", output_folder_path="dara/cdn_dns_record"
    data_processor = DataProcessor(dns_record_folder_path, cdn_dns_record_folder_path,cdn_ip_folder_path, cdn_hosted_FQDN_folder_path)
    # Execute the process_folder_to_get_cdn_dns_record method
    data_processor.process_folder_to_get_cdn_dns_record()
    data_processor.classify_ip_by_cdn_vendors()
    data_processor.classify_domain_names_by_cdn_vendors()