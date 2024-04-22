#!/bin/bash

# WALLET INTELLIGENCE FROM FILE
# Version v1
# Last updated 2024.04.18
# For any questions, please contact us at matt@thirdwavelabs.com

# Requirements
# - `jq` for parsing Thirdwave API responses.
# - `parallel` for speeding up processing times.

# Initial flag setup
output_to_terminal=false

# Check for the presence of the -t flag
while getopts ":t" opt; do
  case $opt in
    t)
      output_to_terminal=true
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
  esac
done
shift $((OPTIND-1))

# Check for API key
if [ -f "apikey.txt" ]; then
    api_key=$(<apikey.txt)
else
    echo "API key file not found. Please ensure apikey.txt is in the same directory."
    exit 1
fi

export api_key

if [[ "$api_key" == "YOUR_API_KEY" ]]; then
    echo "Update apikey.txt with your API key. More info at https://docs.thirdwavelabs.com"
    exit 1
fi

# Record the start time
start_time=$(date +"%Y-%m-%d %H:%M:%S")

# Check if an input file is provided
if [[ -z "$1" ]]; then
    echo "Welcome to Wallet Intelligence!"
    echo "Please provide an input file containing wallet addresses."
    echo "./wi.sh <wallets>.txt
    exit 1
fi

input_file="$1"

# Ensure the input file exists and is readable
if [ ! -f "$input_file" ]; then
    echo "Error: File not found or not readable: $input_file"
    exit 1
fi

# Ensure the reports directory exists
mkdir -p reports

# Conditionally set the default output file based on the flag
if [[ "$output_to_terminal" == "true" ]]; then
    output_file=""
else
    output_file="reports/$(date +"%Y-%m-%d-%H-%M.csv")"
    echo "Wallet Address,Response,Is Bot,Spend,Total Balance,Transaction Count,Created At,Hodler Score,Temporal Activity,Transaction Velocity,Continuous Engagement,Funding Network" > "$output_file"
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

# Export the process_wallet function to be used by parallel
export -f process_wallet

# Adjust parallel command to process wallets
if [[ "$output_to_terminal" == "true" ]]; then
    parallel -j 10 --bar process_wallet {} :::: "$input_file"
else
    parallel -j 10 --bar process_wallet {} "$output_file" :::: "$input_file"
fi

# After processing, count the rows in the output CSV file, excluding the header row
if [[ "$output_to_terminal" == "false" ]]; then
    request_count=$(awk 'NR > 1' "$output_file" | wc -l)
else
    request_count=$(echo "$request_count" | wc -l)
fi

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

# Check and adjust final output handling based on the output destination
if [[ "$output_to_terminal" == "false" ]]; then
    echo "CSV file generated: $output_file"
    echo "Wallets Processed:  $(echo $request_count | xargs)"
else
    echo "Output sent to terminal."
fi
