import os
import argparse

# parse arguments
def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('-sld1', '--sld1_floder', type=str, required=True, help="sld1 floder.")
	parser.add_argument('-sld2', '--sld2_floder', type=str,required=True, help="sld2 floder.")
	parser.add_argument('-sld', '--sld_floder', type=str,required=True, help="sld floder.") 
	return parser.parse_args()

def get_txt_files(folder):

    return {file for file in os.listdir(folder) if file.endswith('.txt')}

def read_file(file_path):

    with open(file_path, 'r', encoding='utf-8') as f:
        return set(line.strip() for line in f)

def write_to_file(file_path, data):

    with open(file_path, 'w', encoding='utf-8') as f:
        for item in sorted(data):
            f.write(f"{item}\n")

def filter_domains(domains):

    return {domain for domain in domains if not domain.startswith('*.')}

def main():

    args = parse_args()

    folder1 = args.sld1_floder
    folder2 = args.sld2_floder
    output_folder = args.sld_floder


    os.makedirs(output_folder, exist_ok=True)


    txt_files1 = get_txt_files(folder1)
    txt_files2 = get_txt_files(folder2)


    common_files = txt_files1.intersection(txt_files2)

    for file_name in common_files:
        file_path1 = os.path.join(folder1, file_name)
        file_path2 = os.path.join(folder2, file_name)


        content1 = read_file(file_path1)
        content2 = read_file(file_path2)
        combined_content = content1.union(content2)


        filtered_content = filter_domains(combined_content)


        output_path = os.path.join(output_folder, file_name)
        write_to_file(output_path, filtered_content)

if __name__ == '__main__':
    main()
