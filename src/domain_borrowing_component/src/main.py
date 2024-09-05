
from util import generate_http_request_header_00, send_http_request, check_error, get_cname_records, read_json_file, read_txt_file, check_borrowed, write_result

import os, json
from cmdline import parse_args
import time
from check_host import check_borrowed_all
from concurrent.futures import ThreadPoolExecutor
import multiprocessing
from get_random_city_ip_dict import get_random_city_ip_dict
from cmdline import parse_args
from get_host import get_all_FQDN, get_no_hosted_FQDN
from group_ips_by_city import process_ips, check_valid_ip
from data_processer import DataProcessor


def check_borrowed_worker(args):

    host, ingress_ip, target_port, traget_request, cdn_vendor = args
    status_code, headers, body = send_http_request(ip=ingress_ip, port=target_port, request=traget_request)

    borrowed_flag = check_borrowed_all(host, status_code, headers, body, cdn_vendor)
    return host, borrowed_flag, ingress_ip


def check_a_host(host,ingress_ips_list, target_port, cdn_vendor, domain_borrowed_dict):
    traget_request = generate_http_request_header_00(host)

    borrowed_ingress_ip = []
    for ingress_ip in ingress_ips_list:

        print(f"ingress ip:{ingress_ip}, domain: {host}")
        status_code, headers, body = send_http_request(ip=ingress_ip, port=target_port, request=traget_request)
        time.sleep(1)
        borrowed_flag = check_borrowed_all(host, status_code, headers, body, cdn_vendor)
        if borrowed_flag == True:
            borrowed_ingress_ip.append(ingress_ip)
            break
    if borrowed_ingress_ip != []:
        domain_borrowed_dict[host] = borrowed_ingress_ip

def main():

    args = parse_args()
    subdomain_folder, dns_record_folder, cdn_dns_record_folder,cdn_hosted_fqdn_folder,fqdn_file, domain_no_host_by_cdn_file, cdn_vendor, cdn_ingress_ip_folder, cdn_ingress_ip_gourped_by_city_folder, domain_borrowed_folder_path = args.subdomain_folder, args.dns_record_folder, args.cdn_dns_record_folder, args.cdn_hosted_fqdn_folder,args.fqdn_file, args.domain_no_host_by_cdn_file,  args.cdn_vendor, args.cdn_ingress_ip_folder, args.cdn_ingress_ip_gourped_by_city_folder, args.domain_borrowed_folder_path

    subdomain_folder_path = os.path.join(os.getcwd(), subdomain_folder)
    all_host_path = os.path.join(os.getcwd(), fqdn_file)
    domain_no_host_by_cdn_file_path = os.path.join(os.getcwd(), domain_no_host_by_cdn_file)
    cdn_ingress_ip_folder_path = os.path.join(os.getcwd(),  cdn_ingress_ip_folder)
    cdn_ingress_ip_gourped_by_city_folder_path =  os.path.join(os.getcwd(),cdn_ingress_ip_gourped_by_city_folder)
    dns_record_folder_path = os.path.join(os.getcwd(), dns_record_folder)
    cdn_dns_record_folder_path = os.path.join(os.getcwd(), cdn_dns_record_folder)
    cdn_hosted_FQDN_folder_path = os.path.join(os.getcwd(), cdn_hosted_fqdn_folder)
    print(f"subdomain_folder_path:{subdomain_folder_path}")
    print(f"dns_record_folder_path:{dns_record_folder_path}")
    print(f"cdn_dns_record_folder_path:{cdn_dns_record_folder_path}")
    print(f"cdn_hosted_FQDN_folder_path:{cdn_hosted_FQDN_folder_path}")
    print(f"all_host_path:{all_host_path}")
    print(f"domain_no_host_by_cdn_file_path:{domain_no_host_by_cdn_file_path}")
    print(f"cdn_ingress_ip_folder_path:{cdn_ingress_ip_folder_path}")
    print(f"cdn_ingress_ip_gourped_by_city_folder_path:{cdn_ingress_ip_gourped_by_city_folder_path}")

    


    data_processor = DataProcessor(dns_record_folder_path=dns_record_folder_path, cdn_dns_record_folder_path=cdn_dns_record_folder_path,cdn_ip_folder_path=cdn_ingress_ip_folder_path, cdn_hosted_FQDN_folder_path=cdn_hosted_FQDN_folder_path)

    data_processor.process_folder_to_get_cdn_dns_record()
    data_processor.classify_ip_by_cdn_vendors()
    data_processor.classify_domain_names_by_cdn_vendors()

    get_all_FQDN(input_folder=subdomain_folder_path, output_file=all_host_path)

    get_no_hosted_FQDN(cdn_vendor=cdn_vendor, all_FQDN_file=all_host_path,cdn_hosted_FQDN_folder_path=cdn_hosted_FQDN_folder_path,all_host_folaer_path=os.path.dirname(all_host_path))


    with open(domain_no_host_by_cdn_file_path, 'r') as f:
        domain_no_host_by_cdn = json.load(f)
    domain_no_host_by_cdn_list = domain_no_host_by_cdn[cdn_vendor]


    cdn_ingress_ip_file_path = os.path.join(cdn_ingress_ip_folder_path, f"{cdn_vendor}.json")


    process_ips(input_file_path=cdn_ingress_ip_file_path,cdn_vendor=cdn_vendor,cdn_ingress_ip_gourped_by_city_folder_path=cdn_ingress_ip_gourped_by_city_folder_path)
    check_valid_ip(input_file_name=f"{cdn_ingress_ip_gourped_by_city_folder_path}/{cdn_vendor}.json",output_file_name=f"{cdn_ingress_ip_gourped_by_city_folder_path}/{cdn_vendor}.json")
    random_city_ip_dict = get_random_city_ip_dict(cdn_ingress_ip_gourped_by_city_folder_path=cdn_ingress_ip_gourped_by_city_folder_path,num_selected_nodes=1,cdn_vendor=cdn_vendor)
    ingress_ips_list = [ip for ips in random_city_ip_dict.values() for ip in ips]
    target_port = 80
    domain_borrowed_dict = {}
    start_time = time.time()
    num_processes = 32
    pool = multiprocessing.Pool(processes=num_processes)


    for host in domain_no_host_by_cdn_list:
        # TODO with ethical的 information
        traget_request = generate_http_request_header_00(host)

        args_list = [(host, ingress_ip, target_port, traget_request, cdn_vendor) for ingress_ip in ingress_ips_list]

        results = pool.map(check_borrowed_worker, args_list)
        

        borrowed_ingress_ip = [ingress_ip for host,  borrowed_flag ,ingress_ip in results if borrowed_flag]
        if borrowed_ingress_ip:
            domain_borrowed_dict[host] = borrowed_ingress_ip

    pool.close()
    pool.join()

    end_time = time.time()

    execution_time = end_time - start_time

    print(f"execution_time:{execution_time} s")

    if not os.path.exists(domain_borrowed_folder_path):
        os.makedirs(domain_borrowed_folder_path)
    domain_borrowed_file_path = os.path.join(domain_borrowed_folder_path, f"{cdn_vendor}.json")
    print(domain_borrowed_file_path)

    with open(domain_borrowed_file_path , 'w') as json_file:
        json.dump(domain_borrowed_dict, json_file, indent=2)
if __name__ == "__main__":
    main()