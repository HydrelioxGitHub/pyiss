from unittest import TestCase
from httmock import all_requests, HTTMock, response
import pyiss


class TestCurrent_location(TestCase):
    def setUp(self):
        """

        Instantiate the Http Request Mock, the ISS class call and the json response

        """

        #Json response
        self.json_current_location = {"timestamp": 1481410143, "message": "success", "iss_position": {"latitude": "6.8272", "longitude": "-160.2689"}}

        #HTTP Mock
        @all_requests
        def correct_response(url, request):
            headers = {'content-type': 'application/json',
                       'Set-Cookie': 'foo=bar;'}
            return response(200, self.json_current_location, headers, None, 5,
                            request)
        self.http_correct = correct_response

        @all_requests
        def wrong_response(url, request):
            headers = {'content-type': 'application/json',
                       'Set-Cookie': 'foo=bar;'}
            return response(403, self.json_current_location, headers, None, 5,
                            request)
        self.http_wrong = wrong_response

        self.iss = pyiss.ISS()

    def test_current_location_json_return(self):
        """

        Test that the function return the right dict answer

        """
        with HTTMock(self.http_correct):
            response = self.iss.current_location()
            location = {"latitude": "6.8272", "longitude": "-160.2689"}
            self.assertDictEqual(response, location)

    def test_current_location_error_server(self):
        """

        Test that the function raise an exception if the server response is not correct

        """
        with HTTMock(self.http_wrong):
            self.assertRaises(Exception, self.iss.current_location )
