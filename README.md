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
STORE_WEBHOOKS_TO_DATABASE=false
```

Replace `your_bot_token_here` with the token you received from BotFather.

**Note**: `STORE_WEBHOOKS_TO_DATABASE` is optional and defaults to `false`. Set it to `true` only for development purposes or if you're curious about the raw data your Dream Machine router sends. When enabled, all webhook payloads will be stored in the MongoDB database.

### Step 3: Start the Service

Run the following command in the project directory:

```bash
docker-compose up -d
```

This will:
- Build the Docker image
- Start the Dreamcatcher service on port `8080`
- Start a MongoDB database container for storing muted notifications

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
- `/mute` - Mute a specific notification (reply to a notification message to mute it)
- `/clear` - Clear all muted notifications and reset the mute list

---

## 🏗️ Architecture

```
UniFi Dream Machine Pro
        ↓
   Alarm Manager (Webhook)
        ↓
   Dreamcatcher API (FastAPI)
        ↓
   Telegram Bot ←→ MongoDB Database
        ↓
   Your Telegram Chat
```

Dreamcatcher runs multiple services:
1. **FastAPI Server**: Receives webhooks from UDM on `/webhook`
2. **Telegram Bot**: Listens for commands and sends notifications
3. **MongoDB Database**: Stores muted notifications and optionally webhook payloads

### Notification Muting

You can mute specific notifications to prevent spam from recurring events. When you reply to a notification with `/mute`, that specific notification will be silenced, and you won't receive further alerts for the same event. Use `/clear` to reset all muted notifications when needed. This is particularly useful when you trust a device and its recurring activity, or when you want to reduce notification noise.

---

## 🐳 Docker Compose Services

- **backend**: The Dreamcatcher FastAPI application (port 8080)
- **mongodb**: MongoDB database for storing muted notifications and webhook data (port 27017)

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

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `TELEGRAM_BOT_TOKEN` | Your Telegram bot token from BotFather | ✅ Yes | - |
| `STORE_WEBHOOKS_TO_DATABASE` | Store complete webhook payloads in database (for development/debugging) | ❌ No | `false` |

**Recommendation**: Keep `STORE_WEBHOOKS_TO_DATABASE` set to `false` in production. Only enable it for development purposes or if you want to inspect the raw data your Dream Machine router sends.

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
  "app": "network",
  "customContent": null,
  "deviceEventClassId": "400",
  "message": "Device Name connected to WiFi Network on Access Point Name. Connection Info: Ch. 100 (5 GHz, 80 MHz), -81 dBm. IP: 10.x.x.x",
  "name": "WiFi Client Connected",
  "parameters": {
    "UNIFIcategory": "Monitoring",
    "UNIFIsubCategory": "WiFi",
    "UNIFIhost": "Dream Machine",
    "UNIFIconnectedToDeviceName": "Access Point Name",
    "UNIFIconnectedToDeviceIp": "192.168.x.x",
    "UNIFIconnectedToDeviceMac": "xx:xx:xx:xx:xx:xx",
    "UNIFIconnectedToDeviceModel": "U6-Lite",
    "UNIFIconnectedToDeviceVersion": "6.7.17",
    "UNIFIclientAlias": "Device Name",
    "UNIFIclientHostname": "hostname",
    "UNIFIclientIp": "10.x.x.x",
    "UNIFIclientMac": "xx:xx:xx:xx:xx:xx",
    "UNIFIwifiChannel": "100",
    "UNIFIwifiChannelWidth": "80",
    "UNIFIwifiName": "WiFi Network",
    "UNIFIwifiBand": "na",
    "UNIFIauthMethod": "wpapsk",
    "UNIFIWiFiRssi": "-81",
    "UNIFInetworkName": "LAN",
    "UNIFInetworkSubnet": "10.x.x.x/24",
    "UNIFInetworkVlan": "10",
    "UNIFIutcTime": "2025-12-02T19:31:59.847Z"
  },
  "severity": 1,
  "version": "9.5.21",
  "alarm_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
}
```

**Note**: The actual webhook payload from UniFi contains extensive metadata, timestamps, device information, and technical details as shown above. However, **Dreamcatcher focuses on simplicity and robustness** by extracting only the essential information (the `message` field) and forwarding it to Telegram. This approach prevents information overload and keeps notifications clean and actionable for the end user.

If you enable `STORE_WEBHOOKS_TO_DATABASE=true` in your `.env` file, the complete payload will be stored in MongoDB for development or debugging purposes.

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
