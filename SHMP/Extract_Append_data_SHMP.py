import re

def extract_data_from_file(file_content, start_pattern, end_pattern=None):
    if end_pattern:
        data_blocks = re.findall(rf'{start_pattern}.*?{end_pattern}.*?(?={start_pattern}|$)', file_content, re.DOTALL)
    else:
        data_blocks = re.findall(rf'{start_pattern}.*?(?={start_pattern}|$)', file_content, re.DOTALL)
    return data_blocks

def write_data_to_files(data_list, prefix='output'):
    for i, data in enumerate(data_list):
        with open(f'{prefix}_{i+1}.dat', 'w') as f:
            f.write(data.strip())

if __name__ == "__main__":
    filename = r'D:\upper_edge_fine_5K_infield_ramp.dat'
    with open(filename, 'r') as file:
        file_content = file.read()

    # Define your custom start and end patterns
    custom_start_pattern = '# Starttime'
    custom_end_pattern = '# Scan finished at'

    extracted_data = extract_data_from_file(file_content, custom_start_pattern)
    write_data_to_files(extracted_data)
