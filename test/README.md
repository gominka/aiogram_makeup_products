# Telebot

## Short description
Telegram bot allows you to find the necessary cosmetic product.

## Description of the commands

### Command /start

  After selecting this command, a message is displayed containing the commands necessary to start the search, as well as:
1. If the user is using the bot for the first time:
   - The user is logged into the database;

### Commands /brand, /product_tag и /product_type

   After selecting one of the commands:
1. A list of attributes is displayed;
2. The user selects one of them;
3. After that, you must select a condition to continue the search.
   
### Commands /high, /low

   After selecting a command, the user selects using the buttons:
1. It is necessary to set a price or rating 
2. Enter a number; 
3. After that, you must select a condition to continue the search.
 
### Command /start_again
   After selecting the command:

1. All the previously selected conditions are reset
2. The search starts anew


The request for conditions continues for now:

 - The user will not select the "/start_again" command and start the search again;
 - The number of products satisfying all the selected conditions will not reach 3.
   - If this happens, the user selects the condition: 
     - The user selects the desired name
       - The description, product link and picture is displayed.

API Endpoint = http://makeup-api.herokuapp.com/api/v1/products.json
 