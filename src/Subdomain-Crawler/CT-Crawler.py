## # LIBRARIES # ##
import re
import requests
import argparse
import os

# parse arguments
def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('-i', '--input_sld_file', type=str, required=True, help="Target sld file.")
	parser.add_argument('-o', '--output_floder', type=str, help="Output floder.")
	return parser.parse_args()

# format sld
def clear_url(target):
	# clear www and /path
	return re.sub('.*www\.','',target,1).split('/')[0].strip()


def save_a_sld(subdomains, output_folder, output_file_name):
    try:

        os.makedirs(output_folder, exist_ok=True)
        

        output_file_path = os.path.join(output_folder, output_file_name)
        

        with open(output_file_path, "a", encoding="utf-8") as f:
            f.write('\n'.join(subdomains) + '\n')
            
        print(f"[✓] Subdomains saved to {output_file_path}")
    except Exception as e:
        print(f"[X] An error occurred while writing to the file: {e}")
		
def process_a_sld(sld, output_folder):
    subdomains = []
    req = requests.get("https://crt.sh/?q=%.{d}&output=json".format(d=sld))
    if req.status_code != 200:
        print("[X] Information not available!") 
        exit(1)

    for (key, value) in enumerate(req.json()):
        subdomains.append(value['name_value'])

    print("\n[!] ---- TARGET: {d} ---- [!] \n".format(d=sld))

    subdomains = sorted(set(subdomains))
    output_file_name = f'{sld}.txt'
    save_a_sld(subdomains, output_folder=output_folder, output_file_name=output_file_name)

	# return subdomains
		
def main():
    args = parse_args()

    subdomains = []

    target_sld = args.input_sld_file
    output_folder = args.output_floder


    with open(target_sld, 'r', encoding='utf-8') as file:
        slds = [line.strip() for line in file.readlines()]


    for sld in slds:
        process_a_sld(sld, output_folder=output_folder)


main()