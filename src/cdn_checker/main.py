from cmdline import parse_args
from data_processer import DataProcessor
import os

if __name__ == "__main__":

    args = parse_args()
    dns_record_folder, cdn_dns_record_folder, cdn_ip_folder, cdn_hosted_FQDN_folder = args.dns_record_folder, args.cdn_dns_record_folder, args.cdn_ip_folder, args.cdn_hosted_FQDN_folder

    dns_record_folder_path = os.path.join(os.getcwd(), dns_record_folder)
    cdn_dns_record_folder_path = os.path.join(os.getcwd(), cdn_dns_record_folder)
    cdn_ip_folder_path = os.path.join(os.getcwd(), cdn_ip_folder)
    cdn_hosted_FQDN_folder_path = os.path.join(os.getcwd(), cdn_hosted_FQDN_folder)

    print(dns_record_folder)
    print(cdn_dns_record_folder)
    print(cdn_ip_folder_path)
    print(cdn_hosted_FQDN_folder_path)

    data_processor = DataProcessor(dns_record_folder_path, cdn_dns_record_folder_path,cdn_ip_folder_path, cdn_hosted_FQDN_folder_path)
    data_processor.process_folder_to_get_cdn_dns_record()
    data_processor.classify_ip_by_cdn_vendors()
    data_processor.classify_domain_names_by_cdn_vendors()