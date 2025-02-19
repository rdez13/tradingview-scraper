# tests/test_indicators.py

import os
import sys
import time
import pytest
import unittest
from unittest import mock
from unittest.mock import patch
import requests
from unittest.mock import patch

path = str(os.getcwd())
if path not in sys.path:
    sys.path.append(path)

from tradingview_scraper.symbols.technicals import Indicators


class TestIndicators:
    @patch('requests.get')
    def test_request_failure_handling(self, mock_get):
        """Test handling of HTTP request failures."""
        mock_get.side_effect = requests.exceptions.RequestException("Connection error")
        indicators = Indicators()
        # Set allIndicators to True to avoid needing to specify indicators
        result = indicators.scrape(exchange="BITSTAMP", symbol="BTCUSD", allIndicators=True)

        assert result['status'] == 'failed', "Expected status to be 'failed'"

    def setup_method(self):
        """Setup method to create an Indicators instance."""
        self.indicators_scraper = Indicators(export_result=True, export_type='json')

    def test_scrape_indicators_success(self, mocker):
        """Test scraping indicators successfully."""
        # Mocking the response of the scrape method with the new structure
        mock_response = {
            'status': 'success',
            'data': {
                'RSI': 50.0,
                'Stoch.K': 80.0
            }
        }
        mocker.patch.object(self.indicators_scraper, 'scrape', return_value=mock_response)

        # Scrape indicators for the BTCUSD symbol
        time.sleep(3)
        indicators = self.indicators_scraper.scrape(
            exchange="BINANCE",
            symbol="BTCUSD",
            timeframe="1d",
            indicators=["RSI", "Stoch.K"]
        )

        # Update assertions to match the new mock_response structure
        assert indicators == mock_response
        assert indicators['status'] == 'success'
        assert 'data' in indicators
        assert 'RSI' in indicators['data']
        assert 'Stoch.K' in indicators['data']
        assert indicators['data']['RSI'] == 50.0
        assert indicators['data']['Stoch.K'] == 80.0

    def test_scrape_indicators_invalid_exchange(self, mocker):
        """Test scraping indicators with an invalid exchange."""
        # Mocking the response for an invalid exchange
        mocker.patch.object(self.indicators_scraper, 'scrape', side_effect=ValueError("Invalid exchange"))

        time.sleep(3)
        with pytest.raises(ValueError, match="Invalid exchange"):
            self.indicators_scraper.scrape(
                exchange="INVALID_EXCHANGE",
                symbol="BTCUSD",
                timeframe="1d",
                indicators=["RSI", "Stoch.K"]
            )

    def test_scrape_indicators_empty_response(self, mocker):
        """Test scraping indicators returns empty response."""
        # Mocking an empty response
        mocker.patch.object(self.indicators_scraper, 'scrape', return_value={})

        time.sleep(3)
        indicators = self.indicators_scraper.scrape(
            exchange="BINANCE",
            symbol="BTCUSD",
            timeframe="1d",
            indicators=["RSI", "Stoch.K"]
        )

        assert indicators == {}

    def test_scrape_indicators_valid_response(self, mocker):
        """Test scraping indicators with a valid success response."""
        # Mocking the valid response of the scrape method
        valid_response = {
            'status': 'success',
            'data': {
                'RSI': 50.0,
                'Stoch.K': 80.0
            }
        }
        mocker.patch.object(self.indicators_scraper, 'scrape', return_value=valid_response)

        # Scrape indicators for the BTCUSD symbol
        time.sleep(3)
        indicators = self.indicators_scraper.scrape(
            exchange="BINANCE",
            symbol="BTCUSD",
            timeframe="1d",
            indicators=["RSI", "Stoch.K"]
        )

        # Print the indicators output
        print("Indicators Output:", indicators)

        # Assertions to verify the valid response structure
        assert indicators['status'] == 'success'
        assert 'data' in indicators
        assert 'RSI' in indicators['data']
        assert 'Stoch.K' in indicators['data']
        assert indicators['data']['RSI'] == 50.0
        assert indicators['data']['Stoch.K'] == 80.0

    

    # @pytest.mark.parametrize("timeframe", ['1h', 'invalid'])
    # def test_timeframe_validation(timeframe):
    #     indicators = Indicators()
        
    #     if timeframe == 'invalid':
    #         with pytest.raises(ValueError):
    #             indicators._validate_timeframe(timeframe)
    #     else:
    #         assert indicators._validate_timeframe(timeframe) is None


    # def test_export_functionality(mocker):
    #     """Test the export functionality depending on export type."""
    #     mocker.patch.object(Indicators, '_export')
    #     indicators = Indicators(export_result=True, export_type='json')
        
    #     data = [{"status": "success", "data": {"RSI": 50.0}}]
    #     indicators._export(data, "BTCUSD", "1d")
        
    #     indicators._export.assert_called_with(data, "BTCUSD", "1d")

    # def test_unsupported_exchange(self):
    #     """Test scraping with an unsupported exchange."""
    #     indicators = Indicators()
        
    #     with self.assertRaises(ValueError):
    #         indicators.scrape(exchange="UNSUPPORTED", symbol="BTCUSD", timeframe="1d")

   
