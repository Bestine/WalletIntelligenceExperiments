""""
This file will:
    - read a csv file containing wallet addresses
    - obtain 10 lists by randomly selecting 10 wallet addresses from the file.
    - the wallet address lists will be saved to txt files in test_#.txt convention
    - these lists will be run on https://thirdwavelabs-dev.fly.dev/ for analysis
"""

# Load the required library 
import pandas as pd 

# Load the required data set
df = pd.read_csv("analysis_tests/data/transaction_dataset.csv")
print(df.head())