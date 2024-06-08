# Wallet Intelligence Audience Audit
# Run the audit on any Wallet Intelligence Report using `python3 audit.py wallet_intelligence.csv`
# Use -html to generate an HTML report
# Version 1.0 
# Updated on 2024.05.02

# REQUIREMENTS 
# If on Mac, install pandas and numpy with `pip3 install pandas numpy`

import sys
from datetime import datetime
from io import StringIO
import logging
# import pytz

import numpy as np
import pandas as pd

from format_report import generate_report

# Setup basic configuration for logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'
ERROR_THRESHOLD = 4
SECTION_HEADING_LENGTH = 75

def format_currency(num):
    """Format a number as currency."""
    if pd.notnull(num):
        return "${:,.0f}".format(round(num))
    else:
        return "N/A"

def format_section_heading(title):
    """Format a section heading."""
    section_heading = "=" * SECTION_HEADING_LENGTH
    padded_title = "> " + title
    return f"\n{section_heading}\n{padded_title}\n{section_heading}\n"

def identify_anomalies(wallet_data):
    """Identify anomalies in the wallet data."""
    anomalies = {}

    for column in ['Spend', 'Total Balance']:
        if wallet_data[column].dtype in ['int64', 'float64']:
            wallet_data[f'{column}_zscore'] = np.abs(wallet_data[column] - wallet_data[column].mean()) / wallet_data[column].std(ddof=0)
            anomalies[column] = wallet_data[wallet_data[f'{column}_zscore'] > ERROR_THRESHOLD]

    return anomalies

def calculate_wallet_age_stats(wallet_data):
    """Calculate wallet age statistics."""
    wallet_data['Created At'] = pd.to_datetime(wallet_data['Created At'], format=DATE_FORMAT, errors='coerce')
    current_date = datetime.now()
    wallet_data['Age'] = (current_date - wallet_data['Created At']).dt.days
    median_age = wallet_data['Age'].median()
    mean_age = wallet_data['Age'].mean()
    min_age = wallet_data['Age'].min()
    max_age = wallet_data['Age'].max()
    return median_age, mean_age, min_age, max_age

def potential_non_bots(wallet_data):
    """Identify potential non-bots based on transaction count."""
    potential_bots = wallet_data[wallet_data['Is Bot'] == False].sort_values(by='Transaction Count', ascending=False).head(10)
    potential_bots['Transaction Count'] = potential_bots['Transaction Count'].astype(int)

    if not potential_bots.empty:
        print(format_section_heading("Top 10 Transaction Count, Non-Bots"))

        col_1_name = "Wallet Address"
        col_1_width = 42
        col_2_name = "Transaction Count"
        col_2_width = 20

        header_row = f"{col_1_name:<{col_1_width}} | {col_2_name:>{col_2_width}}"
        print(header_row)
        # print("-" * len(header_row))

        for _, row in potential_bots.iterrows():
            print(f"{row['Wallet Address']:<{col_1_width}} | {row['Transaction Count']:>{col_2_width}}")

def oldest_wallets(wallet_data):
    """Identify the oldest wallets."""
    oldest_wallets = wallet_data.nsmallest(10, 'Created At')
    if not oldest_wallets.empty:
        print(format_section_heading("Oldest Wallets"))

        col_1_name = "Wallet Address"
        col_1_width = 42
        col_2_name = "Created At"
        col_2_width = 20 
        col_3_name = "Days Old"
        col_3_width = 8

        oldest_wallets['Created At'] = pd.to_datetime(oldest_wallets['Created At'], errors='coerce')
        oldest_wallets['Days Old'] = (datetime.now() - oldest_wallets['Created At']).dt.days

        header_row = f"{col_1_name:<{col_1_width}} | {col_2_name:<{col_2_width}} | {col_3_name:>{col_3_width}}"
        print(header_row)
        # print("-" * len(header_row))

        for _, row in oldest_wallets.iterrows():
            created_at = row['Created At'].strftime('%Y-%m-%d %H:%M:%S')  # Format timestamp without milliseconds
            print(f"{row['Wallet Address']:<{col_1_width}} | {created_at:<{col_2_width}} | {row['Days Old']:>{col_3_width}}")

def daily_transactions_leaderboard(wallet_data):
    """Identify the top 10 wallets with the highest daily transaction rate."""
    # Filter wallets based on criteria
    filtered_wallets = wallet_data[(wallet_data['Is Bot'] == False) & (wallet_data['Age'] > 10)].copy()

    filtered_wallets['Transaction Count'] = pd.to_datetime(filtered_wallets['Transaction Count'], errors="coerce")
    
    filtered_wallets.loc[:, 'Daily Transaction Rate'] = filtered_wallets['Transaction Count'] / filtered_wallets['Age']

    print("FILTERED WALLETS: ", filtered_wallets) # Check if exists on the original document
    
    leaderboard = filtered_wallets.nlargest(10, 'Daily Transaction Rate')

    print(format_section_heading("Daily Transactions Leaderboard (Non-Bots, >10 Days Old)"))

    col_1_name = "Wallet Address"
    col_1_width = 42
    col_2_name = "Daily Transactions"
    col_2_width = 20
    col_3_name = "Days Old"
    col_3_width = 10

    header_row = f"{col_1_name:<{col_1_width}} | {col_2_name:>{col_2_width}} | {col_3_name:>{col_3_width}}"
    print(header_row)
    # print("-" * len(header_row))

    for _, row in leaderboard.iterrows():
        print(f"{row['Wallet Address']:<{col_1_width}} | {row['Daily Transaction Rate']:>{col_2_width}.2f} | {row['Age']:>{col_3_width}.0f}")

def daily_transactions_leaderboard_modified(wallet_data):
    """
    A new function to correct the issue in the original one 
    """

    # Calculate wallet data age in days 
    current_time = datetime.now()
    #wallet_data["Created At"] = pd.to_datetime(wallet_data["Created At"], errors="coerce")
    wallet_data["Age"] = (current_time - wallet_data['Created At']).dt.days

    # Filter based on the criteria above(original function)
    filtered_wallets = wallet_data[(wallet_data['Is Bot'] == False) & (wallet_data['Age'] > 10)].copy()
    
    # calculate the daily transaction rate 
    #filtered_wallets['Transaction Count'] = pd.to_numeric(filtered_wallets['Transaction Count'], errors="coerce")
    filtered_wallets.loc[:, 'Daily Transaction Rate'] = filtered_wallets['Transaction Count'] / filtered_wallets['Age']

    leaderboard = filtered_wallets.nlargest(10, 'Daily Transaction Rate')

    print(format_section_heading("Daily Transactions Leaderboard (Non-Bots, >10 Days Old)"))

    col_1_name = "Wallet Address"
    col_1_width = 42
    col_2_name = "Daily Transactions"
    col_2_width = 20
    col_3_name = "Days Old"
    col_3_width = 10

    header_row = f"{col_1_name:<{col_1_width}} | {col_2_name:>{col_2_width}} | {col_3_name:>{col_3_width}}"
    print(header_row)
    # print("-" * len(header_row))

    for _, row in leaderboard.iterrows():
        print(f"{row['Wallet Address']:<{col_1_width}} | {row['Daily Transaction Rate']:>{col_2_width}.2f} | {row['Age']:>{col_3_width}.0f}")


def print_bot_summary(wallet_data):
    """Print a summary of bot behaviors."""
    bot_true_df = wallet_data[wallet_data['Is Bot'] == True]
    total_true_bots = bot_true_df.shape[0]

    temporal_activity_count = bot_true_df[bot_true_df['Temporal Activity'] == True].shape[0]
    transaction_velocity_count = bot_true_df[bot_true_df['Transaction Velocity'] == True].shape[0]
    continuous_engagement_count = bot_true_df[bot_true_df['Continuous Engagement'] == True].shape[0]
    funding_network_count = bot_true_df[bot_true_df['Funding Network'] == True].shape[0]

    temporal_activity_pct = (temporal_activity_count / total_true_bots) * 100 if total_true_bots > 0 else 0
    transaction_velocity_pct = (transaction_velocity_count / total_true_bots) * 100 if total_true_bots > 0 else 0
    continuous_engagement_pct = (continuous_engagement_count / total_true_bots) * 100 if total_true_bots > 0 else 0
    funding_network_pct = (funding_network_count / total_true_bots) * 100 if total_true_bots > 0 else 0

    print(f"--- Bot Behaviors ---")
    print(f"    Temporal Activity: {temporal_activity_count} ({temporal_activity_pct:.2f}%)")
    print(f" Transaction Velocity: {transaction_velocity_count} ({transaction_velocity_pct:.2f}%)")
    print(f"Continuous Engagement: {continuous_engagement_count} ({continuous_engagement_pct:.2f}%)")
    print(f"      Funding Network: {funding_network_count} ({funding_network_pct:.2f}%)")

def main(csv_file, output_format=None, summary_only=False):
    """Main function to perform the wallet intelligence audience audit."""
    wallet_data = pd.read_csv(csv_file)
    columns_to_clean = ['Spend', 'Total Balance', 'Transaction Count', 
                        'Hodler Score', 'Spend Games']
    for column in columns_to_clean:
        wallet_data[column] = pd.to_numeric(wallet_data[column], errors='coerce')

    bool_columns = ['Is Bot', 'Temporal Activity', 'Transaction Velocity', 
                    'Continuous Engagement', 'Funding Network']
    for column in bool_columns:
        wallet_data[column] = wallet_data[column].map({'True': True, 
                                                       'False': False, 
                                                       'unknown': np.nan, 
                                                       True: True, 
                                                       False: False})

    total_wallets = len(wallet_data)
    unique_wallets = wallet_data['Wallet Address'].nunique()
    duplicate_occurrences = total_wallets - unique_wallets

    # Remove duplicate wallet addresses from wallet data
    wallet_data = wallet_data.drop_duplicates(subset=['Wallet Address'], keep='first')

    unique_wallets = len(wallet_data)
    #normal_wallets = wallet_data[(wallet_data['Is Bot'] == False) & (wallet_data['Transaction Count'] > 0)].shape[0]
    
    normal_wallets = wallet_data[
        (wallet_data['Is Bot'] == False) &
        ((wallet_data['Transaction Count'] > 0) |
        (wallet_data['Spend'] > 0) |
        (wallet_data['Total Balance'] > 0))
        ].shape[0]
    
    #zero_outbound_wallets = wallet_data[(wallet_data['Total Balance'] == 0) & (wallet_data['Transaction Count'] == 0) & (wallet_data['Spend'] == 0)].shape[0]
    zero_outbound_wallets = wallet_data[
        (wallet_data['Is Bot'] == False) & 
        (wallet_data['Transaction Count'] == 0) & 
        (wallet_data['Spend'] == 0) &
        (wallet_data['Total Balance'] == 0)
        ].shape[0]
    
    null_results = wallet_data.isnull().sum()
    fresh_wallets = zero_outbound_wallets + null_results['Spend']
    bot_wallets = wallet_data[wallet_data['Is Bot'] == True].shape[0]

    print(format_section_heading("Summary of Analysis"))
    print(f"Total Wallets Submitted: {total_wallets}")
    print(f"Unique Wallets Analyzed: {unique_wallets} (Duplicates Removed: {duplicate_occurrences})")
    print()
    print(f"Normal Wallets (IsBot: False, Outbound Activity: True): {normal_wallets} ({normal_wallets / unique_wallets * 100:.2f}%)")
    print(f"Fresh Wallets (IsBot: False, Outbound Activity: False): {fresh_wallets} ({fresh_wallets / unique_wallets * 100:.2f}%)")
    print(f"Bot Wallets (IsBot: True): {bot_wallets} ({bot_wallets / unique_wallets * 100:.2f}%)")
    
    # Check Totals 
    # total_check = normal_wallets + fresh_wallets + bot_wallets
    # print(f"MECE Total Unique Wallets Check: {total_check}")

    print()

    if summary_only:
        return
    
    # Section: Wallet Metrics
    median_spend_per_wallet = wallet_data['Spend'].median()
    mean_spend_per_wallet = wallet_data['Spend'].mean()
    min_spend_per_wallet = wallet_data['Spend'].min()
    max_spend_per_wallet = wallet_data['Spend'].max()

    median_balance_per_wallet = wallet_data['Total Balance'].median()
    mean_balance_per_wallet = wallet_data['Total Balance'].mean()
    min_balance_per_wallet = wallet_data['Total Balance'].min()
    max_balance_per_wallet = wallet_data['Total Balance'].max()

    median_transaction_count_per_wallet = wallet_data['Transaction Count'].median()
    mean_transaction_count_per_wallet = wallet_data['Transaction Count'].mean()
    min_transaction_count_per_wallet = wallet_data['Transaction Count'].min()
    max_transaction_count_per_wallet = wallet_data['Transaction Count'].max()

    median_spend_games_per_wallet = wallet_data['Spend Games'].median()
    mean_spend_games_per_wallet = wallet_data['Spend Games'].mean()
    min_spend_games_per_wallet = wallet_data['Spend Games'].min()
    max_spend_games_per_wallet = wallet_data['Spend Games'].max()

    median_transaction_value = wallet_data['Spend'].sum() / wallet_data['Transaction Count'].sum() if wallet_data['Transaction Count'].sum() != 0 else 0

    median_wallet_age, mean_wallet_age, min_wallet_age, max_wallet_age = calculate_wallet_age_stats(wallet_data)

    print(format_section_heading("Wallet Metrics"))
    print(f"{'Metric':<30} | {'Median':<10} | {'Average':<10} | {'Min':<10} | {'Max':<10}")
    print(f"{'Spend per Wallet':<30} | {format_currency(median_spend_per_wallet):<10} | {format_currency(mean_spend_per_wallet):<10} | {format_currency(min_spend_per_wallet):<10} | {format_currency(max_spend_per_wallet):<10}")
    print(f"{'Balance per Wallet':<30} | {format_currency(median_balance_per_wallet):<10} | {format_currency(mean_balance_per_wallet):<10} | {format_currency(min_balance_per_wallet):<10} | {format_currency(max_balance_per_wallet):<10}")
    print(f"{'Transaction Count per Wallet':<30} | {median_transaction_count_per_wallet:<10.0f} | {mean_transaction_count_per_wallet:<10.0f} | {min_transaction_count_per_wallet:<10.0f} | {max_transaction_count_per_wallet:<10.0f}")
    print(f"{'Spend Games per Wallet':<30} | {format_currency(median_spend_games_per_wallet):<10} | {format_currency(mean_spend_games_per_wallet):<10} | {format_currency(min_spend_games_per_wallet):<10} | {format_currency(max_spend_games_per_wallet):<10}")
    print(f"{'Transaction Value':<30} | {format_currency(median_transaction_value):<10} | {'N/A':<10} | {'N/A':<10} | {'N/A':<10}")
    print(f"{'Wallet Age (days)':<30} | {median_wallet_age:<10.0f} | {mean_wallet_age:<10.0f} | {min_wallet_age:<10.0f} | {max_wallet_age:<10.0f}")

    print(format_section_heading("Bot Report"))

    bot_true_df = wallet_data[wallet_data['Is Bot'].eq(True)]
    bot_false_df = wallet_data[wallet_data['Is Bot'].eq(False)]

    print(f"--- IsBot: False ---")
    print(f"Median Spend: {format_currency(bot_false_df['Spend'].median())} (Count: {bot_false_df.shape[0]})")
    print(f"Median Transaction Count: {bot_false_df['Transaction Count'].median():.0f} (Count: {bot_false_df.shape[0]})\n")

    print(f"--- IsBot: True ---")
    print(f"Median Spend: {format_currency(bot_true_df['Spend'].median())} (Count: {bot_true_df.shape[0]})")
    print(f"Median Transaction Count: {bot_true_df['Transaction Count'].median():.0f} (Count: {bot_true_df.shape[0]})")
    print()

    print_bot_summary(wallet_data)

    anomalies = identify_anomalies(wallet_data)

    print(format_section_heading("Anomaly Detection"))

    for category, anomaly_df in anomalies.items():
        if category in ['Spend', 'Total Balance']:
            anomaly_df = anomaly_df.sort_values(by=f'{category}_zscore', ascending=False)
            anomaly_df[category] = anomaly_df[category].apply(format_currency)

        print(f"--- Anomalies in {category} ---")
        print(f"{'Wallet Address':<42} | {category:>14}")
        # print("-" * 60) #table header line
        for _, row in anomaly_df.iterrows():
            print(f"{row['Wallet Address']:<42} | {row[category]:>14}")
        print()

    potential_non_bots(wallet_data)
    oldest_wallets(wallet_data)

    print("DOES ANALYSIS CONTINUE?")

    daily_transactions_leaderboard_modified(wallet_data)  
    print()

    if output_format:
        output = sys.stdout.getvalue()
        generate_report(csv_file, output, output_format)
        sys.stdout = sys.__stdout__
        print(output)

if __name__ == "__main__":

    # daily leaderboard modified
    # daily_transactions_leaderboard_modified()

    # function 9
    main("audienceaudit/ExampleReport.csv")







    # if len(sys.argv) < 2:
    #     print("Usage: python3 audit.py <file>.csv [-html|-md|-txt|-csv] [-s]")
    #     sys.exit(1)
    
    # csv_file = sys.argv[1]
    # print(csv_file)
    # output_format = None
    # summary_only = False

    # if len(sys.argv) > 2:
    #     for arg in sys.argv[2:]:
    #         if arg in ['-html', '-md', '-txt', '-csv']:
    #             output_format = arg[1:]
    #         elif arg == '-s':
    #             summary_only = True
    #         else:
    #             print("Invalid argument. Supported arguments: -html, -md, -txt, -csv, -s")
    #             sys.exit(1)

    # if output_format:
    #     sys.stdout = StringIO()
    #     print(type(sys.stdout))

    # main(csv_file, output_format, summary_only)
    # sys.stdout = sys.__stdout__