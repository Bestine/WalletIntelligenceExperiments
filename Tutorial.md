# Wallet Intelligence Tutorial

This tutorial will walk you through the basics of using Wallet Intelligence. 


## PREREQUISITES 
Please complete the following prior to downloading the tutorial:

1) Sign up for Thirdwave API Key at https://docs.thirdwavelabs.com
2) Install Visual Studio Code (https://code.visualstudio.com/)
3) Open Terminal and install Homebrew (instructions here: https://brew.sh/)
4) parallel (brew install parallel)
5) jq (brew install jq)

## DOWNLOAD TUTORIAL
Navigate to desired folder and run the following command to download tutorial files. 

```
git clone https://github.com/mattlor/WalletIntelligenceTutorial.git
```

## SET PERMISSIONS
Run the following command to set executable permissions on the Wallet Intelligence script. 
```
chmod +x wi.sh 
```


## RUN WALLET INTELLIGENCE
Add your Thirdwave API key to the script to begin the tests. 

### NO INPUT 
```
./wi.sh 
```
### TXT INPUT
```
cat ten.txt | ./wi.sh
```

### TERMINAL flag
```
cat ten.txt | ./wi.sh -t 
```
### ETHERSCAN EXPORT
Pull Audience Statistics for NFT or Token Holders

1. Navigate to OpenSea to find the Etherscan Contract link https://opensea.io/collection/sugartownoras
2. Open Etherscan Export Data Page and Select “ERC-721 or ERC-1155" https://etherscan.io/exportData?type=tokenholders-nft&contract=0xd564c25b760cb278a55bdd98831f4ff4b6c97b38
3. It’s possible to extract wallets from the default Etherscan Export and generate report with this code:
```
cat etherscan_export.csv | sed '1d' | awk -F ',' '{print $1}' | sed 's/"//g' | ./wi.sh
```

