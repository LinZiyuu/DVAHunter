import argparse

def parse_args():

    parse = argparse.ArgumentParser(description='Domain Borrowing Finder') 
    parse.add_argument('-subdomain', '--subdomain_folder', default='data/test-subdomain', type=str, help='subdomain_folder_path')
    parse.add_argument('-dns_record', '--dns_record_folder', default='data/test-dns_record', type=str, help='dns_record_folder_path')
    parse.add_argument('-cdn_dns_record', '--cdn_dns_record_folder', default='data/test-cdn_dns_record', type=str, help='cdn_dns_record_folder_path')
    parse.add_argument('-cdn_hosted_fqdn', '--cdn_hosted_fqdn_folder', default='data/test-cdn_hosted_FQDN', type=str, help='cdn_hosted_fqdn_folder_path')
    parse.add_argument('-fqdn', '--fqdn_file', default='data/all_FQDN/test-subdomain.txt', type=str, help='all_host_folder_path')
    parse.add_argument('-host', '--domain_no_host_by_cdn_file', default='data/test-all_FQDN/Fastly.json', type=str, help='domain_no_host_by_cdn_file')
    parse.add_argument('-cdn', '--cdn_vendor', default='Fastly', type=str, help='cdn_vendor')
    parse.add_argument('-cdn_ip', '--cdn_ingress_ip_folder', default='data/test-cdn_ingress_ip', type=str, help='cdn_ingress_ip_folder')
    parse.add_argument('-g_cdn_ip', '--cdn_ingress_ip_gourped_by_city_folder', default='data/test-cdn_ingress_ip_gourped_by_city', type=str, help='cdn_ingress_ip_gourped_by_city_folder')
    parse.add_argument('-db', '--domain_borrowed_folder_path', default='data/test-Domain_Borrowed', type=str, help='domain_borrowed_folder_path')


    args = parse.parse_args()  
    return args