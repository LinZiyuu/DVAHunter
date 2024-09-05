import dns.resolver
import socket
import json
import os
import multiprocessing


class DNSQueryComponent:
    def __init__(self, dns_server=["8.8.8.8"],timeout=5):
        self.resolver = dns.resolver.Resolver()
        self.resolver.nameservers = dns_server
        self.resolver.timeout = timeout
    def get_all_cnames(self, domain):
        cnames = []
        current_domain = domain

        while True:
            try:
                answers = self.resolver.query(current_domain, 'CNAME')
                cname = answers[0].target.to_text()
                cnames.append(cname)
                current_domain = cname
            except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
                break

        return cnames
    def get_dns_records(self, domain):
        try:
            ns_records = [str(record) for record in self.resolver.query(domain, 'NS')]
            ns_err = ""
        except dns.exception.DNSException as e:
            ns_records = []
            if isinstance(e, dns.resolver.NXDOMAIN):
                ns_err = "NXDOMAIN"
            else:
                ns_err = str(e)

        try:
            cname_records = self.get_all_cnames(domain=domain)
            cname_err = ""
        except dns.exception.DNSException as e:
            cname_records = []
            if isinstance(e, dns.resolver.NXDOMAIN):
                cname_err = "NXDOMAIN"
            else:
                cname_err = str(e)

        try:
            a_records = [ip for ip in socket.gethostbyname_ex(domain)[2]]
        except socket.gaierror:
            a_records = []

        return ns_records, cname_records, a_records, ns_err, cname_err

    def save_dns_records_to_json(self, domain, output_file):
        ns_records, cname_records, a_records, cname_err, ns_err = self.get_dns_records(domain)
        result_dict = {
            domain: {
                "ns": ns_records,
                "cname": cname_records,
                "A": a_records,
                "cname_err": cname_err,
                "ns_err": ns_err

            }
        }

        with open(output_file, 'w') as json_file:
            json.dump(result_dict, json_file, indent=2)

    def process_txt_file_to_get_dns_record(self, args):
        file_path, output_folder_path = args
        if not os.path.exists(output_folder_path):
            os.makedirs(output_folder_path)

        result_dict = {}

        sld = os.path.splitext(os.path.basename(file_path))[0]
        print(sld)
        with open(file_path, 'r') as file:
            try:
                lines = file.readlines()
            except Exception as e:
                print(f"err: {file_path}")
            for line in lines:
                subdomain = line.strip('\n')
    
                ns_records, cname_records, a_records, cname_err, ns_err = self.get_dns_records(subdomain)

                result_dict[subdomain] = {
                    "ns": ns_records,
                    "cname": cname_records,
                    "A": a_records,
                    "cname_err": cname_err,
                    "ns_err": ns_err

                }


        json_file_path = os.path.join(output_folder_path, f"{sld}.json")

        with open(json_file_path, 'w') as json_file:
            json.dump(result_dict, json_file, indent=2)

    def process_folder_to_get_dns_record(self, input_folder_path, output_folder_path, n_process):     
        txt_files = [f for f in os.listdir(input_folder_path) if f.endswith('.txt')]
        pool = multiprocessing.Pool(processes=n_process)
        args_list = [(os.path.join(input_folder_path, txt_file), output_folder_path) for txt_file in txt_files]
        pool.map(self.process_txt_file_to_get_dns_record, args_list)
        pool.close()
        pool.join()

