import re

def extract_data_from_file(file_content):
    data_blocks = re.findall(r'# Starttime:.*?# Scan finished at.*?(?=# Starttime:|$)', file_content, re.DOTALL)
    return data_blocks

def write_data_to_files(data_list, prefix='output'):
    for i, data in enumerate(data_list):
        with open(f'{prefix}_{i+1}.dat', 'w') as f:
            f.write(data.strip())



if __name__ == "__main__":
    filename = r'D:\upper_edge_fine_5K_infield_ramp.dat'
    with open(filename, 'r') as file:
        file_content = file.read()

    extracted_data = extract_data_from_file(file_content)
    write_data_to_files(extracted_data)
