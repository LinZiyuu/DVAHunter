import re
from util import get_cname_records, check_CNAME

def check_error_fastly(response_body):
    try:
        error_string = "Fastly error: unknown domain"
        match = re.search(re.escape(error_string), response_body)


        return match is None
    except TypeError as e:
        print(f'An error occurred in check_error_fastly: {e}')
        return True

def check_error_keycdn(response_body):

    error_string = "The access to the resource has been denied."

    match = re.search(re.escape(error_string), response_body)

    return match is None


def check_error_bunny(response_body):
    error_string = "Domain suspended or not configured"

    match = re.search(re.escape(error_string), response_body)

    return match is None

def check_error_cachefly(response_body):

    error_string = "Hostname not configured"


    match = re.search(re.escape(error_string), response_body)


    return match is None
    
def check_headers_huawei(headers):
    if 'X-CCDN-FORBID-CODE' not in headers.keys():
        return True
    elif headers['X-CCDN-FORBID-CODE'] == '040001':
        return False


# TODO Yundun 
def check_borrowed_all(host, status_code, headers, body,cdn_vendor):
    # TODO Kuocai Medianova Netlify UCloud Yundun goooood lightCDN
    if cdn_vendor == 'Fastly':
        borrowed_flag = check_borrowed_fastly(host, status_code, headers, body)
    elif cdn_vendor == 'BunnyCDN':
        borrowed_flag = check_borrowed_bunny(host, status_code, headers, body)
    elif cdn_vendor == 'KeyCDN':
        borrowed_flag = check_borrowed_keycdn(host, status_code, headers, body)
    elif cdn_vendor == 'Cachefly':
        borrowed_flag = check_borrowed_cachefly(host, status_code, headers, body)
    elif cdn_vendor == 'CDN77':
        borrowed_flag = check_borrowed_cdn77(host, status_code, headers, body)
    elif cdn_vendor == 'StackPath':
        borrowed_flag = check_borrowed_stackpath(host, status_code, headers, body)
    elif cdn_vendor == 'HuaweiCloud':
        borrowed_flag = check_borrowed_huawei(host, status_code, headers, body)
    elif cdn_vendor == 'CDNetworks':
        borrowed_flag = check_borrowed_cdnetworks(host, status_code, headers, body)
    elif cdn_vendor == 'ChinaNetCenter':
        borrowed_flag = check_borrowed_chinanetcenter(host, status_code, headers, body)
    elif cdn_vendor == 'EdgeNext':
        borrowed_flag = check_borrowed_edgenext(host, status_code, headers, body)
    elif cdn_vendor == 'Edgio':
        borrowed_flag = check_borrowed_edgio(host, status_code, headers, body)
    elif cdn_vendor == 'Kuocai':
        borrowed_flag = check_borrowed_kuocai(host, status_code, headers, body)
    elif cdn_vendor == 'Medianova':
        borrowed_flag = check_borrowed_medianova(host, status_code, headers, body)
    elif cdn_vendor == 'Netlify':
        borrowed_flag = check_borrowed_netlify(host, status_code, headers, body)
    elif cdn_vendor == 'UCloud':
        borrowed_flag = check_borrowed_ucloud(host, status_code, headers, body)
    elif cdn_vendor == 'Goooood':
        borrowed_flag = check_borrowed_goooood(host, status_code, headers, body)
    elif cdn_vendor == 'lightCDN':
        borrowed_flag = check_borrowed_lightcdn(host, status_code, headers, body)
    return borrowed_flag

def check_borrowed_fastly(host, status_code, headers, body):

    body_err = check_error_fastly(body)
    if status_code != 500 and body_err == True:
        cname_records = get_cname_records(host)
        cdn_provider_cname = check_CNAME(cname_records)
        if cdn_provider_cname != "Fastly":
            print(f"domain: {host} borrowed in Fastly")
            return True
        else: 
            return False
        

def check_borrowed_cdnetworks(host, status_code, headers, body):
    if status_code != 0:
        cname_records = get_cname_records(host)

        cdn_provider_cname = check_CNAME(cname_records)
        if cdn_provider_cname != "CDNetworks":
            print(f"domain: {host} borrowed in CDNetworks")
            return True
        else: 
            return False
        
def check_borrowed_chinanetcenter(host, status_code, headers, body):


    if status_code != 0:
        cname_records = get_cname_records(host)

        cdn_provider_cname = check_CNAME(cname_records)
        if cdn_provider_cname != "ChinaNetCenter":
            print(f"domain: {host} borrowed in ChinaNetCenter")
            return True
        else: 
            return False



def check_borrowed_bunny(host, status_code, headers, body):
    body_err = check_error_bunny(body)
    if status_code != 403 and body_err == True:
        cname_records = get_cname_records(host)
        cdn_provider_cname = check_CNAME(cname_records)
        if cdn_provider_cname != "BunnyCDN":
            print(f"domain: {host} borrowed in BunnyCDN")
            return True
        else: 
            return False

def check_borrowed_keycdn(host, status_code, headers, body):
    body_err = check_error_keycdn(body)
    if status_code != 403 and body_err == True:
        cname_records = get_cname_records(host)
        cdn_provider_cname = check_CNAME(cname_records)
        if cdn_provider_cname != "KeyCDN":
            print(f"domain: {host} borrowed in KeyCDN")
            return True
        else: 
            return False

def check_borrowed_cachefly(host, status_code, headers, body):
    body_err = check_error_cachefly(body)
    if status_code != 404 and body_err == True:
        cname_records = get_cname_records(host)
        cdn_provider_cname = check_CNAME(cname_records)
        if cdn_provider_cname != "Cachefly":
            print(f"domain: {host} borrowed in Cachefly")
            return True
        else: 
            return False

def check_borrowed_cdn77(host, status_code, headers, body):
    if status_code != 0:
        cname_records = get_cname_records(host)
        cdn_provider_cname = check_CNAME(cname_records)
        if cdn_provider_cname != "CDN77":
            print(f"domain: {host} borrowed in CDN77")
            return True
        else: 
            return False

def check_borrowed_stackpath(host, status_code, headers, body):

    if headers["Cache-Control"] != 'max-age=0' and headers['Content-Length'] != '0' and status_code != 404 :
        cname_records = get_cname_records(host)
        cdn_provider_cname = check_CNAME(cname_records)
        if cdn_provider_cname != "StackPath":
            print(f"domain: {host} borrowed in StackPath")
            return True
        else: 
            return False

def check_borrowed_huawei(host, status_code, headers, body):
    code_bool = check_headers_huawei(headers)
    if status_code != 403 and code_bool:
        cname_records = get_cname_records(host)
        cdn_provider_cname = check_CNAME(cname_records)
        if cdn_provider_cname != "HuaweiCloud":
            print(f"domain: {host} borrowed in HuaweiCloud")
            return True
        else: 
            return False

def check_borrowed_edgenext(host, status_code, headers, body):
    body_err = check_error_edgenext(body)
    if status_code != 403 and body_err == True:
        cname_records = get_cname_records(host)
        cdn_provider_cname = check_CNAME(cname_records)
        if cdn_provider_cname != "EdgeNext":
            print(f"domain: {host} borrowed in EdgeNext")
            return True
        else: 
            return False
        
def check_error_edgenext(response_body):
    error_string = "ERROR: ACCESS DENIED"

    match = re.search(re.escape(error_string), response_body)

    return match is None


def check_borrowed_edgio(host, status_code, headers, body):
    body_err = check_error_edgio(body)

    if status_code != 404 and body_err == True:
        cname_records = get_cname_records(host)
        cdn_provider_cname = check_CNAME(cname_records)
        if cdn_provider_cname != "Edgio":
            print(f"domain: {host} borrowed in Edgio")
            return True
        else: 
            return False


def check_error_edgio(response_body):
    error_string = "404 - Not Found"

    match = re.search(re.escape(error_string), response_body)

    return match is None

def check_borrowed_kuocai(host, status_code, headers, body):
    body_err = check_error_kuocai(host, body)
    if status_code != 403 and body_err == True:
        cname_records = get_cname_records(host)
        cdn_provider_cname = check_CNAME(cname_records)
        if cdn_provider_cname != "Kuocai":
            print(f"domain: {host} borrowed in Kuocai")
            return True
        else: 
            return False
        
def check_error_kuocai(host, response_body):
    error_string = f"{host} conf not found"

    match = re.search(re.escape(error_string), response_body)

    return match is None


def check_borrowed_medianova (host, status_code, headers, body):
    if status_code != 0:
        cname_records = get_cname_records(host)
        cdn_provider_cname = check_CNAME(cname_records)
        if cdn_provider_cname != "Medianova":
            print(f"domain: {host} borrowed in Medianova")
            return True
        else: 
            return False
        
def check_borrowed_netlify(host, status_code, headers, body):
    body_err = check_error_netlify(body)
    if status_code != 404 and body_err == True:
        cname_records = get_cname_records(host)
        cdn_provider_cname = check_CNAME(cname_records)
        if cdn_provider_cname != "Netlify":
            print(f"domain: {host} borrowed in Netlify")
            return True
        else: 
            return False


def check_error_netlify(response_body):
    error_string = "Not Found - Request ID:"

    match = re.search(re.escape(error_string), response_body)

    return match is None

def check_borrowed_ucloud(host, status_code, headers, body):
    body_err = check_error_ucloud(body)
    if status_code != 403 and body_err == True:
        cname_records = get_cname_records(host)
        cdn_provider_cname = check_CNAME(cname_records)
        if cdn_provider_cname != "UCloud":
            print(f"domain: {host} borrowed in UCloud")
            return True
        else: 
            return False
        

def check_error_ucloud(response_body):
    error_string = f"Please report this message and include the following information to us"

    match = re.search(re.escape(error_string), response_body)

    return match is None

def check_borrowed_lightcdn(host, status_code, headers, body):
    body_err = check_error_lightcdn(body)
    if status_code != 400 and body_err == True:
        cname_records = get_cname_records(host)
        cdn_provider_cname = check_CNAME(cname_records)
        if cdn_provider_cname != "LightCDN":
            print(f"domain: {host} borrowed in LightCDN")
            return True
        else: 
            return False
        

def check_error_lightcdn(response_body):
    error_string = f"400 Bad Request"

    match = re.search(re.escape(error_string), response_body)

    return match is None


def check_borrowed_goooood(host, status_code, headers, body):
    body_err = check_error_goooood(body)

    if status_code != 400 and body_err == True:
        cname_records = get_cname_records(host)
        cdn_provider_cname = check_CNAME(cname_records)
        if cdn_provider_cname != "Goooood":
            print(f"domain: {host} borrowed in Goooood")
            return True
        else: 
            return False
        
def check_error_goooood(response_body):
    error_string = f"/unkonwdomain404/notfound"

    match = re.search(re.escape(error_string), response_body)

    return match is None

