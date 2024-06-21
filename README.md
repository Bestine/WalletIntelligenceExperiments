# Wallet Intelligence Experiments

Wallet Intelligence is a simple HTTP REST API to enable all wallet-aware projects to make smarter business decisions through deep onchain analytics. It can help you answer questions like:

* Growth. Which wallets on my whitelist are bots?
* Insights. What is the average value of my customer wallets?
* Targeting. Who is most likely to make a purchase in my game?

This project is a catalog of experiments I've run using the API to understand audiences, evaluate projects, and study segments of wallets across the ecosystem. 

These projects are my own and not official releases from Thirdwave Labs. To learn about the latest developments, visit https://docs.thirdwavelabs.com

## PREREQUISITES 
Please complete the following prior to downloading the tutorial:

1) Sign up for Thirdwave API Key at https://docs.thirdwavelabs.com
2) Install Visual Studio Code (https://code.visualstudio.com/)

## DOWNLOAD TUTORIAL
Navigate to desired folder and run the following command to download these files. 

```
git clone https://github.com/mattlor/WalletIntelligenceExperiments/ 
```

## INSTALL API KEY
Open apikey.txt and replace "YOUR_API_KEY" with your Thirdwave API key before running the script

## RUN THIRDWAVE.PY
The thirdwave.py script can processes a single wallet or list of wallets as text files, CSVs, and JSON arrays as inputs. 
The output will be a CSV report that includes all current Wallet Intelligence fields. 

## REQUIREMENTS
This script using the Python requests library. You can install it using pip: `pip install requests`

## USAGE
`python3 thirdwave.py 0x606137dBaBaE484101C66e6De7d15Eb6D8161b19`
`python3 thirdwave.py <source file>.txt`
`python3 thirdwave.py <source file>.json`
`python3 thirdwave.py <source file>.csv`

## FLAGS
-t : Output to terminal only


## NEED DATA?
You can verify the script is working with the list of 1000 wallets in the `sampledata` folder. 

`python3 thirdwave.py sampledata/sample1k.txt`


# AUDIT.PY

`audit.py` is a useful utility to quickly generate a summary of wallet intelligence data once you generate the CSV results using `thirdwave.py`

## USAGE
python3 audit.py <walletintelligence.csv>

## FLAGS
-txt : Generate audience summary as a txt file
-html : Generate audience summary as an HTML file


## QUESTIONS? COMMENTS? FEEDBACK?
We're here to help. Reach out to matt@thirdwavelabs.com


# ADDITIONAL WALLET UTILITIES

* `walletcheck.py` validates Ethereum wallet addresses from an input file. It extracts potential wallet addresses and checks for their validity, listing unique wallets and reporting invalid entries.
* `walletcompare.py` processes two lists of wallet addresses from text files and outputs the unique wallets from each list.
* `walletextract.py` extracts wallet addresses from a txt, CSV, or JSON file and writes them to a text file for further processing. 