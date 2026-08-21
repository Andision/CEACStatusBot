import unittest

from CEACStatusBot.request.query import _normalize_application_num


class NormalizeApplicationNumberTest(unittest.TestCase):
    def test_ignores_spacing_hyphens_and_case(self) -> None:
        self.assertEqual(
            _normalize_application_num(" aa00-20 akax "),
            _normalize_application_num("AA0020AKAX"),
        )

    def test_keeps_distinct_application_numbers_distinct(self) -> None:
        self.assertNotEqual(
            _normalize_application_num("AA0020AKAX"),
            _normalize_application_num("AA0020AKAY"),
        )


if __name__ == "__main__":
    unittest.main()
