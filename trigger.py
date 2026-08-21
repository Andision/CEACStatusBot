import json
import os
import subprocess

from dotenv import load_dotenv

from CEACStatusBot import (
    BarkNotificationHandle,
    EmailNotificationHandle,
    NotificationManager,
    TelegramNotificationHandle,
)

# --- Load .env if present, else fallback to system env ---
if os.path.exists(".env"):
    load_dotenv(dotenv_path=".env")  # loads into os.environ
else:
    print(".env not found, using system environment only")


def download_artifact():
    try:
        result = subprocess.run(
            ["gh", "api", f"repos/{os.environ['GITHUB_REPOSITORY']}/actions/artifacts"],
            capture_output=True,
            text=True,
        )
        artifacts = json.loads(result.stdout)
        artifact_exists = any(artifact["name"] == "status-artifact" for artifact in artifacts["artifacts"])

        if artifact_exists:
            subprocess.run(["gh", "run", "download", "--name", "status-artifact"], check=True)
        else:
            with open("status_record.json", "w") as file:
                json.dump({"statuses": []}, file)
    except Exception as e:
        print(f"Error downloading artifact: {e}")


# --- Read env vars with fallback ---
GH_TOKEN = os.getenv("GH_TOKEN")
if not GH_TOKEN:
    print("GH_TOKEN not found")

if not os.path.exists("status_record.json"):
    download_artifact()

try:
    LOCATION = os.environ["LOCATION"]
    NUMBER = os.environ["NUMBER"]
    PASSPORT_NUMBER = os.environ["PASSPORT_NUMBER"]
    SURNAME = os.environ["SURNAME"]
    notificationManager = NotificationManager(LOCATION, NUMBER, PASSPORT_NUMBER, SURNAME)
except KeyError as e:
    raise RuntimeError(f"Missing required env var: {e}") from e


# --- Optional: Email notifications ---
FROM = os.getenv("FROM")
TO = os.getenv("TO")
PASSWORD = os.getenv("PASSWORD")
SMTP = os.getenv("SMTP", "")

if FROM and TO and PASSWORD:
    emailNotificationHandle = EmailNotificationHandle(FROM, TO, PASSWORD, SMTP)
    notificationManager.addHandle(emailNotificationHandle)
else:
    print("Email notification config missing or incomplete")


# --- Optional: Telegram notifications ---
BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
CHAT_ID = os.getenv("TG_CHAT_ID")

if BOT_TOKEN and CHAT_ID:
    tgNotif = TelegramNotificationHandle(BOT_TOKEN, CHAT_ID)
    notificationManager.addHandle(tgNotif)
else:
    print("Telegram bot notification config missing or incomplete")


# --- Optional: Bark notifications ---
BARK_DEVICE_KEY = os.getenv("BARK_DEVICE_KEY")
BARK_SERVER = os.getenv("BARK_SERVER") or "https://api.day.app"
BARK_GROUP = os.getenv("BARK_GROUP") or "CEACStatusBot"
BARK_SOUND = os.getenv("BARK_SOUND")

if BARK_DEVICE_KEY:
    bark_notification = BarkNotificationHandle(
        BARK_DEVICE_KEY,
        BARK_SERVER,
        BARK_GROUP,
        BARK_SOUND,
    )
    notificationManager.addHandle(bark_notification)
else:
    print("Bark notification config missing or incomplete")


# --- Send notifications ---
notificationManager.send()
