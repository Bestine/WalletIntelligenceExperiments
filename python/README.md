# Wallet Intelligence Tutorial // Python

This tutorial will walk you through the basics of using Wallet Intelligence on a Mac. 

## PREREQUISITES 
Please complete the following prior to downloading the tutorial:

1) Sign up for Thirdwave API Key at https://docs.thirdwavelabs.com
2) Install Visual Studio Code (https://code.visualstudio.com/)

## DOWNLOAD TUTORIAL
Navigate to desired folder and run the following command to download tutorial files. 

```
git clone https://github.com/mattlor/WalletIntelligenceExperiments/ 
```

## INSTALL API KEY
Replace "YOUR_API_KEY" with your Thirdwave API key before running the script

## RUN THIRDWAVE.PY
The thirdwave.py script can processes a single wallet or list of wallets as text files, CSVs, and JSON arrays as inputs. 
The output will be a CSV report that includes all current Wallet Intelligence fields. 

## REQUIREMENTS
This script using the Python requests library. You can install it using pip: pip install requests 

## USAGE
`python3 thirdwave.py 0x606137dBaBaE484101C66e6De7d15Eb6D8161b19`
`python3 thirdwave.py <source file>.txt`
`python3 thirdwave.py <source file>.json`
`python3 thirdwave.py <source file>.csv`

## FLAGS
-t : Output to terminal only


## NEED DATA?
You can verify the script is working with the sample data file in this folder. 

`python3 thirdwave.py sample1k.txt`