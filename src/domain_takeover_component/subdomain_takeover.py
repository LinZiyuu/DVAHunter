import requests
import dns.resolver
import sys,getopt,os,base64,json
import yaml
from termcolor import colored, cprint
import os
vulnerable_domains = []

HEADERS = {
    "Accept":"application/json, text/javascript, */*; q=0.01",
    "Accept-Language":"zh-CN,zh;q=0.9",
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36",
}


def url_get(url):
    try:
        r = requests.get(url=url,headers=HEADERS,timeout=5)
        status_code = r.status_code
        response_text = r.content.decode('utf-8')
        return status_code,response_text
    except:
        cprint('[*]Network connection timeout, please try again later.','yellow','on_red')



def providers_read():
    prividers_file_path = os.path.join(os.getcwd(), "src/domain_takeover_component/providers.json")
    try:
        with open(prividers_file_path,'r') as f:
            str_json = f.read()
            json_dicts = json.loads(str_json)
            return json_dicts
    except:
        cprint('[*]Failed to load fingerprint file, please check if you save providers.json file.','yellow','on_red')

def cname_get(url):

    try:
        cn = dns.resolver.query(url,'CNAME')
        for rrset in cn.response.answer:
            for cname in rrset.items:
                return (cname.to_text())
    except: 
        cprint('[*]' + url + 'CNAME record not found','yellow','on_red')


def process_json(json_file):
    try:
        json_dicts = providers_read()  
        for json_dict in json_dicts:
            fingerprint_lists = json_dict['response'] 
            fingercname_lists = json_dict['cname']  
        with open(json_file, 'r') as file:
            data = json.load(file)
            for domain, details in data.items():
                takeover_check(domain, details, json_dicts)
    except Exception as e:
        cprint(f'[!] Error while reading JSON file: {e}', 'red')


def output_to_json(vulnerable_domains, output_file):
    with open(output_file, 'w') as f:
        json.dump(vulnerable_domains, f, indent=4)


def takeover_check(domain,details,fingercname_lists):

    cname_record = details['cname'][0] if 'cname' in details and details['cname'] else None
    domain_cdn = details.get('cdn', 'Unknown CDN')
    cname_err = details.get('cname_err', '').lower()
    if cname_record:
        for fingerprint in fingercname_lists:
            if any(cname_suffix in cname_record for cname_suffix in fingerprint['cname']):
                if 'NXDOMAIN' in cname_err:
                    if any('NXDOMAIN' in response.lower() for response in fingerprint['response']):
                        cprint(f'[+] {domain} May have been taken over, CDN vendors:{domain_cdn}, CNAME:{cname_record}', 'green')
                        vulnerable_domains.append({
                            'domain': domain,
                            'cname': cname_record,
                            'cdn_provider': domain_cdn
                        })
                        return
                    else:
                        cprint(f'[*] {domain} CNAME is resolved to NXDOMAIN, but the fingerprints don t match, CDN vendor:{domain_cdn}', 'yellow')
                        return
                else:

                    cnameresponse_text = url_get('http://' + domain)[1]  
                    if any(response_phrase in cnameresponse_text for response_phrase in fingerprint['response']):
                        vulnerable_domains.append({
                            'domain': domain,
                            'cname': cname_record,
                            'cdn_provider': domain_cdn
                        })
                        cprint(f'[+] {domain} There is a risk of subdomain takeover, CDN vendors:{domain_cdn}, CNAME:{cname_record}', 'green')
                        return
                    else:
                        cprint(f'[*] {domain} No takeover risk found, CDN vendors:{domain_cdn}', 'yellow')
                        return
        cprint(f'[*] {domain} the CNAME is not in the known victim fingerprints, the CDN vendor:{domain_cdn}', 'yellow')
    else:
        cprint(f'[*] {domain} No CNAME records, CDN vendors:{domain_cdn}', 'yellow')

def main(argv):
    url_file = None
    json_file = None
    try:
        opts, args = getopt.getopt(argv, 'hu:f:c:o:')
    except getopt.GetoptError as e:
        cprint('[*] Usage: python subdomain_takeover.py -u <target>', 'red')
        cprint('[*] Usage: python subdomain_takeover.py -f <file>', 'red')
        cprint('[*] Usage: python subdomain_takeover.py -j <json_file>', 'red')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            cprint('[*] Usage: python subdomain_takeover.py -u <target>', 'red')
            cprint('[*] Usage: python subdomain_takeover.py -f <file>', 'red')
            cprint('[*] Usage: python subdomain_takeover.py -j <json_file>', 'red')
            sys.exit()
        elif opt == '-o':
            output_file = arg
        elif opt == '-u':
            url = arg
            cname = cname_get(url)
            process_domain(url, cname)
        elif opt == '-f':
            path = arg
            if os.path.isdir(path):
                for filename in os.listdir(path):
                    if filename.endswith('.json'):
                        json_file = os.path.join(path, filename)
                        print(f"Processing {json_file}")
                        process_json(json_file)

            elif os.path.isfile(path) and path.endswith('.json'):  
                process_json(path)
            else:
                cprint('[*] The path provided is not a JSON file or folder', 'red')

    output_to_json(vulnerable_domains, output_file)

def process_domain(url, cname):
    if cname is not None:
        print(cname)
        cprint('[*]CNAME was obtained successfully and is being verified to exist in the sensitive list....', 'green')
        json_dicts = providers_read()  
        for json_dict in json_dicts:
            fingerprint_lists = json_dict['response']  
            fingercname_lists = json_dict['cname']  
            for fingercname in fingercname_lists:
                if fingercname in cname:
                    cprint('[*]Present in fingerprint list, subdomain takeover risk being detected...', 'green')
                    takeover_check(url, cname, fingerprint_lists) 
    else:
        pass

if __name__ == "__main__":
    main(sys.argv[1:])



