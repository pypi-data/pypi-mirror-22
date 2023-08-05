# -*- coding: utf-8 -*-

"""
    raas_v2.http.requests_client

    This file was automatically generated for Tango Card, Inc. by APIMATIC v2.0 ( https://apimatic.io ).
"""

import requests

from cachecontrol import CacheControl
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from .http_client import HttpClient
from .http_response import HttpResponse
from .http_method_enum import HttpMethodEnum

class RequestsClient(HttpClient):

    """An implementation of HttpClient that uses Requests as its HTTP Client

    Attributes:
        timeout (int): The default timeout for all API requests.

    """

    def __init__(self, timeout=60, cache=False, max_retries=None, retry_interval=None):
        """The constructor.

        Args:
            timeout (float): The default global timeout(seconds).

        """
        self.timeout = timeout
        self.session = requests.session()

        if max_retries and retry_interval:
            retries = Retry(total=max_retries, backoff_factor=retry_interval)
            self.session.mount('http://', HTTPAdapter(max_retries=retries))
            self.session.mount('https://', HTTPAdapter(max_retries=retries))

        if cache:
            self.session = CacheControl(self.session)

    def execute_as_string(self, request):
        """Execute a given HttpRequest to get a string response back

        Args:
            request (HttpRequest): The given HttpRequest to execute.

        Returns:
            HttpResponse: The response of the HttpRequest.

        """
        response = self.session.request(HttpMethodEnum.to_string(request.http_method),
                                        request.query_url,
                                        headers=request.headers,
                                        params=request.query_parameters,
                                        data=request.parameters,
                                        files=request.files,
                                        timeout=self.timeout)

        return self.convert_response(response, False)

    def execute_as_binary(self, request):
        """Execute a given HttpRequest to get a binary response back

        Args:
            request (HttpRequest): The given HttpRequest to execute.

        Returns:
            HttpResponse: The response of the HttpRequest.

        """
        response = self.session.request(HttpMethodEnum.to_string(request.http_method),
                                        request.query_url,
                                        headers=request.headers,
                                        params=request.query_parameters,
                                        data=request.parameters,
                                        files=request.files,
                                        timeout=self.timeout)

        return self.convert_response(response, True)

    def convert_response(self, response, binary):
        """Converts the Response object of the HttpClient into an
        HttpResponse object.

        Args:
            response (dynamic): The original response object.

        Returns:
            HttpResponse: The converted HttpResponse object.

        """
        if binary:
            return HttpResponse(response.status_code, response.headers, response.content)
        else:
            return HttpResponse(response.status_code, response.headers, response.text)
