# heath_check.pyのテスト
# 実際のURLへのリクエストは行わずに、`requests.get()`をモックしてテスト。
# メール送信のテストも行わず、`send_mail()`をテストから除外します。

import unittest
import requests
from unittest.mock import patch
from src.health_check import health_check

class TestHealthCheck(unittest.TestCase):
    # ステータスコードが200の場合、OKが返ることを確認します。
    @patch('requests.get')
    def test_health_check_ok(self, mock_get):
        mock_get.return_value.status_code = 200
        result = health_check('https://example.com')
        self.assertEqual(result, 'OK')

    # ステータスコードが200以外の場合、ステータスコードが200ではありません。が返ることを確認します。
    @patch('requests.get')
    def test_health_check_status_code_not_200(self, mock_get):
        mock_get.return_value.status_code = 404
        result = health_check('https://example.com')
        self.assertEqual(result, 'ステータスコードが200ではありません。')

    # リクエストが失敗した場合、リクエストが失敗しました。が返ることを確認します。
    @patch('requests.get')
    def test_health_check_request_exception(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException()
        result = health_check('https://example.com')
        self.assertEqual(result, 'リクエストが失敗しました。')

if __name__ == '__main__':
    unittest.main()
