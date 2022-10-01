from typing import Protocol
import requests


class HttpProtocol(Protocol):
    def post(path, **param):
        """Send a post request to the ca service

        :param path: sub path after the base_url
        :param **param: post request params
        :return: the response body in json
        """
        pass

    def get(path, **param):
        """Send a get request to the ca service

        :param path: sub path after the base_url
        :param **param: get request params
        :return: the response body in json
        """
        pass

    def delete(path, **param):
        """Send a delete request to the ca service

        :param path: sub path after the base_url
        :param **param: delete request params
        :return: the response body in json
        """
        pass

    def update(path, **param):
        """Send a update request to the ca service

        :param path: sub path after the base_url
        :param **param: update request params
        :return: the response body in json
        """
        pass


class HttpClient:

    @staticmethod
    def post(path, **param):
        """Send a post request to the ca service

        :param path: sub path after the base_url
        :param **param: post request params
        :return: the response body in json
        """
        r = requests.post(url=path, **param)
        return r.json(), r.status_code

    @staticmethod
    def get(path, **param):
        """Send a get request to the ca service

        :param path: sub path after the base_url
        :param **param: get request params
        :return: the response body in json
        """
        r = requests.get(url=path, **param)
        return r.json(), r.status_code

    @staticmethod
    def delete(path, **param):
        """Send a delete request to the ca service

        :param path: sub path after the base_url
        :param **param: delete request params
        :return: the response body in json
        """
        r = requests.delete(url=path, **param)
        return r.json(), r.status_code

    @staticmethod
    def update(path, **param):
        """Send a update request to the ca service

        :param path: sub path after the base_url
        :param **param: update request params
        :return: the response body in json
        """
        r = requests.put(url=path, **param)
        return r.json(), r.status_code


class HttpDynamicBody:
    def __init__(self) -> None:
        self.data = {}

    def __setattr__(self, __name: str, __value) -> None:
        if not __value in [None, '']:
            self.data[__name] = __value

        return self
