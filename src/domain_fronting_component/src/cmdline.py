import argparse

def parse_args():
    parse = argparse.ArgumentParser(description='Domain Fronting')  
    parse.add_argument('-cdn', '--cdn_vendor', default='TencentCloud', type=str, help='cdn_vendor')
    parse.add_argument('-dns', '--dns_record_folder', default="data/dns_record", type=str, help='dns record folder')
    parse.add_argument('-cdn_dns', '--cdn_dns_record_folder', default="data/cdn_dns_record", type=str, help='cdn dns record folder')
    parse.add_argument('-fqdn', '--cdn_hosted_FQDN', default='data/cdn_hosted_FQDN', type=str, help='data/cdn_hosted_FQDN')
    parse.add_argument('-target_domain_url', '--target_domain_urls_folder', default='data/target_domain_urls', type=str, help='data/target_domain_urls_folder')
    parse.add_argument('-tuple', '--tuple_folder', default='data/tuple', type=str, help='data/tuple_folder')
    parse.add_argument('-abuse_tuple', '--abuse_tuple_folder', default='data/abuse_tuple', type=str, help='data/abuse_tuple_folder')
    args = parse.parse_args()  
    return args
