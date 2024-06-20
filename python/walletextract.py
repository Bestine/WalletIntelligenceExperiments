"""
OVERVIEW // WALLET EXTRACT
This script extracts wallet addresses from a txt, CSV, or JSON file and writes them to a text file for further processing. 

USAGE
python3 walletextract.py <input_file>

OUTPUT
The output will be a text file named <input_file>_clean.txt containing the unique wallet addresses extracted from the input file.
"""

import sys
import re
import json
import csv

def is_valid_wallet(address):
    return re.match(r"^0x[a-fA-F0-9]{40}$", address)

def extract_addresses(file_path):
    if file_path.endswith(".txt"):
        with open(file_path, "r") as file:
            content = file.read()
            return re.findall(r"0x[a-fA-F0-9]{40}|\S+", content)
    elif file_path.endswith(".json"):
        with open(file_path, "r") as file:
            data = json.load(file)
            if isinstance(data, list):
                return [item for item in data if is_valid_wallet(item)]
            else:
                print("Invalid JSON format. Expected a list of wallet addresses.")
                sys.exit(1)
    elif file_path.endswith(".csv"):
        with open(file_path, "r") as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip header row
            return [row[0] for row in csv_reader if len(row) > 0 and is_valid_wallet(row[0])]
    else:
        print("Unsupported file format. Please provide a .txt, .json, or .csv file.")
        sys.exit(1)

if len(sys.argv) < 2:
    print("Please provide an input file containing wallet addresses.")
    print("Usage: python3 walletextract.py <input_file>")
    sys.exit(1)

input_file = sys.argv[1]
extracted_addresses = extract_addresses(input_file)

valid_wallets = []
invalid_entries = []

for address in extracted_addresses:
    if is_valid_wallet(address):
        valid_wallets.append(address)
    else:
        invalid_entries.append(address)

unique_wallets = set(valid_wallets)
duplicate_wallets = len(valid_wallets) - len(unique_wallets)

print(f"Total Rows: {len(extracted_addresses)}")
print(f"Unique Wallets: {len(unique_wallets)}")
print(f"Duplicate Wallets: {duplicate_wallets}")
print(f"Invalid Entries: {len(invalid_entries)}")

if len(invalid_entries) > 0:
    print("\nInvalid Entries:")
    for entry in invalid_entries:
        print(entry)

# Write unique wallets to a text file with the same name as the input file
output_file = input_file.rsplit(".", 1)[0] + "_clean.txt"
with open(output_file, "w") as file:
    file.write("\n".join(unique_wallets))

print(f"\nUnique wallets extracted and saved to: {output_file}")