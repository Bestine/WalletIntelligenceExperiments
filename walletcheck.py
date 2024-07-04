"""
OVERVIEW // WALLET CHECK
This script validates Ethereum wallet addresses from an input file. It extracts potential wallet addresses and checks for their validity, listing unique wallets and reporting invalid entries.

REQUIREMENTS
This script does not require any external libraries. It uses the built-in `sys` and `re` modules.

USAGE
python3 walletcheck.py <input_file>

EXAMPLE
python3 walletcheck.py wallets.txt

The output will display:
- Total number of rows processed.
- Count of unique wallet addresses.
- Count of duplicate wallet addresses.
- Count of invalid entries, along with a list of those invalid entries.
"""

real_wallet = "0xce8a4492bfa6f529041fc0c0a407f479de443aa507a3b870ee1d617c595505e4"

import sys
import re

def is_valid_wallet(address):
    return re.match(r"^0x[a-fA-F0-9]{40}$", address)

if len(sys.argv) < 2:
    print("Please provide an input file containing wallet addresses.")
    print("Usage: python3 walletcheck.py <input_file>")
    sys.exit(1)

input_file = sys.argv[1]

try:
    with open(input_file, "r") as file:
        content = file.read()
        extracted_addresses = re.findall(r"0x[a-fA-F0-9]{40}|\S+", content)
except FileNotFoundError:
    print(f"File not found: {input_file}")
    sys.exit(1)

valid_wallets = []
invalid_entries = []

for address in extracted_addresses:
    if is_valid_wallet(address):
        valid_wallets.append(address)
    else:
        invalid_entries.append(address)

unique_wallets = set(valid_wallets)
duplicate_wallets = len(valid_wallets) - len(unique_wallets)

print(f"\n       Total Rows: {len(extracted_addresses)}")
print(f"   Unique Wallets: {len(unique_wallets)}")
print(f"Duplicate Wallets: {duplicate_wallets}")
print(f"  Invalid Entries: {len(invalid_entries)}")

if len(invalid_entries) > 0:
    print("\nInvalid Entries:")
    for entry in invalid_entries:
        print(entry)
        
# Lets test the functions 
if __name__ == "__main__":
    # is_valid_wallet?
    # check if wallet is valid 
    is_valid_wallet("0x9BA9e1B15B8B88d2D184FC89bda4f31Fb1a12757")