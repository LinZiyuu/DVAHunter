import os
import json

# 获取所有SLD的子域名的txt
def get_all_FQDN(input_folder, output_file):
    # 获取目录路径
    directory_path = os.path.dirname(output_file)

    # 检查目录是否存在，如果不存在则创建
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    # TODO 需要加一个文件夹判断
    with open(output_file, 'w') as output:
        for filename in os.listdir(input_folder):
            if filename.endswith(".txt"):
                file_path = os.path.join(input_folder, filename)
                with open(file_path, 'r') as input_file:
                    output.write(input_file.read())

# TODO 也需要修改
# def get_no_hosted_FQDN(cdn_vendor, all_FQDN_file):
#     # 读取所有的子域名
#     with open(all_FQDN_file, 'r') as f:
#         all_FQDN = list(map(lambda x: x.strip("\n"), f.readlines()))
#     # print(f"all_FQDN:{all_FQDN}")

#     # 读取某个CDN托管的域名
#     # cdn_vendor_file = f"data/cdn_hosted_FQDN/{cdn_vendor}.json"
#     cdn_vendor_file = f"data/test-cdn_hosted_FQDN/{cdn_vendor}.json"
#     with open(cdn_vendor_file, 'r') as f:
#         cdn_hosted_FQDN = json.load(f)
#     print(f"cdn_hosted_FQDN:{cdn_hosted_FQDN}")

#     no_hosted_FQDN = (set(all_FQDN) - set(cdn_hosted_FQDN[cdn_vendor]))
#     # no_hosted_FQDN_json_file_path = os.path.join("data/all_FQDN", f"{cdn_vendor}.json")
#     no_hosted_FQDN_json_file_path = os.path.join("data/test-all_FQDN", f"{cdn_vendor}.json")
#     no_hosted_FQDN_dict = {
#         cdn_vendor: list(no_hosted_FQDN)
#     }
#     if no_hosted_FQDN:
#         with open(no_hosted_FQDN_json_file_path, 'w') as json_file:
#             json.dump(no_hosted_FQDN_dict, json_file, indent=2)
#     # return no_hosted_FQDN

def get_no_hosted_FQDN(cdn_vendor, all_FQDN_file,cdn_hosted_FQDN_folder_path,all_host_folaer_path):
    # 读取所有的子域名
    with open(all_FQDN_file, 'r') as f:
        all_FQDN = list(map(lambda x: x.strip("\n"), f.readlines()))
    # print(f"all_FQDN:{all_FQDN}")

    # 读取某个CDN托管的域名
    # cdn_vendor_file = f"data/cdn_hosted_FQDN/{cdn_vendor}.json"
    # cdn_vendor_file = f"data/test-cdn_hosted_FQDN/{cdn_vendor}.json"
    cdn_vendor_file = os.path.join(cdn_hosted_FQDN_folder_path,f"{cdn_vendor}.json")
    with open(cdn_vendor_file, 'r') as f:
        cdn_hosted_FQDN = json.load(f)
    print(f"cdn_hosted_FQDN:{cdn_hosted_FQDN}")

    no_hosted_FQDN = (set(all_FQDN) - set(cdn_hosted_FQDN[cdn_vendor]))
    # no_hosted_FQDN_json_file_path = os.path.join("data/all_FQDN", f"{cdn_vendor}.json")
    # no_hosted_FQDN_json_file_path = os.path.join("data/test-all_FQDN", f"{cdn_vendor}.json")
    no_hosted_FQDN_json_file_path = os.path.join(all_host_folaer_path, f"{cdn_vendor}.json")
    no_hosted_FQDN_dict = {
        cdn_vendor: list(no_hosted_FQDN)
    }
    if no_hosted_FQDN:
        with open(no_hosted_FQDN_json_file_path, 'w') as json_file:
            json.dump(no_hosted_FQDN_dict, json_file, indent=2)
    # return no_hosted_FQDN

if __name__ == "__main__":
    
    # subdomain_folder_path = os.path.join(os.getcwd(), "data/subdomain")
    # all_host_path = os.path.join(os.getcwd(), "data/all_FQDN/subdomain.txt")

    subdomain_folder_path = os.path.join(os.getcwd(), "data/tranco-top-1k-subdomain")
    all_host_path = os.path.join(os.getcwd(), "data/all_FQDN/tranco-top-1k-subdomain.txt")
    # input_folder_path = "top-10k-subdomain"  # 请替换为你的输入文件夹路径
    # output_file_path = "top-10k-subdomain.txt"  # 请替换为你的输出文件路径

    get_all_FQDN(input_folder=subdomain_folder_path, output_file=all_host_path)
    get_no_hosted_FQDN(cdn_vendor="Fastly",all_FQDN_file=all_host_path)
