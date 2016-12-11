from unittest import TestCase
from httmock import all_requests, HTTMock, response
import pyiss


class TestPass_times(TestCase):
    def setUp(self):
        """

        Instantiate the Http Request Mock, the ISS class call and the json response

        """

        # Json response
        self.json_pass_times = {
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
                },
                {
                    "duration": 220,
                    "risetime": 1481460482
                },
                {
                    "duration": 224,
                    "risetime": 1481484335
                },
                {
                    "duration": 640,
                    "risetime": 1481489937
                }
            ]
        }

        self.location = self.json_pass_times['response']

        #HTTP Mock
        @all_requests
        def correct_response(url, request):
            headers = {'content-type': 'application/json',
                       'Set-Cookie': 'foo=bar;'}
            return response(200, self.json_pass_times, headers, None, 5,
                            request)
        self.http_correct = correct_response

        @all_requests
        def wrong_response(url, request):
            headers = {'content-type': 'application/json',
                       'Set-Cookie': 'foo=bar;'}
            return response(403, self.json_pass_times, headers, None, 5,
                            request)
        self.http_wrong = wrong_response

        self.iss = pyiss.ISS()

    def test_pass_times_json_return(self):
        """

        Test that the function return the right list answer

        """
        with HTTMock(self.http_correct):
            response = self.iss.pass_times(20, 15)

            self.assertListEqual(self.location, response)

    def test_pass_times_error_server(self):
        """

        Test that the function raise an exception if the server response is not correct

        """
        with HTTMock(self.http_wrong):
            self.assertRaises(Exception, self.iss.pass_times, 15,20)


    def test_pass_times_input_bound(self):
        """

        Test that input raise exception using voluptuous
        Each set of data test a boundary

        """
        with HTTMock(self.http_correct):
            data = [[-80.1, 1, 1, 1], [80.1, 1, 1, 1], [1, -180.1, 1, 1],
                    [1, 180.1, 1, 1], [1, 1, -1, 1], [1, 1, 10000.1, 1],
                    [1, 1, 1, 0], [1, 1, 1, 101], [1, 1, 1, 5.1]]
            for value in data:
                self.assertRaises(Exception, self.iss.pass_times, value[0],
                                  value[1], value[2], value[3])

            data = [[-80, 1, 1, 1], [80, 1, 1, 1], [1, -180, 1, 1],
                    [1, 180, 1, 1], [1, 1, 0, 1], [1, 1, 10000, 1],
                    [1, 1, 1, 1], [1, 1, 1, 100]]
            for value in data:
                self.assertListEqual(self.location,
                                     self.iss.pass_times(value[0],
                                                         value[1], value[2],
                                                         value[3]))
