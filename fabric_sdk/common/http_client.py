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

    @staticmethod
    def build_http_data(
        self, data: dict,
        predicate=lambda key, value: not value in [None, '']
    ):
        result = {}
        for key, value in data.items():
            if predicate(key, value):
                result[key] = value

        return result


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
    def __init__(self, data={}) -> None:
        self.data = data

    def __setattr__(self, __name: str, __value) -> None:
        if not __value in [None, '']:
            self.data[__name] = __value

        return self
