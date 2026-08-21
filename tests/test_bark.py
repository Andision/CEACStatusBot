import unittest
from unittest.mock import Mock, patch

from CEACStatusBot.notification.bark import CEAC_STATUS_URL, BarkNotificationHandle


class BarkNotificationHandleTest(unittest.TestCase):
    def setUp(self) -> None:
        self.result = {
            "application_num_origin": "AA00123456",
            "status": "Issued",
            "visa_type": "NONIMMIGRANT VISA APPLICATION",
            "case_created": "20-Aug-2026",
            "case_last_updated": "21-Aug-2026",
            "description": "Your visa is in final processing.",
        }

    @patch("CEACStatusBot.notification.bark.requests.post")
    def test_send_uses_v2_json_api(self, post: Mock) -> None:
        response = post.return_value
        response.json.return_value = {"code": 200, "message": "success"}

        notification = BarkNotificationHandle(
            "device-key",
            "https://bark.example.com/",
            "Visa",
            "minuet",
        )
        notification.send(self.result)

        post.assert_called_once_with(
            "https://bark.example.com/push",
            json={
                "device_key": "device-key",
                "title": "[CEACStatusBot] AA00123456: Issued",
                "body": (
                    "Visa type: NONIMMIGRANT VISA APPLICATION\n"
                    "Case created: 20-Aug-2026\n"
                    "Last updated: 21-Aug-2026\n\n"
                    "Your visa is in final processing."
                ),
                "group": "Visa",
                "url": CEAC_STATUS_URL,
                "sound": "minuet",
            },
            timeout=15,
        )
        response.raise_for_status.assert_called_once_with()

    @patch("CEACStatusBot.notification.bark.requests.post")
    def test_send_raises_for_bark_api_error(self, post: Mock) -> None:
        post.return_value.json.return_value = {"code": 400, "message": "invalid device key"}
        notification = BarkNotificationHandle("device-key")

        with self.assertRaisesRegex(RuntimeError, "invalid device key"):
            notification.send(self.result)

    def test_empty_device_key_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "must not be empty"):
            BarkNotificationHandle("  ")


if __name__ == "__main__":
    unittest.main()
