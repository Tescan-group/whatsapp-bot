# StockBot: A WhatsApp Chatbot for Inventory Management

**StockBot** is a WhatsApp chatbot designed to manage inventory levels for products. It allows users to check stock levels, add or reduce stock quantities, and log transactions in a MongoDB database. The bot is built using Python and Flask and integrates with Twilio's WhatsApp API for messaging.

## Features

- **Check Stock**: View the current stock level for a product.
- **Add Stock**: Increase the stock level for a product.
- **Reduce Stock**: Decrease the stock level for a product.
- **Transaction Logs**: Record all transactions with timestamps and counts.

## Installation

To install and run StockBot, follow the steps below.

### Prerequisites

- **Python 3.x**
- **MongoDB**: A MongoDB instance, either local or remote.
- **Twilio**: A Twilio account for WhatsApp API integration.

### Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Tescan-group/whatsapp-bot.git
   cd whatsapp-bot
   ```

2. **Install Required Packages**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Environment Variables**

   Create a `.env` file in the root directory and add your MongoDB URI and any other required environment variables.

   ```plaintext
   MONGO_URI=your_mongodb_connection_string
   ```

4. **Update Twilio Webhook**

   In your [Twilio Console](https://www.twilio.com/console), configure the webhook URL for incoming messages:

   ```
   https://your-domain.com/webhook
   ```

   - If running locally, you can use [ngrok](https://ngrok.com/) to create a public URL:
     ```bash
     ngrok http 5000
     ```

   - Update your Twilio webhook with the ngrok URL:
     ```
     https://your-ngrok-url/webhook
     ```

5. **Run the Application**

   Run the app locally:
   ```bash
   python stockbot.py
   ```

   The bot will start on `http://localhost:5000`, and messages sent to your Twilio WhatsApp number will trigger the bot’s responses.

## MongoDB Configuration

StockBot uses MongoDB to store transaction data. Make sure MongoDB is running and accessible from the environment where StockBot is deployed.

- **Database**: `stockbot_db`
- **Collection**: `transactions`

### MongoDB Connection String

The MongoDB connection string should be added to the `.env` file as shown above. Replace `your_mongodb_connection_string` with your actual MongoDB URI.

## Command List and Customization

StockBot supports the following commands:

- **Check Stock**: `how many units in stock`
- **Add Stock**: `add <number>`
- **Reduce Stock**: `reduce <number>`

You can modify these command phrases in the `stockbot.py` file by adjusting the regular expressions in the `webhook` function.

```python
# Example: Modify the Check Stock command
if re.search(r"\b(current stock)\b", user_message):
    # Rest of the code...
```

## Usage

Send the following messages to the bot:

1. **Check stock**: `How many units in stock?`
2. **Add stock**: `Add 10`
3. **Reduce stock**: `Reduce 5`

The bot will respond with messages indicating the stock levels or error messages if the command is unrecognized.

## Screenshots

Include screenshots here to show the WhatsApp conversation flow with StockBot. (The screenshots example was in a different language as the commands were set to be in Portuguese at the time.)

<img height="250" alt="Screenshot 2024-11-12 at 3 19 35 AM" src="https://github.com/user-attachments/assets/20b021e9-08bc-4b15-b572-6c8472d110da">
<img height="250" alt="Screenshot 2024-11-12 at 3 19 35 AM" src="https://github.com/user-attachments/assets/1c1931b3-64bb-40d4-ac3d-64144bd727f3">


## Deploying to AWS Lambda with Zappa

To deploy this app on AWS Lambda using [Zappa](https://github.com/Miserlou/Zappa), follow these steps:

1. Install Zappa:
   ```bash
   pip install zappa
   ```

2. Initialize Zappa:
   ```bash
   zappa init
   ```

3. Deploy to AWS:
   ```bash
   zappa deploy
   ```

Zappa will provide an API URL, which you can use as the webhook URL in Twilio.

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Please open a pull request with any improvements or suggestions.
