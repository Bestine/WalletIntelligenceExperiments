import sys
import csv
from datetime import datetime
from collections import defaultdict

# Define initial variables
total_results = 0
error_results = 0
total_spend = 0.0
total_transaction_count = 0
is_bot_true = 0
is_bot_false = 0
total_balance = 0.0
spend_by_bot_status = defaultdict(float)
transaction_count_by_bot_status = defaultdict(int)
dates = []

# Read CSV data from stdin
csv_reader = csv.DictReader(sys.stdin)

for row in csv_reader:
    total_results += 1

    # Check for error in the RESPONSE field
    if row['Response'].startswith('Error'):
        error_results += 1
        continue

    # Spend and transaction count
    try:
        spend = float(row['Spend'])
        transaction_count = int(row['Transaction Count'])
        total_spend += spend
        total_transaction_count += transaction_count
    except ValueError:
        continue  # Skip rows with invalid numeric data

    # Bot status counts
    is_bot = row['Is Bot'].strip().lower()
    if is_bot == 'true':
        is_bot_true += 1
        spend_by_bot_status['true'] += spend
        transaction_count_by_bot_status['true'] += transaction_count
    elif is_bot == 'false':
        is_bot_false += 1
        spend_by_bot_status['false'] += spend
        transaction_count_by_bot_status['false'] += transaction_count

    # Total balance
    try:
        balance = float(row['Total Balance'])
        total_balance += balance
    except ValueError:
        pass  # If balance is not a number, ignore it

    # Collecting dates for lifespan calculation
    try:
        date = datetime.fromisoformat(row['Created At'][:-1])  # Remove the trailing 'Z'
        dates.append(date)
    except ValueError:
        pass  # If date is invalid, ignore it

# Calculations
valid_wallets = total_results - error_results
avg_spend_per_wallet = total_spend / valid_wallets if valid_wallets else 0
avg_transaction_count_per_wallet = total_transaction_count / valid_wallets if valid_wallets else 0
avg_transaction_value = total_spend / total_transaction_count if total_transaction_count else 0
avg_balance_per_wallet = total_balance / valid_wallets if valid_wallets else 0
avg_spend_bot_true = spend_by_bot_status['true'] / is_bot_true if is_bot_true else 0
avg_spend_bot_false = spend_by_bot_status['false'] / is_bot_false if is_bot_false else 0
avg_transaction_count_bot_true = transaction_count_by_bot_status['true'] / is_bot_true if is_bot_true else 0
avg_transaction_count_bot_false = transaction_count_by_bot_status['false'] / is_bot_false if is_bot_false else 0
error_rate = (error_results / total_results) * 100 if total_results else 0

# Wallet lifespan calculation
if dates:
    min_date = min(dates)
    max_date = max(dates)
    lifespan_days = (max_date - min_date).days
    avg_lifespan = lifespan_days / len(dates)
else:
    avg_lifespan = 0

# Presenting the data
print(f"SUMMARY OF ANALYSIS\n{'-'*40}")
print(f"Total Wallets Analyzed: {total_results}")
print(f"Null Results: {error_results} ({error_rate:.2f}% error rate)\n")
print(f"AVERAGE TRANSACTION METRICS\n{'-'*40}")
print(f"- Average Spend per Wallet: ${avg_spend_per_wallet:.2f} (Count: {valid_wallets})")
print(f"- Average Transaction Count per Wallet: {avg_transaction_count_per_wallet:.2f} (Count: {valid_wallets})")
print(f"- Average Transaction Value: ${avg_transaction_value:.2f} (Count: {total_transaction_count})\n")
print(f"AVERAGE BALANCE METRICS\n{'-'*40}")
print(f"- Average Balance per Wallet: ${avg_balance_per_wallet:.2f} (Count: {valid_wallets})\n")
print(f"AVERAGE SPEND BY BOT STATUS\n{'-'*40}")
print(f"Bot: true  | Average Spend: ${avg_spend_bot_true:.2f} (Count: {is_bot_true})")
print(f"Bot: false | Average Spend: ${avg_spend_bot_false:.2f} (Count: {is_bot_false})\n")
print(f"AVERAGE TRANSACTION COUNT BY BOT STATUS\n{'-'*40}")
print(f"Bot: true  | Average Transaction Count: {avg_transaction_count_bot_true:.2f} (Count: {is_bot_true})")
print(f"Bot: false | Average Transaction Count: {avg_transaction_count_bot_false:.2f} (Count: {is_bot_false})\n")
print(f"WALLET LIFESPAN\n{'-'*40}")
print(f"- Average Wallet Lifespan: {avg_lifespan:.2f} days (Based on unique wallet creation dates)")

# The quartiles and ASCII bar charts would require more complex calculations and plotting libraries not ideal for bash.
# If needed, these could be computed and plotted using Python's matplotlib or similar libraries.

