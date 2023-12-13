import requests
import json
import html
from .handle import NotificationHandle

class TelegramNotificationHandle(NotificationHandle):
    def __init__(self, bot_token: str, chat_id: str) -> None:
        super().__init__()
        self.__bot_token = bot_token
        self.__chat_id = chat_id
        self.__api_url = f"https://api.telegram.org/bot{self.__bot_token}/sendMessage"

    def send(self, result):
        # {'success': True, 'visa_type': 'NONIMMIGRANT VISA APPLICATION', 'status': 'Issued', 'case_created': '30-Aug-2022', 'case_last_updated': '19-Oct-2022', 'description': 'Your visa is in final processing. If you have not received it in more than 10 working days, please see the webpage for contact information of the embassy or consulate where you submitted your application.', 'application_num': '***'}

        message_title = f"[CEACStatusBot] {result['application_num_origin']}: {result['status']}"
        message_content = html.escape(json.dumps(result, indent=2))

        # Construct the message text with the title in bold
        message_text = f"<b>{message_title}</b>\n\n<pre>{message_content}</pre>"

        # Send the message using the Telegram Bot API
        response = requests.post(self.__api_url, data={
            "chat_id": self.__chat_id,
            "text": message_text,
            "parse_mode": "HTML"
        })

        # Check the response
        if response.status_code == 200:
            print("Message sent successfully")
        else:
            print(f"Failed to send message: {response.text}")