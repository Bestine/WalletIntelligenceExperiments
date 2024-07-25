""""
This file will:
    - read a csv file containing wallet addresses
    - obtain 10 lists by randomly selecting 10 wallet addresses from the file.
    - the wallet address lists will be saved to txt files in test_#.txt convention
    - these lists will be run on https://thirdwavelabs-dev.fly.dev/ for analysis
"""

# Load the required library 
import pandas as pd 
import random 

# Load the required data set
df = pd.read_csv("analysis_tests/data/transaction_dataset.csv")

# Obtain lists of wallet addresses
wallet_address_list = df["Address"].to_list()

# shuffle the wallet addresses
random.shuffle(wallet_address_list)

# Create 10 lists each containing 10 unique wallet addresses
lists_of_wallets = [wallet_address_list[i*10:(i+1)*10] for i in range(10)]

# Save each list to a separate text file
for i, wallet_list in enumerate(lists_of_wallets):
    with open(f'analysis_tests/data/wallet_list_test_{i+1}.txt', 'w') as f:
        for address in wallet_list:
            f.write(f"{address}\n")

print("Wallet lists saved to text files successfully.")