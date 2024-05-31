// 2024.3.19 added funding network and default wallet for easier debugging
// 2024.3.19 added Google's cache service to avoid reloading data constantly. Use WalletIntelligenceLive to bypass cache.

function WalletIntelligenceCached(wallet = '0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045') {
  var cache = CacheService.getScriptCache();
  var cacheKey = 'walletInfo_' + wallet;
  var cachedData = cache.get(cacheKey);

  if (cachedData) {
    Logger.log('Retrieved from cache');
    return cachedData;
  }

  var url = `https://wi.thirdwavelabs.com/wallet/${wallet}`;
  
  // matt@zakari.com API key created 2024.3.19 eyJvcmciOiIiLCJpZCI6ImYxY2RlMWYzNjViNzQ1YjE4YWM0OGI5YjE1NGRmN2E4IiwiaCI6Im11cm11cjEyOCJ9
  // steppa key on 2024.03.22 eyJvcmciOiIiLCJpZCI6IjhmMDZkN2RiY2UxYzQ0MTY4ODQ3ODVkOWU3ODkzYTJhIiwiaCI6Im11cm11cjEyOCJ9
  var api_key = 'eyJvcmciOiIiLCJpZCI6ImYxY2RlMWYzNjViNzQ1YjE4YWM0OGI5YjE1NGRmN2E4IiwiaCI6Im11cm11cjEyOCJ9';

  var options = {
    method: 'GET',
    headers: {
      'X-Api-Key': `${api_key}`
    },
    muteHttpExceptions: true
  };

  var response = UrlFetchApp.fetch(url, options);
  var json = JSON.parse(response.getContentText());
  var userData = json.data;
 
  Logger.log(userData);
 
  // Extract all elements from the API response
  var wallet = userData.evm.wallet.address || "null";
  var totalBalance = userData.evm.wallet.totalBalance || "null";
  var createdAt = userData.evm.wallet.createdAt || "null";
  var transactionCount = userData.evm.wallet.transactionCount || "null";
  var isBot = userData.evm.wallet.isBot ? "true" : "false";
  var hodlerScore = userData.evm.wallet.hodlerScore || "null";
  var spend = userData.evm.wallet.spend || "null";
  var temporalActivity = userData.evm.wallet.botBehaviors.temporalActivity ? "true" : "false";
  var continuousEngagement = userData.evm.wallet.botBehaviors.continuousEngagement ? "true" : "false";
  var fundingNetwork = userData.evm.wallet.botBehaviors.fundingNetwork ? "true" : "false";
  var transactionVelocity = userData.evm.wallet.botBehaviors.transactionVelocity ? "true" : "false";

  // Create the formatted string with "|" as separators
  var infoString =
    wallet + "|" +
    totalBalance + "|" +
    createdAt + "|" +
    transactionCount + "|" +
    isBot + "|" +
    hodlerScore + "|" +
    spend + "|" +
    temporalActivity + "|" +
    continuousEngagement + "|" +
    fundingNetwork + "|" +
    transactionVelocity;

  Logger.log(infoString);

  // Store the result in the cache for future use
  cache.put(cacheKey, infoString, 21600); // Cache expiration time set to 6 hours (21600 seconds)

  return infoString;
}


function WalletIntelligenceLive(wallet = '0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045') {
  var url = `https://wi.thirdwavelabs.com/wallet/${wallet}`;
  
  // API TOKEN Team Token eyJvcmciOiIiLCJpZCI6IjBjZmEyZmI1YTQxMDQxODA5Y2RlNDRmMTA5N2ZmNTljIiwiaCI6Im11cm11cjEyOCJ9 
  // API Unlimited eyJvcmciOiIiLCJpZCI6IjhmMDZkN2RiY2UxYzQ0MTY4ODQ3ODVkOWU3ODkzYTJhIiwiaCI6Im11cm11cjEyOCJ9 
  // matt@zakari.com API key created 2024.3.19 eyJvcmciOiIiLCJpZCI6ImYxY2RlMWYzNjViNzQ1YjE4YWM0OGI5YjE1NGRmN2E4IiwiaCI6Im11cm11cjEyOCJ9

  var api_key = 'eyJvcmciOiIiLCJpZCI6ImYxY2RlMWYzNjViNzQ1YjE4YWM0OGI5YjE1NGRmN2E4IiwiaCI6Im11cm11cjEyOCJ9';

  var options = {
    method: 'GET',
    headers: {
      'X-Api-Key': `${api_key}`
    },
    muteHttpExceptions: true
  };

  var response = UrlFetchApp.fetch(url, options);
  var json = JSON.parse(response.getContentText());
  var userData = json.data;
 
  Logger.log(userData); // View the result in "View" > "Logs" menu in the Google Apps Script editor
 
  // Extract all elements from the API response
  // Instead of using the || operator, a ternary operator is used to check the value and return "true" or "false" accordingly
  var wallet = userData.evm.wallet.address || "null";
  var totalBalance = userData.evm.wallet.totalBalance || "null";
  var createdAt = userData.evm.wallet.createdAt || "null";
  var transactionCount = userData.evm.wallet.transactionCount || "null";
  var isBot = userData.evm.wallet.isBot ? "true" : "false";
  var hodlerScore = userData.evm.wallet.hodlerScore || "null";
  var spend = userData.evm.wallet.spend || "null";
  var temporalActivity = userData.evm.wallet.botBehaviors.temporalActivity ? "true" : "false";
  var continuousEngagement = userData.evm.wallet.botBehaviors.continuousEngagement ? "true" : "false";
  var fundingNetwork = userData.evm.wallet.botBehaviors.fundingNetwork ? "true" : "false";
  var transactionVelocity = userData.evm.wallet.botBehaviors.transactionVelocity ? "true" : "false";

  // Create the formatted string with "|" as separators
  var infoString =
    wallet + "|" +
    totalBalance + "|" +
    createdAt + "|" +
    transactionCount + "|" +
    isBot + "|" +
    hodlerScore + "|" +
    spend + "|" +
    temporalActivity + "|" +
    continuousEngagement + "|" +
    fundingNetwork + "|" +
    transactionVelocity;

  Logger.log(infoString);

  return infoString;
}



function WalletIntelligenceNew(wallet = '0xf45b42b64c44397ea5f08dfae70d1237f93d606f') {
  var url = `https://wi.thirdwavelabs.com/wallet/${wallet}`;

// company 85   eyJvcmciOiIiLCJpZCI6ImYxY2RlMWYzNjViNzQ1YjE4YWM0OGI5YjE1NGRmN2E4IiwiaCI6Im11cm11cjEyOCJ9
// company 1    eyJvcmciOiIiLCJpZCI6IjhmMDZkN2RiY2UxYzQ0MTY4ODQ3ODVkOWU3ODkzYTJhIiwiaCI6Im11cm11cjEyOCJ9

  var api_key = 'eyJvcmciOiIiLCJpZCI6ImYxY2RlMWYzNjViNzQ1YjE4YWM0OGI5YjE1NGRmN2E4IiwiaCI6Im11cm11cjEyOCJ9';

  var options = {
    method: 'GET',
    headers: {
      'X-Api-Key': api_key
    },
    muteHttpExceptions: true
  };

  try {
    var response = UrlFetchApp.fetch(url, options);
    var responseCode = response.getResponseCode();
    var content = response.getContentText();

    // Check if the response code is not 200 OK
    if (responseCode !== 200) {
      Logger.log("Error response received: " + content);
      return "Error: " + responseCode;
    }

    var json = JSON.parse(content);
    if (json.data === null || !json.data.evm) {
      Logger.log("Error response received: " + content);
      return "Error: " + content;
    }

    var userData = json.data;

    // Safe access to potentially undefined properties
    var evmWallet = userData.evm && userData.evm.wallet ? userData.evm.wallet : {};

    // Extract all elements from the API response using a more defensive approach
    var walletAddress = evmWallet.address || "null";
    var totalBalance = evmWallet.totalBalance || "null";
    var createdAt = evmWallet.createdAt || "null";
    var transactionCount = evmWallet.transactionCount || "null";
    var isBot = evmWallet.isBot ? "true" : "false";
    var hodlerScore = evmWallet.hodlerScore || "null";
    var spend = evmWallet.spend || "null";

    var botBehaviors = evmWallet.botBehaviors || {};
    var temporalActivity = botBehaviors.temporalActivity ? "true" : "false";
    var continuousEngagement = botBehaviors.continuousEngagement ? "true" : "false";
    var fundingNetwork = botBehaviors.fundingNetwork ? "true" : "false";
    var transactionVelocity = botBehaviors.transactionVelocity ? "true" : "false";

    // Create the formatted string with "|" as separators
    var infoString = [
      walletAddress,
      totalBalance,
      createdAt,
      transactionCount,
      isBot,
      hodlerScore,
      spend,
      temporalActivity,
      continuousEngagement,
      fundingNetwork,
      transactionVelocity
    ].join("|");

    Logger.log(infoString);
    return infoString;

  } catch (e) {
    // Catch any errors that occur during the execution of the script
    Logger.log("Caught an exception: " + e.toString());
    return "Error: Exception occurred";
  }
}
