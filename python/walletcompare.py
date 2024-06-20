"""
OVERVIEW // WALLET COMPARE
walletcompare.py processes two lists of wallet addresses from text files and outputs the unique wallets from each list.

REQUIREMENTS
This script does not require any external libraries. It uses the built-in `sys` module.

USAGE
python3 walletcompare.py <listofwallets1.txt> <listofwallets2.txt>

OUTPUT
The output will display the filenames and counts of unique wallets in each list, followed by the unique wallet addresses.
"""

import sys

def read_wallets(file_path):
    with open(file_path, 'r') as file:
        return set(file.read().splitlines())

def find_unique(wallets1, wallets2):
    unique_to_list1 = wallets1 - wallets2
    unique_to_list2 = wallets2 - wallets1
    return unique_to_list1, unique_to_list2

def main(file1, file2):
    wallets1 = read_wallets(file1)
    wallets2 = read_wallets(file2)

    unique_to_list1, unique_to_list2 = find_unique(wallets1, wallets2)

    print(f"{file1} ({len(unique_to_list1)} unique)")
    for wallet in unique_to_list1:
        print(wallet)
    
    print(f"\n{file2} ({len(unique_to_list2)} unique)")
    for wallet in unique_to_list2:
        print(wallet)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 walletcompare.py <listofwallets1.txt> <listofwallets2.txt>")
        sys.exit(1)

    file1 = sys.argv[1]
    file2 = sys.argv[2]
    main(file1, file2)
