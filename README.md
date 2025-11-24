# 🌙 Dreamcatcher

**A simple, lightweight service that bridges UniFi Dream Machine alarms to Telegram notifications.**

Dreamcatcher is a straightforward solution that solves a simple problem: **UniFi Dream Machine Pro doesn't have native Telegram integration**. This service acts as a bridge, receiving webhook notifications from your UDM's Alarm Manager and forwarding them directly to your Telegram bot.

Stay up-to-date with everything happening in your network - from security alerts to connection events - all delivered instantly to your Telegram chat.

---

## ✨ Why Dreamcatcher?

- **No Native Integration**: UniFi doesn't support Telegram notifications out of the box
- **Real-time Updates**: Receive network alerts instantly on Telegram
- **Simple Setup**: Just a webhook endpoint and a Telegram bot token
- **Lightweight**: Minimal resource usage with FastAPI and Docker
- **Stay Informed**: Know exactly what's happening on your network, anytime, anywhere

---

## 🧪 Tested Environment

This service has been tested with:
- **UniFi OS**: UDM Pro 4.4.6 (Release Channel: Official)
- **Network Application**: 9.5.21

However, it will **most likely work with other versions** as well, since the webhook interface is relatively stable.

---

## 🚀 Quick Start

### Prerequisites

1. **UniFi Dream Machine Pro** (or compatible device)
2. **Docker** and **Docker Compose** installed
3. **Telegram Account** to create a bot

### Step 1: Create a Telegram Bot

1. Open Telegram and search for [@BotFather](https://t.me/botfather)
2. Send `/newbot` and follow the instructions
3. Choose a name and username for your bot
4. Copy the **Bot Token** you receive (it looks like `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### Step 2: Configure Environment Variables

Create a `.env` file in the project root directory:

```bash
TELEGRAM_BOT_TOKEN=your_bot_token_here
```

Replace `your_bot_token_here` with the token you received from BotFather.

### Step 3: Start the Service

Run the following command in the project directory:

```bash
docker-compose up -d
```

This will:
- Build the Docker image
- Start the Dreamcatcher service on port `8080`
- Start a MongoDB database for future features

### Step 4: Configure UniFi Alarm Manager

1. Open your **UniFi Dream Machine Pro** web interface
2. Navigate to **Settings** → **System** → **Notifications** → **Alarm Manager**
3. Create or edit an alarm
4. Under **Action**, select **Webhook**
5. Choose **Custom Webhook**
6. Configure the webhook:
   - **URL**: `http://<your-dreamcatcher-ip>:8080/webhook`
   - **Delivery Method**: `POST`
   - **Content Type**: `Default Content`
7. Save the alarm

Replace `<your-dreamcatcher-ip>` with the IP address where Dreamcatcher is running (e.g., `192.168.1.100:8080`).

### Step 5: Activate the Bot

1. Open Telegram and find your bot
2. Send `/start` to activate monitoring
3. You'll receive a confirmation message

That's it! Your network alarms will now be forwarded to Telegram.

---

## 📋 Bot Commands

- `/start` - Start receiving notifications
- `/stop` - Stop receiving notifications

---

## 🏗️ Architecture

```
UniFi Dream Machine Pro
        ↓
   Alarm Manager (Webhook)
        ↓
   Dreamcatcher API (FastAPI)
        ↓
   Telegram Bot
        ↓
   Your Telegram Chat
```

Dreamcatcher runs two parallel services:
1. **FastAPI Server**: Receives webhooks from UDM on `/webhook`
2. **Telegram Bot**: Listens for commands and sends notifications

---

## 🐳 Docker Compose Services

- **backend**: The Dreamcatcher FastAPI application (port 8080)
- **database**: MongoDB for future data persistence

---

## 📂 Project Structure

```
dreamcatcher/
├── app/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   └── utilities/
│       ├── bot.py           # Telegram bot logic
│       └── logger.py        # Logging configuration
├── docker-compose.yml       # Docker Compose configuration
├── Dockerfile              # Docker image definition
├── .env                    # Environment variables (create this!)
└── README.md               # This file
```

---

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `TELEGRAM_BOT_TOKEN` | Your Telegram bot token from BotFather | ✅ Yes |

### MongoDB (Optional)

The MongoDB service is included for future features. Current functionality doesn't require it, but it's ready for data persistence if needed.

---

## 🛠️ Development

To run in development mode with live reload:

```bash
cd app
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8080
```

---

## 📝 Example Webhook Payload

When an alarm triggers, UDM sends a POST request to `/webhook` with JSON data:

```json
{
  "message": "Intrusion detected on device XX:XX:XX:XX:XX:XX"
}
```

Dreamcatcher extracts the message and forwards it to your Telegram chat.

---

## 🔐 Security Notes

- Keep your `.env` file secure and never commit it to version control
- Consider using a reverse proxy with HTTPS in production
- Restrict webhook access to your UDM's IP address using firewall rules

---

## 🤝 Contributing

This is a simple project, but contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

---

## 📜 License

This project is open source and available for personal and commercial use.

---

## 💡 Use Cases

- **Security Alerts**: Get notified immediately when intrusion attempts occur
- **Device Connections**: Know when devices join or leave your network
- **Network Events**: Stay informed about system events and anomalies
- **Remote Monitoring**: Check on your network even when you're away

---

**Made with ☕ for the UniFi community**
