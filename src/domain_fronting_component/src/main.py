from tuple_generater import generate_tuple, write_tuples_to_json
from tester import fronting_tester
from crawl import get_static_file_urls
import os
import json
import multiprocessing
import time
from cmdline import parse_args
from data_processer import DataProcessor

def fronting_tester_wrapper(fronting_tuple):
    Df, Dt, Ut = fronting_tuple
    abuse_tuple = fronting_tester(Df=Df, Dt=Dt, Ut=Ut)
    return abuse_tuple

def write_abuse_tuples_to_json(cdn_vendor, tuples, abuse_folder_path):
    if not os.path.exists(abuse_folder_path):
        os.makedirs(abuse_folder_path)
    aubse_cdn_path = os.path.join(abuse_folder_path, f"{cdn_vendor}.json")
    with open(aubse_cdn_path, "w") as json_file:
        json.dump(tuples, json_file, indent=2)

if __name__ == "__main__":

    args = parse_args()
    cdn_vendor,  dns_record, cdn_dns_record ,cdn_hosted_FQDN, target_domain_urls_folder, tuple_folder, abuse_tuple_folder = args.cdn_vendor, args.dns_record_folder, args.cdn_dns_record_folder, args.cdn_hosted_FQDN, args.target_domain_urls_folder, args.tuple_folder,args.abuse_tuple_folder
    
    dns_record_folder_path = os.path.join(os.getcwd(), dns_record)
    cdn_dns_record_folder_path = os.path.join(os.getcwd(), cdn_dns_record)
    cdn_hosted_FQDN_folder_path = os.path.join(os.getcwd(), cdn_hosted_FQDN)
    target_domain_urls_folder_path = os.path.join(os.getcwd(), target_domain_urls_folder)
    tuple_folder_path =  os.path.join(os.getcwd(), tuple_folder)
    abuse_tuple_folder_path =  os.path.join(os.getcwd(), abuse_tuple_folder)
    print(f"cdn vendor:{cdn_vendor}")
    print(f"dns_record_folder_path:{dns_record_folder_path}")
    print(f"cdn_dns_record_folder_path:{cdn_dns_record_folder_path}")
    print(f"cdn_hosted_FQDN_folder_path:{cdn_hosted_FQDN_folder_path}")
    print(f"tuple_folder_path:{tuple_folder_path}")
    print(f"abuse_tuple_folder_path:{abuse_tuple_folder_path}")


    data_processor = DataProcessor(dns_record_folder_path, cdn_dns_record_folder_path,cdn_hosted_FQDN_folder_path)

    data_processor.process_folder_to_get_cdn_dns_record()

    data_processor.classify_domain_names_by_cdn_vendors()

    cral_domain_num = 15
    fronting_test_case_num = 10


    get_static_file_urls(cdn_vendor=cdn_vendor, cral_domain_num= cral_domain_num ,num_urls_to_crawl=10, target_domain_urls_folder_path=target_domain_urls_folder_path, CDN_Serverd_Domain_List_folder_path=cdn_hosted_FQDN_folder_path)


    tuples = generate_tuple(cdn_vendor=cdn_vendor, fronting_test_case_num=fronting_test_case_num,target_domain_urls_folder_path=target_domain_urls_folder_path)

    write_tuples_to_json(tuples=tuples,tuple_folder_path=tuple_folder_path, cdn_vendor=cdn_vendor)

    start_time = time.time()

    abuse_tuples = []
  

    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:

        results = pool.map(fronting_tester_wrapper, tuples)

        for abuse_tuple in results:
            if abuse_tuple != ():
                abuse_tuples.append(abuse_tuple)

    end_time = time.time()

    execution_time = end_time - start_time

    print(f"execution_time:{execution_time}s")
    write_abuse_tuples_to_json(cdn_vendor=cdn_vendor, tuples=abuse_tuples, abuse_folder_path=abuse_tuple_folder_path)

