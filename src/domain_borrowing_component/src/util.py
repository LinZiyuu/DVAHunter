import json
import socket
# from test_body import check_error
# from test_cname import get_cname_records
from cdn_map import cname_mapping,  check_CNAME
import uuid
import re
import os
import dns.resolver
import random

# *生成HTTP请求
def generate_http_request_header_00(host):
    bypass_cache = uuid.uuid4()
    uri = f"/?{bypass_cache}"
    parts = [
        f"GET {uri} HTTP/1.1\r\n",
        f"Host: {host}\r\n",
        f"User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36\r\n",
        f"Connection: close\r\n",
        "\r\n",
    ]
    return "".join(parts)

# def send_http_request(ip, port, request):
#     try:
#         # 创建一个TCP连接
#         with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#             # 连接到指定的IP和端口
#             s.connect((ip, port))

#             # 发送HTTP请求
#             s.sendall(request.encode())

#             # 接收响应数据
#             response = b''
#             while True:
#                 data = s.recv(1024)
#                 if not data:
#                     break
#                 response += data

#         # 将响应数据按照CRLF分割成响应头和响应体
#         header, body = response.split(b'\r\n\r\n', 1)

#         # 解析响应头
#         header_lines = header.decode().split('\r\n')
#         status_line = header_lines[0]
#         status_code = int(status_line.split(' ')[1])

#         # 获取响应头部
#         headers = {}
#         for line in header_lines[1:]:
#             key, value = line.split(': ', 1)
#             headers[key] = value

#         return status_code, headers, body.decode()
#     except Exception as e:
#         print(e)

def send_http_request(ip, port, request):
    try:
        # 创建一个TCP连接
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            
            # 设置超时时间为5秒
            s.settimeout(5)
            # 连接到指定的IP和端口

            s.connect((ip, port))

            # 发送HTTP请求
            s.sendall(request.encode())

            # 接收响应数据
            response = b''
            while True:
                data = s.recv(1024)
                if not data:
                    break
                response += data
        if response != b'':
        # 将响应数据按照CRLF分割成响应头和响应体
            header, body = response.split(b'\r\n\r\n', 1)

            # 解析响应头
            header_lines = header.decode().split('\r\n')
            status_line = header_lines[0]
            status_code = int(status_line.split(' ')[1])

            # 获取响应头部
            headers = {}
            for line in header_lines[1:]:
                key, value = line.split(': ', 1)
                headers[key] = value
            # print(type(status_code))
            # print(type(headers))
            # print(type(body))
        # <class 'int'>
        # <class 'dict'>
        # <class 'str'>
        else:
            status_code = 0 
            headers = {}
            body = b''

        return status_code, headers, body.decode()
    except Exception as e:
        print(e)
        return 0, {}, b''

# * 检测body中是否存在未部署的特征
def check_error(response_body):
    # 定义要检查的错误字符串
    error_string = "Fastly error: unknown domain"

    # 使用正则表达式搜索错误字符串
    match = re.search(re.escape(error_string), response_body)

    # 如果匹配到错误字符串，则返回 False
    return match is None


# * 获取dns记录 
# ! 是否能用本地已经有的CNAME进行匹配省去查询
def get_cname_records(domain):
    # 获取NS、CNAME和A记录列表
    resolver = dns.resolver.Resolver()

    try:
        # 获取域名的 CNAME 记录
        cname_records = [str(record) for record in resolver.query(domain, 'CNAME')]

    except dns.exception.DNSException:
        cname_records = []

    return cname_records


def read_json_file(input_folder_path, file_name):
    file_path = os.path.join(input_folder_path, file_name)
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def read_txt_file(input_folder_path, file_name):
    file_path = os.path.join(input_folder_path, file_name)
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file.readlines()]
        return lines 

# fastly
def check_borrowed(host, status_code, headers, body):
    # 检测body中是否有未部署的特征
    body_err = check_error(body)
    # print(body_err)
    # 检测响应码和body特征是否符合未部署
    # 如果部署则检测cname
    if status_code != 500 and body_err == True:
        cname_records = get_cname_records(host)
        # print(cname_records)
        cdn_provider_cname = check_CNAME(cname_records)
        if cdn_provider_cname != "Fastly":
            print(f"domain: {host} borrowed in Fastly")
            return True
        else: 
            return False

# Fastly
def check_borrowed_fastly(host, status_code, headers, body):
    # 检测body中是否有未部署的特征
    body_err = check_error(body)
    # print(body_err)
    # 检测响应码和body特征是否符合未部署
    # 如果部署则检测cname
    if status_code != 500 and body_err == True:
        cname_records = get_cname_records(host)
        # print(cname_records)
        cdn_provider_cname = check_CNAME(cname_records)
        if cdn_provider_cname != "Fastly":
            print(f"domain: {host} borrowed in Fastly")
            return True
        else: 
            return False
       
# Bunny 
def check_borrowed_bunny(host, status_code, headers, body):
    # 检测body中是否有未部署的特征
    body_err = check_error(body)
    # print(body_err)
    # 检测响应码和body特征是否符合未部署
    # 如果部署则检测cname
    if status_code != 500 and body_err == True:
        cname_records = get_cname_records(host)
        # print(cname_records)
        cdn_provider_cname = check_CNAME(cname_records)
        if cdn_provider_cname != "Fastly":
            print(f"domain: {host} borrowed in Fastly")
            return True
        else: 
            return False


def write_result(output_folder_path = "Domain_Borrowed",cdn_vendor= "Fastly"):
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    for key, value in result_dict.items():
        json_file_path = os.path.join(output_folder_path, f"{cdn_vendor}.json")
        with open(json_file_path, 'w') as json_file:
            json.dump({key: value}, json_file, indent=2)

def get_random_country_ip_dict(file_name='Fastly_sort_by_country.json',num_selected_nodes=1,cdn_vendor="Fastly"):
    input_folder_path="ingress_ip"
    file_path = os.path.join(input_folder_path, file_name)
    with open(file_path, 'r') as file:
        data = json.load(file)
    # 获取 Fastly 厂商的国家节点信息
    fastly_nodes = data.get(cdn_vendor, {})

    random_country_ip_dict = {}
    # 选择的节点个数
    num_selected_nodes = 1  # 你可以根据需要修改这个数字

    # 遍历每个国家的节点信息
    for country, nodes in fastly_nodes.items():
        # 随机选取一个节点
        selected_nodes = random.sample(nodes, num_selected_nodes) if nodes else []

        random_country_ip_dict[country] = selected_nodes

        # 打印国家和对应的节点
        # print(f"Country: {country}, Selected Node: {selected_nodes}")
    return random_country_ip_dict