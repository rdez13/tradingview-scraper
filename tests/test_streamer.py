import unittest
from unittest import mock
from tradingview_scraper.symbols.stream.streamer import Streamer

class TestStreamer(unittest.TestCase):

    @mock.patch('tradingview_scraper.symbols.stream.streamer.StreamHandler')
    def test_stream_initialization(self, MockStreamHandler):
        """Test initialization of Streamer class."""
        streamer = Streamer(export_result=True, export_type='json')
        self.assertTrue(streamer.export_result)
        self.assertEqual(streamer.export_type, 'json')
        MockStreamHandler.assert_called_once()

    @mock.patch('tradingview_scraper.symbols.stream.streamer.Streamer.get_data')
    def test_stream_data_handling(self, mock_get_data):
        """Test data handling from WebSocket."""
        mock_get_data.return_value = iter([{"p": [{"i": "123", "v": [1,2,3,4,5,6]}]}])
        streamer = Streamer()
        data = next(streamer.get_data())
        self.assertIn("p", data)

    @mock.patch.object(Streamer, 'get_data')
    def test_stream_timeout_handling(self, mock_get_data):
        """Test handling of timeouts in data streaming."""
        mock_get_data.side_effect = TimeoutError("Timed out")
        streamer = Streamer()
        
        with self.assertRaises(TimeoutError):
            _ = next(streamer.get_data())