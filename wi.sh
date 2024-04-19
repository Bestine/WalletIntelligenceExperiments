#!/bin/bash

# WALLET INTELLIGENCE FROM FILE
# Version v1
# Last updated 2024.04.18
# For any questions, please contact us at matt@thirdwavelabs.com

# Requirements
# This project relies on specific tools to handle data processing and task execution efficiently:
# - `jq` is used for parsing Thirdwave API responses.
# - `parallel` is used for speeding up processing times.

# How it works
# The following command will output a CSV of Wallet Intelligence data for any list of wallets
# cat <list of wallets>.txt | ./wi.sh 
# Add the -t flag to output directly to terminal 
# cat <list of wallets>.txt | ./wi.sh -t

# Replace YOUR_API_KEY in apikey.txt with your API key from Thirdwave. More info at https://docs.thirdwavelabs.com
if [ -f "apikey.txt" ]; then
    api_key=$(<apikey.txt)
else
    echo "API key file not found. Please ensure APIKEY.txt is in the same directory."
    exit 1
fi

export api_key

if [[ "$api_key" == "YOUR_API_KEY" ]]; then
    echo "It looks like you haven't added your Thirdwave API key to the script. Please update APIKEY.txt with your API key to continue. More info at https://docs.thirdwavelabs.com"
    exit 1
fi

# Record the start time
start_time=$(date +"%Y-%m-%d %H:%M:%S")

if [ -t 0 ]; then
echo
echo "Welcome to Wallet Intelligence!"
echo "To run the API script, provide wallet addresses via stdin."
echo "Example usage: cat wallet_addresses.txt | ./wi.sh"
echo
exit 1
fi

# Function to process each wallet address
process_wallet() {

    address="$1"
    output_file="$2"
    temp_file=$(mktemp)

    # Make API request for each wallet address with a unique delimiter "###" for separating the response from the HTTP status code
    OUTPUT=$(curl -s --request GET "https://wi.thirdwavelabs.com/wallet/$address" \
            --header "X-Api-Key: $api_key" -w '###%{http_code}')

    # Split the response and the HTTP status code using the delimiter "###"
    RESPONSE_BODY=$(echo "$OUTPUT" | awk -F'###' '{print $1}')
    HTTP_STATUS=$(echo "$OUTPUT" | awk -F'###' '{print $2}')

    # Check if the response contains a null wallet or any error messages
    if echo "$RESPONSE_BODY" | grep -q '"wallet":null' || echo "$RESPONSE_BODY" | grep -q 'error'; then
        # Sanitize the error message by removing commas and newlines
        sanitized_error=$(echo "$RESPONSE_BODY" | jq -r '.error.message // "API error"')
        sanitized_error=$(echo "$sanitized_error" | tr ',' ' ' | tr '\n' ' ')

        # Output the sanitized error message in the "Response" field with the status code
        echo "$address,\"Error: $sanitized_error, Status: $HTTP_STATUS\",unknown,unknown,unknown,unknown,unknown,unknown,unknown,unknown,unknown,unknown" > "$temp_file"
    else
        # Extract relevant data using jq, handling null values
        wallet_address=$(echo "$RESPONSE_BODY" | jq -r '.address // ""')
        isBot=$(echo "$RESPONSE_BODY" | jq -r '.isBot // false')
        spend=$(echo "$RESPONSE_BODY" | jq -r '.spend // "unknown"')
        totalBalance=$(echo "$RESPONSE_BODY" | jq -r '.totalBalance // "unknown"')
        transactionCount=$(echo "$RESPONSE_BODY" | jq -r '.transactionCount // "unknown"')
        createdAt=$(echo "$RESPONSE_BODY" | jq -r '.createdAt // "unknown"')
        hodlerScore=$(echo "$RESPONSE_BODY" | jq -r '.hodlerScore // "unknown"')
        temporalActivity=$(echo "$RESPONSE_BODY" | jq -r '.botBehaviors.temporalActivity // false')
        transactionVelocity=$(echo "$RESPONSE_BODY" | jq -r '.botBehaviors.transactionVelocity // false')
        continuousEngagement=$(echo "$RESPONSE_BODY" | jq -r '.botBehaviors.continuousEngagement // false')
        fundingNetwork=$(echo "$RESPONSE_BODY" | jq -r '.botBehaviors.fundingNetwork // false')
        
        # Output data to the temporary file with the status code
        echo "$address,$HTTP_STATUS,$isBot,$spend,$totalBalance,$transactionCount,$createdAt,$hodlerScore,$temporalActivity,$transactionVelocity,$continuousEngagement,$fundingNetwork" > "$temp_file"
    fi

    # Append the temporary file to the output file if not in terminal mode
    if [[ -n "$output_file" ]]; then
        cat "$temp_file" >> "$output_file"
    else
        cat "$temp_file"
    fi

    # Remove the temporary file
    rm "$temp_file"
}

export -f process_wallet

# Set the default output file
output_file=$(date +"%Y-%m-%d-%H-%M.csv")

# Check if the -t flag is provided
if [[ "$1" == "-t" ]]; then
  output_file=""
else
  echo "Wallet Address,Response,Is Bot,Spend,Total Balance,Transaction Count,Created At,Hodler Score,Temporal Activity,Transaction Velocity,Continuous Engagement,Funding Network" > "$output_file"
fi

# Read wallet addresses from stdin and process them in parallel with a limit of 10 jobs
parallel -j 10 --bar process_wallet ::: $(</dev/stdin) ::: "$output_file"

# After processing, count the rows in the output CSV file, excluding the header row
request_count=$(awk 'NR > 1' "$output_file" | wc -l)

# Record the finish time
finish_time=$(date +"%Y-%m-%d %H:%M:%S")

# Print the performance summary
echo
echo "Performance Summary:"
echo "Start Time:  $start_time"
echo "Finish Time: $finish_time"

# Calculate the total time
start_seconds=$(date -j -f "%Y-%m-%d %H:%M:%S" "$start_time" +%s)
finish_seconds=$(date -j -f "%Y-%m-%d %H:%M:%S" "$finish_time" +%s)
total_seconds=$((finish_seconds - start_seconds))

# Convert total time to minutes and seconds
minutes=$((total_seconds / 60))
seconds=$((total_seconds % 60))

echo "Total Time:  $minutes minutes $seconds seconds"
echo

# The request count and file path are relevant in both cases but handled differently
if [[ -n "$output_file" ]]; then
echo "CSV file generated: $output_file"
echo "Wallets Processed:  $(echo $request_count | xargs) "
echo
fi
