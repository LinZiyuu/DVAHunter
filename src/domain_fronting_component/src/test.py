from data_processer import DataProcessor
import os

if __name__ == "__main__":
    # This block of code will be executed only if the script is run directly (not imported as a module)
    print("starting")
 
    dns_record_folder_path = os.path.join(os.getcwd(), "data/dns_record")
    cdn_dns_record_folder_path = os.path.join(os.getcwd(), "data/cdn_dns_record")
    cdn_ip_folder_path = os.path.join(os.getcwd(), "data/cdn_ingress_ip")
    cdn_hosted_FQDN_folder_path = os.path.join(os.getcwd(), "data/cdn_hosted_FQDN")
    print(cdn_dns_record_folder_path)
    print(dns_record_folder_path)
    print(cdn_ip_folder_path)
    print(cdn_hosted_FQDN_folder_path)
    # input_folder_path="data/dns_record", output_folder_path="dara/cdn_dns_record"
    data_processor = DataProcessor(dns_record_folder_path, cdn_dns_record_folder_path,cdn_ip_folder_path, cdn_hosted_FQDN_folder_path)
    # Execute the process_folder_to_get_cdn_dns_record method
    data_processor.process_folder_to_get_cdn_dns_record()
    # data_processor.classify_ip_by_cdn_vendors()
    data_processor.classify_domain_names_by_cdn_vendors()