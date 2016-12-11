from unittest import TestCase
from httmock import all_requests, HTTMock, response
import pyiss


class TestPeople_in_space(TestCase):
    def setUp(self):
        """

        Instantiate the Http Request Mock, the ISS class call and the json response

        """

        #Json response
        self.json_people_in_space = {
            "people": [{"craft": "ISS", "name": "Sergey Rizhikov"},
                       {"craft": "ISS", "name": "Andrey Borisenko"},
                       {"craft": "ISS", "name": "Shane Kimbrough"},
                       {"craft": "ISS", "name": "Oleg Novitskiy"},
                       {"craft": "ISS", "name": "Thomas Pesquet"},
                       {"craft": "ISS", "name": "Peggy Whitson"}],
            "message": "success", "number": 6}

        #HTTP Mock
        @all_requests
        def correct_response(url, request):
            headers = {'content-type': 'application/json',
                       'Set-Cookie': 'foo=bar;'}
            return response(200, self.json_people_in_space, headers, None, 5,
                            request)
        self.http_correct = correct_response

        @all_requests
        def wrong_response(url, request):
            headers = {'content-type': 'application/json',
                       'Set-Cookie': 'foo=bar;'}
            return response(403, self.json_people_in_space, headers, None, 5,
                            request)
        self.http_wrong = wrong_response

        self.iss = pyiss.ISS()

    def test_people_in_space_json_return(self):
        """

        Test that the function return the right json answer

        """
        with HTTMock(self.http_correct):
            response = self.iss.people_in_space()
            self.assertDictEqual(response, self.json_people_in_space)

    def test_people_in_space_error_server(self):
        """

        Test that the function raise an exception if the server response is not correct

        """
        with HTTMock(self.http_wrong):
            self.assertRaises(Exception, self.iss.people_in_space)