from cmdline import parse_args
from DnsQueryComponent import DNSQueryComponent
import os


if __name__ == "__main__":
    args = parse_args()
    input_folder, output_folder,workers, dns_servers = args.input_folder, args.output_folder,args.num_workers, args.dns_servers.split(',')

    subdomain_folder_path = os.path.join(os.getcwd(), input_folder)
    dns_record_folder_path = os.path.join(os.getcwd(), output_folder)
    dns_query_component = DNSQueryComponent(dns_server=dns_servers)
    dns_query_component.process_folder_to_get_dns_record(subdomain_folder_path, dns_record_folder_path, n_process=workers)