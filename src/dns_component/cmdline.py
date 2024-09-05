import argparse

def parse_args():
    parse = argparse.ArgumentParser(description='DNS Component') 
    parse.add_argument('-i', '--input_folder', default="data/test-subdomain", type=str, help='input folder')
    parse.add_argument('-o', '--output_folder', default="data/test-dns_record", type=str, help='output folder')
    parse.add_argument('-n', '--num_workers', default=4, type=int, help='Number of workers')
    parse.add_argument('-d', '--dns_servers', default=["8.8.8.8"], type=str, help='dns_servers')
    args = parse.parse_args()  
    return args