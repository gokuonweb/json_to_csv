'''
This script is used for converting JSON data to CSV format.
Input accepted:
    .TXT or .JSON files
    
Output:
    .CSV file
'''

import json
import csv
import os
import time

# checking for JSON data
def check_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        if isinstance(data, list) and isinstance(data[0], dict):
            print("[+] The file contains valid JSON.")
            return data
        else:
            print("[-] The JSON is valid but does not contain a top-level dictionary.")
            return 0

    except json.JSONDecodeError as e:
        print(f"[-] Invalid JSON: {e}")
        return 0
    except Exception as e:
        print(f"[-] An error occurred: {e}")
        return 0

# converting JSON to CSV
def convert_json_to_csv(output_file, json_data):
    count_entries = 0
    count_write = 0
    skipped_lines = 0
    headers = []
    try:
        for entry in json_data:
            count_entries += 1
            for key in entry.keys():
                if key not in headers:
                    headers.append(key)
        print("[+] Headers of CSV file:\n\t{0}".format('\n\t'.join(headers)))

        with open(output_file, 'w', newline='') as file:
            csv_writer = csv.DictWriter(file, fieldnames=headers)
            csv_writer.writeheader()
            for row in json_data:
                try:
                    count_write += 1
                    csv_writer.writerow({header: row.get(header, 'N/A') for header in headers})
                except (UnicodeEncodeError, ValueError, TypeError) as e:
                    print('-'*100)
                    print(f"[-] Skipping line {count_write} due to unsupported character or error: {e}\n\nData: {row}")
                    skipped_lines += 1
                    print('-' * 100)
                    continue
        if skipped_lines !=0:
            print(f"[+] Conversion completed: {count_write - skipped_lines} lines written, {skipped_lines} lines skipped.")
        else:
            print(f"[+] Conversion completed: {count_write} lines written.")

        return 1

    except Exception as e:
        if count_write != 0:
            print(f'[-] Error occurred while processing entry: {count_write}\n\nPlease check data: {row}.\n\nError description: {str(e)}')
        else:
            print(f'[-] Error occurred. Details: {str(e)}')
        return 0


if __name__ == "__main__":
    # main file
    try: # accepting input
        file_path = input("\n[<] Enter the JSON file path: ")
        file_path = file_path.replace('"', '').replace("'", "")
        if not (os.path.exists(file_path)):
            print('[-] Path does not exists. Exiting!')
            time.sleep(10)
            raise SystemExit()
        else:
            file_path_lower = file_path.lower()
            if file_path_lower.endswith('.json') or file_path_lower.endswith('.txt'):
                random_suffix = int(time.time()%100000) # generating random number for file name suffix
                output_file = f'{os.path.splitext(os.path.basename(file_path))[0]}_{random_suffix}.csv'
                output_path = os.path.join(os.path.split(file_path)[0],output_file) # output file path

                json_data = check_json_file(file_path) # checking whether it is a valid JSON format or not

                if json_data and isinstance(json_data, list):
                    end_result = convert_json_to_csv(output_path, json_data)
                    if end_result:
                        print(f"[+] CSV file saved at: {output_path}.")
                        time.sleep(10)
                    else:
                        print(f"[-] Unable to convert JSON to CSV.")
                        time.sleep(10)
                        raise SystemExit()
                else:
                    print('[-] Please check the JSON data and error description.')
                    print('[!] Sample JSON data format:\n')
                    print('''   [
        {"name": "ABC", "age": 30, "city": "Bangalore", "country": "India"},
        {"name": "DEF", "age": 25, "country": "USA"},
        {"name": "XYZ", "city": "London", "country": "UK", "profession": "Engineer"}
    ]
''')
                    time.sleep(10)
                    raise SystemExit()
            else:
                print('[-] Please check the file extension. Only .txt or .json files accepted as input files!')
                time.sleep(10)
                raise SystemExit()

    except Exception as e:
        print(f'\n[-] Error occurred. Details: {str(e)}')
        time.sleep(10)
        raise SystemExit()
    
    except KeyboardInterrupt:
        print('\n[!] Keyboard interrupt detected. Exiting!')
        time.sleep(10)
        raise SystemExit()