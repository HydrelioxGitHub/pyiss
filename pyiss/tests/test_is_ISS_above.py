from unittest import TestCase
from httmock import all_requests, HTTMock, response
import pyiss


class TestIs_ISS_above(TestCase):
    def setUp(self):
        """

        Instantiate the Http Request Mock, the ISS class call and the json response

        """

        # Json response
        self.json_is_ISS_above_false = {
            "message": "success",
            "request": {
                "altitude": 100,
                "datetime": 1481418788,
                "latitude": 15.0,
                "longitude": 20.0,
                "passes": 5
            },
            "response": [
                {
                    "duration": 348,
                    "risetime": 1481448840
                },
                {
                    "duration": 634,
                    "risetime": 1481454465
                }
            ]
        }

        self.json_is_ISS_above_true = {
            "message": "success",
            "request": {
                "altitude": 100,
                "datetime": 1481418788,
                "latitude": 15.0,
                "longitude": 20.0,
                "passes": 5
            },
            "response": [
                {
                    "duration": 348,
                    "risetime": 1481448840
                }
            ]
        }

        # HTTP Mock
        @all_requests
        def true_response(url, request):
            headers = {'content-type': 'application/json',
                       'Set-Cookie': 'foo=bar;'}
            return response(200, self.json_is_ISS_above_true, headers, None, 5,
                            request)

        self.http_true = true_response

        @all_requests
        def false_response(url, request):
            headers = {'content-type': 'application/json',
                       'Set-Cookie': 'foo=bar;'}
            return response(200, self.json_is_ISS_above_false, headers, None,
                            5,
                            request)

        self.http_false = false_response

        @all_requests
        def wrong_response(url, request):
            headers = {'content-type': 'application/json',
                       'Set-Cookie': 'foo=bar;'}
            return response(403, self.json_is_ISS_above, headers, None, 5,
                            request)

        self.http_wrong = wrong_response

        self.iss = pyiss.ISS()

    def test_is_ISS_above_true(self):
        """

        Test that json match a true answer

        """
        with HTTMock(self.http_true):
            response = self.iss.is_ISS_above(20, 15)

            self.assertTrue(response)

    def test_is_ISS_above_false(self):
        """

        Test that json match a false answer

        """
        with HTTMock(self.http_false):
            response = self.iss.is_ISS_above(20, 15)

            self.assertFalse(response)

    def test_is_ISS_above_error_server(self):
        """

        Test that the function raise an exception if the server response is not correct

        """
        with HTTMock(self.http_wrong):
            self.assertRaises(Exception, self.iss.is_ISS_above, 15, 20)

    def test_is_ISS_above_input_bound(self):
        """

        Test that input raise exception using voluptuous
        Each set of data test a boundary

        """
        with HTTMock(self.http_true):
            data = [[-80.1, 1, 1], [80.1, 1, 1], [1, -180.1, 1],
                    [1, 180.1, 1], [1, 1, -1], [1, 1, 10000.1]]
            for value in data:
                self.assertRaises(Exception, self.iss.is_ISS_above, value[0],
                                  value[1], value[2])

            data = [[-80, 1, 1], [80, 1, 1], [1, -180, 1],
                    [1, 180, 1], [1, 1, 0], [1, 1, 10000]]
            for value in data:
                self.assertTrue(self.iss.is_ISS_above(value[0],
                                                      value[1], value[2]))
