import argparse

def parse_args():
    parse = argparse.ArgumentParser(description='Data Processer') 
    parse.add_argument('-df', '--dns_record_folder', default="data/test-dns_record", type=str, help='dns_record_folder')
    parse.add_argument('-cdf', '--cdn_dns_record_folder', default="data/test-cdn_dns_record", type=str, help='cdn_dns_record_folder')
    parse.add_argument('-cif', '--cdn_ip_folder', default="data/test-cdn_ingress_ip", type=str, help='cdn_ip_folder')
    parse.add_argument('-chdf', '--cdn_hosted_FQDN_folder', default="data/test-cdn_hosted_FQDN", type=str, help='cdn_hosted_FQDN_folder')
    args = parse.parse_args()  
    return args

