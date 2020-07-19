import logging
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from django.conf import settings
from .exceptions import *

logger = logging.getLogger("maya_logger")


class ApiHttpClient:
    """
    Base class for http client which will handle internal working of http request
    such retry,session etc.
    """

    def __init__(
        self,
        retries=3,
        backoff_factor=0.3,
        timeout=10,
        status_forcelist=None,
        session=None,
        **kwargs,
    ):
        """
        params:
        retries: no of retries in case of failure, 
        backoff_factor: sleep configuration for retrying, 
        status_forcelist: status list to be considered for retrying, 
        session: requests session object
        """

        if status_forcelist is None:
            status_forcelist = (502, 504)

        self.base_url = settings.MAYA_SETTINGS["BASE_URL"]

        session = session or requests.Session()
        self.timeout = timeout

        retry = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist,
        )

        adapter = HTTPAdapter(max_retries=retry)
        session.auth = (
            settings.MAYA_SETTINGS["CLIENT_ID"],
            settings.MAYA_SETTINGS["CLIENT_SECRET"],
        )
        session.mount(self.base_url, adapter)
        self.session = session
        self.session.headers.update({"content-type": "application/json"})


class MayaApiClient(ApiHttpClient):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _build_url(self, path):
        return self.base_url + path

    def _post(self, url, data):

        try:
            res = self.session.post(url, data=data, timeout=self.timeout)
            return res

        except requests.exceptions.ConnectionError as e:
            raise ApiConnectionErrorException(
                f"Connection error for url {self.base_url}"
            )

        except requests.exceptions.Timeout as e:
            raise ApiTimeoutException(f"Timeout error for url {self.base_url}")

        except Exception as e:
            logger.error("api error", exc_info=True)
            raise ResponseException(f"Response Exception for url {self.base_url}")

    def _get(self, url, params=None):

        if params is None:
            params = dict()

        try:
            res = self.session.get(url, params=params, timeout=self.timeout)
            return res

        except requests.exceptions.ConnectionError as e:
            raise ApiConnectionErrorException(f"Connection error for url {url}")

        except requests.exceptions.Timeout as e:
            raise ApiTimeoutException(f"Timeout error for url {url}")

        except Exception as e:
            logger.error("api error", exc_info=True)
            raise ResponseException(f"Response Exception for url {url}")

    def get_movie_list(self, page=None):

        """
        params:
        page : interger to get specified page number data
        return:json
        """
        params = dict()
        if page is not None:
            params["page"] = page
        response = self._get(self._build_url("movies/"), params=params)
        return response.json()
