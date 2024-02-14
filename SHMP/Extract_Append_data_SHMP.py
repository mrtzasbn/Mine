import re

def extract_and_return_data(file_path, start_pattern, end_pattern=None, output_prefix='output'):
    with open(file_path, 'r') as file:
        file_content = file.read()
    
    if end_pattern:
        data_blocks = re.findall(rf'{start_pattern}.*?{end_pattern}.*?(?={start_pattern}|$)', file_content, re.DOTALL)
    else:
        data_blocks = re.findall(rf'{start_pattern}.*?(?={start_pattern}|$)', file_content, re.DOTALL)
    
    for i, data in enumerate(data_blocks):
        with open(f'{output_prefix}_{i+1}.dat', 'w') as f:
            f.write(data.strip())
    return data_blocks

if __name__ == "__main__":
    filename = r'D:\yline01.dat'

    # Define your custom start and end patterns
    custom_start_pattern = '# Starttime'
    custom_end_pattern = '# Scan finished at'

    extracted_data = extract_and_return_data(filename, custom_start_pattern)

