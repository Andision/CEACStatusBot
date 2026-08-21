import requests

from .handle import NotificationHandle

DEFAULT_BARK_SERVER = "https://api.day.app"
DEFAULT_BARK_GROUP = "CEACStatusBot"
CEAC_STATUS_URL = "https://ceac.state.gov/CEACStatTracker/Status.aspx?App=NIV"
BARK_SUCCESS_CODE = 200


class BarkNotificationHandle(NotificationHandle):
    def __init__(
        self,
        device_key: str,
        server_url: str = DEFAULT_BARK_SERVER,
        group: str = DEFAULT_BARK_GROUP,
        sound: str | None = None,
    ) -> None:
        super().__init__()
        if not device_key.strip():
            error_message = "Bark device key must not be empty"
            raise ValueError(error_message)

        normalized_server_url = server_url.strip().rstrip("/") or DEFAULT_BARK_SERVER
        self.__device_key = device_key.strip()
        self.__api_url = f"{normalized_server_url}/push"
        self.__group = group.strip() or DEFAULT_BARK_GROUP
        self.__sound = sound.strip() if sound else None

    def send(self, result: dict) -> None:
        title = f"[CEACStatusBot] {result['application_num_origin']}: {result['status']}"
        body_parts = [
            f"Visa type: {result.get('visa_type', 'Unknown')}",
            f"Case created: {result.get('case_created', 'Unknown')}",
            f"Last updated: {result.get('case_last_updated', 'Unknown')}",
        ]
        if description := result.get("description"):
            body_parts.extend(("", description))

        payload = {
            "device_key": self.__device_key,
            "title": title,
            "body": "\n".join(body_parts),
            "group": self.__group,
            "url": CEAC_STATUS_URL,
        }
        if self.__sound:
            payload["sound"] = self.__sound

        response = requests.post(self.__api_url, json=payload, timeout=15)
        response.raise_for_status()

        response_data = response.json()
        if response_data.get("code") != BARK_SUCCESS_CODE:
            message = response_data.get("message", "unknown Bark API error")
            error_message = f"Failed to send Bark notification: {message}"
            raise RuntimeError(error_message)

        print("Bark notification sent successfully")
