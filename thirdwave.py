"""
THIRDWAVE WALLET INTELLIGENCE // Python Example
Version v1
Last updated 2024.04.24
For any questions, please contact us at matt@thirdwavelabs.com

OVERVIEW
This script can processes a single wallet or list of wallets as text files, CSVs, and JSON arrays as inputs. 
The output will be a CSV report that includes all current Wallet Intelligence fields. 

REQUIREMENTS
This script using the Python requests library. You can install it using pip: pip install requests 

USAGE
python3 thirdwave.py 0x606137dBaBaE484101C66e6De7d15Eb6D8161b19
python3 thirdwave.py <source file>.txt
python3 thirdwave.py <source file>.json
python3 thirdwave.py <source file>.csv

"""

import sys
import re
import json
import csv
import time
import requests
from datetime import datetime
import os

# Record the start time
start_time = datetime.now()

# Check for API key
try:
    with open("apikey.txt", "r") as file:
        api_key = file.read().strip()
except FileNotFoundError:
    print("API key file not found. Please ensure apikey.txt is in the same directory.")
    sys.exit(1)

if api_key == "YOUR_API_KEY":
    print("Update apikey.txt with your API key. More info at https://docs.thirdwavelabs.com")
    sys.exit(1)

# Check for -t flag
output_to_terminal = "-t" in sys.argv

# Check if an input file or wallet address is provided
if len(sys.argv) < 2:
    print("")
    print("Welcome to Wallet Intelligence!")
    print("Please provide a single wallet address or an input file containing wallet addresses in the following format:\n")
    print("python3 thirdwave.py 0x606137dBaBaE484101C66e6De7d15Eb6D8161b19")
    print("python3 thirdwave.py <source file>.txt")
    print("python3 thirdwave.py <source file>.json")
    print("python3 thirdwave.py <source file>.csv")
    print("")
    sys.exit(1)

input_arg = sys.argv[1]

# Check if the input argument is a single wallet address
if input_arg.startswith("0x") and len(input_arg) == 42:
    wallet_addresses = [input_arg]
    use_batch_endpoint = False
else:
    # Treat the input argument as a file path
    input_file = input_arg

    # Ensure the input file exists and is readable
    try:
        with open(input_file, "r") as file:
            pass
    except FileNotFoundError:
        print(f"Error: File not found or not readable: {input_file}")
        sys.exit(1)

    # Extract wallet addresses based on the file extension
    wallet_addresses = []

    if input_file.endswith(".txt"):
        with open(input_file, "r") as file:
            content = file.read()
            wallet_addresses = re.findall(r"0x[a-fA-F0-9]{40}", content)
    elif input_file.endswith(".json"):
        with open(input_file, "r") as file:
            data = json.load(file)
            if isinstance(data, list):
                wallet_addresses = [item for item in data if re.match(r"^0x[a-fA-F0-9]{40}$", item)]
            else:
                print("Invalid JSON format. Expected a list of wallet addresses.")
                sys.exit(1)
    elif input_file.endswith(".csv"):
        with open(input_file, "r") as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip header row
            for row in csv_reader:
                if len(row) > 0:
                    wallet_address = row[0]
                    if re.match(r"^0x[a-fA-F0-9]{40}$", wallet_address):
                        wallet_addresses.append(wallet_address)
    else:
        print("Unsupported file format. Please provide a .txt, .json, or .csv file.")
        sys.exit(1)

    use_batch_endpoint = len(wallet_addresses) > 100

if not output_to_terminal:
    # Create the reports directory if it doesn't exist
    os.makedirs("reports", exist_ok=True)

    # Record the start time
    start_time = datetime.now()

# Set the batch size
batch_size = 5000

# Process each wallet address or batch of addresses
if not output_to_terminal:
    output_file = f"reports/{start_time.strftime('%Y-%m-%d-%H-%M')}.csv"
    with open(output_file, "w", newline="") as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow([
            "Wallet Address",
            "Status Code",
            "Response",
            "Total Balance",
            "Transaction Count",
            "Spend",
            "Spend Games",
            "Created At",
            "Hodler Score",
            "Is Bot",
            "Temporal Activity",
            "Transaction Velocity",
            "Continuous Engagement",
            "Funding Network"
            ])

        if use_batch_endpoint:
            total_batches = (len(wallet_addresses) + batch_size - 1) // batch_size
            for batch_num in range(total_batches):
                start_index = batch_num * batch_size
                end_index = min((batch_num + 1) * batch_size, len(wallet_addresses))
                batch_addresses = wallet_addresses[start_index:end_index]

                print(f"Processing batch {batch_num + 1} of {total_batches}")
                print(f"Wallets {start_index + 1} to {end_index}")

                # Make batch API request
                response = requests.post(
                    "https://wi.thirdwavelabs.com/evm/wallets/batch",
                    headers={"X-Api-Key": api_key, "Content-Type": "application/json"},
                    json=batch_addresses
                )
                status_code = response.status_code

                if status_code == 200:
                    response_body = response.json()
                    for i, wallet_data in enumerate(response_body):
                        if wallet_data is not None:
                            csv_writer.writerow([
                                wallet_data.get("address", "unknown"),
                                status_code,
                                "Success",
                                wallet_data.get("totalBalance", "unknown"),
                                wallet_data.get("transactionCount", "unknown"),
                                wallet_data.get("spend", "unknown"),
                                wallet_data.get("spendGames", "unknown"),
                                wallet_data.get("createdAt", "unknown"),
                                wallet_data.get("hodlerScore", "unknown"),
                                wallet_data.get("isBot", False),
                                wallet_data.get("botBehaviors", {}).get("temporalActivity", False),
                                wallet_data.get("botBehaviors", {}).get("transactionVelocity", False),
                                wallet_data.get("botBehaviors", {}).get("continuousEngagement", False),
                                wallet_data.get("botBehaviors", {}).get("fundingNetwork", False)
                            ])
                        else:
                            csv_writer.writerow([
                                batch_addresses[i],
                                "null",
                                "Wallet Not Found",
                                "unknown",
                                "unknown",
                                "unknown",
                                "unknown",
                                "unknown",
                                "unknown",
                                "unknown",
                                "unknown",
                                "unknown",
                                "unknown",
                                "unknown"
                            ])
                else:
                    error_message = response.text
                    for address in batch_addresses:
                        csv_writer.writerow([
                            address,
                            status_code,
                            f"Error: {error_message}",
                            "unknown",
                            "unknown",
                            "unknown",
                            "unknown",
                            "unknown",
                            "unknown",
                            "unknown",
                            "unknown",
                            "unknown",
                            "unknown",
                            "unknown"
                        ])
        else:
            total_addresses = len(wallet_addresses)
            processed_count = 0

            for address in wallet_addresses:
                # Make API request for each wallet address
                response = requests.get(f"https://wi.thirdwavelabs.com/evm/wallets/{address}", headers={"X-Api-Key": api_key})
                status_code = response.status_code

                processed_count += 1
                remaining_count = total_addresses - processed_count

                print(f"Wallets {remaining_count}:{processed_count}")
                print(f"{status_code} {address} {response.text}\n")

                try:
                    response_body = response.json()
                except requests.exceptions.JSONDecodeError as e:
                    print(f"Wallet Not Found at {address}. Please check for any formatting issues or unexpected characters.")
                    csv_writer.writerow([
                        address,
                        status_code,
                        "Wallet Not Found",
                        "unknown",
                        "unknown",
                        "unknown",
                        "unknown",
                        "unknown",
                        "unknown",
                        "unknown",
                        "unknown",
                        "unknown",
                        "unknown",
                        "unknown"
                    ])
                    continue

                if status_code == 200:
                    csv_writer.writerow([
                        address,
                        status_code,
                        "Success",
                        response_body.get("totalBalance", "unknown"),
                        response_body.get("transactionCount", "unknown"),
                        response_body.get("spend", "unknown"),
                        response_body.get("spendGames", "unknown"),
                        response_body.get("createdAt", "unknown"),
                        response_body.get("hodlerScore", "unknown"),
                        response_body.get("isBot", False),
                        response_body.get("botBehaviors", {}).get("temporalActivity", False),
                        response_body.get("botBehaviors", {}).get("transactionVelocity", False),
                        response_body.get("botBehaviors", {}).get("continuousEngagement", False),
                        response_body.get("botBehaviors", {}).get("fundingNetwork", False)
                    ])
                else:
                    error_message = response_body.get("error", {}).get("message", "")
                    csv_writer.writerow([
                        address,
                        status_code,
                        f"Error: {error_message}",
                        "unknown",
                        "unknown",
                        "unknown",
                        "unknown",
                        "unknown",
                        "unknown",
                        "unknown",
                        "unknown",
                        "unknown",
                        "unknown",
                        "unknown"
                    ])

else:
    if use_batch_endpoint:
        total_batches = (len(wallet_addresses) + batch_size - 1) // batch_size
        for batch_num in range(total_batches):
            start_index = batch_num * batch_size
            end_index = min((batch_num + 1) * batch_size, len(wallet_addresses))
            batch_addresses = wallet_addresses[start_index:end_index]

            print(f"Processing batch {batch_num + 1} of {total_batches}")
            print(f"Wallets {start_index + 1} to {end_index}")

            # Make batch API request
            response = requests.post(
                "https://wi.thirdwave.com/evm/wallets/batch",
                headers={"X-Api-Key": api_key, "Content-Type": "application/json"},
                json=batch_addresses
            )
            status_code = response.status_code

            if status_code == 200:
                response_body = response.json()
                for i, wallet_data in enumerate(response_body):
                    if wallet_data is not None:
                        print(f"{status_code} {wallet_data.get('address', 'unknown')} {json.dumps(wallet_data)}\n")
                    else:
                        print(f"null {batch_addresses[i]} Missing Data\n")
            else:
                error_message = response.text
                for address in batch_addresses:
                    print(f"{status_code} {address} Error: {error_message}\n")

    else:
        total_addresses = len(wallet_addresses)
        processed_count = 0

        for address in wallet_addresses:
            # Make API request for each wallet address
            response = requests.get(f"https://wi.thirdwavelabs.com/evm/wallets/{address}", headers={"X-Api-Key": api_key})
            status_code = response.status_code

            processed_count += 1
            remaining_count = total_addresses - processed_count

            print(f"Wallets {remaining_count}:{processed_count}")
            print(f"{status_code} {address} {response.text}\n")

if not output_to_terminal:
    # Record the finish time
    finish_time = datetime.now()

    # Print the performance summary
    print("\nPerformance Summary:")
    print(f" Start Time: {start_time}")
    print(f"Finish Time: {finish_time}")

    # Calculate the total time
    total_seconds = (finish_time - start_time).total_seconds()
    minutes = int(total_seconds // 60)
    seconds = int(total_seconds % 60)
    print(f" Total Time: {minutes} minutes {seconds} seconds")

    # Count the rows in the output CSV file, excluding the header row
    with open(output_file, "r") as file:
        csv_reader = csv.reader(file)
        request_count = sum(1 for _ in csv_reader) - 1

    print(f"\nCSV file generated: {output_file}")
    print(f" Wallets Processed: {request_count}\n")
else:
    finish_time = datetime.now()
    total_seconds = (finish_time - start_time).total_seconds()
    minutes = int(total_seconds // 60)
    seconds = int(total_seconds % 60)
    print(f"\nTotal Time: {minutes} minutes {seconds} seconds")
    print(f"Wallets Processed: {len(wallet_addresses)}\n")