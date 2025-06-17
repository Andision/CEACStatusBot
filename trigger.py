import os
import subprocess
import json
from CEACStatusBot import NotificationManager, EmailNotificationHandle, TelegramNotificationHandle

def download_artifact():
    try:
        # Check if the artifact exists
        result = subprocess.run(
            ['gh', 'api', f'repos/{os.environ["GITHUB_REPOSITORY"]}/actions/artifacts'],
            capture_output=True,
            text=True
        )
        artifacts = json.loads(result.stdout)
        artifact_exists = any(artifact['name'] == 'status-artifact' for artifact in artifacts['artifacts'])

        if artifact_exists:
            # Download the artifact
            subprocess.run(
                ['gh', 'run', 'download', '--name', 'status-artifact'],
                check=True
            )
        else:
            # Create an empty JSON file if the artifact doesn't exist
            with open('status_record.json', 'w') as file:
                json.dump({'statuses': []}, file)
    except Exception as e:
        print(f"Error downloading artifact: {e}")


try:
    GH_TOKEN = os.environ["GH_TOKEN"]
except KeyError:
    print("GH_TOKEN not found")

if not os.path.exists('status_record.json'):
    download_artifact()

try:
    LOCATION = os.environ["LOCATION"]
    NUMBER = os.environ["NUMBER"]
    PASSPORT_NUMBER = os.environ["PASSPORT_NUMBER"]
    SURNAME = os.environ["SURNAME"]
    notificationManager = NotificationManager(LOCATION, NUMBER, PASSPORT_NUMBER, SURNAME)
except KeyError:
    print("LOCATION or NUMBER Error")

try:
    FROM = os.environ["FROM"]
    TO = os.environ["TO"]
    PASSWORD = os.environ["PASSWORD"]
    SMTP = os.environ.get("SMTP", "")
    if FROM and TO and PASSWORD:
        emailNotificationHandle = EmailNotificationHandle(FROM, TO, PASSWORD, SMTP)
        notificationManager.addHandle(emailNotificationHandle)
except KeyError:
    print("Email notification config error")

try:
    BOT_TOKEN = os.environ["TG_BOT_TOKEN"]
    CHAT_ID = os.environ["TG_CHAT_ID"]
    if BOT_TOKEN and CHAT_ID:
        tgNotif = TelegramNotificationHandle(BOT_TOKEN, CHAT_ID)
        notificationManager.addHandle(tgNotif)
except KeyError:
    print("Telegram bot notification config error")

notificationManager.send()
