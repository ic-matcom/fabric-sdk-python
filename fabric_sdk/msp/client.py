from typing import Tuple
from fabric_sdk.context import ContextClient
from fabric_sdk.common import HttpClient, HttpProtocol, Ecies, Crypto, HttpDynamicBody
from fabric_sdk.common.crypto_tools import decode_csr
import base64


class CAClient:
    def __init__(
        self,
        context: ContextClient,
        ca_name: str = None,
        http_client: HttpProtocol = HttpClient,
        crypto_algorithm: Crypto = None
    ) -> None:
        """Init new ca's client by context and maybe a ca's name  

        :param context: context with network config 
        :type context: ContextClient

        :param ca_name: name of specific ca. Context can has 
                        more that one ca  
        :type ca_name: str

        :param http_client: Http client to communicate with server 
        :type http_client: HttpProtocol 
        """

        self.http_client = http_client
        self._crypto = Ecies() if crypto_algorithm is None else crypto_algorithm

        try:
            if ca_name is None:
                self.__ca_config = context.ca_list[0]
            else:
                self.__ca_config = [
                    ca for ca in context.ca_list if ca.name == ca_name][0].url
        except IndexError:
            raise Exception()

    def __path(self, path):
        return self.__ca_config.url + path

    def enroll(self, enrollment_id, enrollment_secret, csr=None, profile='', attr_reqs=None) -> Tuple[bytes, bytes]:
        """Enroll a registered user in order to receive a signed X509
         certificate

        :param enrollment_id: The registered ID to use for enrollment
        :type enrollment_id: str

        :param enrollment_secret: The secret associated with the
                                     enrollment ID
        :type enrollment_secret: str

        :param profile: The profile name.  Specify the 'tls' profile for a
             TLS certificate; otherwise, an enrollment certificate is issued. (Default value = '')
        :type profile: str

        :param csr: Optional. PEM-encoded PKCS#10 Certificate Signing
             Request. The message sent from client side to Fabric-ca for the
              digital identity certificate. (Default value = None)
        :type csr: str

        :param attr_reqs: An array of AttributeRequest
        :type attr_reqs: list

        :return: PEM-encoded X509 certificate (Default value = None)
        :raises RequestException: errors in requests.exceptions
        :raises ValueError: Failed response, json parse error, args missing
        """

        if not enrollment_id or not enrollment_secret:
            raise ValueError(
                "Missing required parameters,'enrollmentID' and 'enrollmentSecret are required.")

        if attr_reqs:
            if not isinstance(attr_reqs, list):
                raise ValueError(
                    "attr_reqs must be an array of AttributeRequest objects")
            for attr in attr_reqs:
                if not attr['name']:
                    raise ValueError(
                        "attr_reqs object is missing the name of the attribute")

        private_key = None
        if not csr:
            private_key = self._crypto.generate_private_key()
            csr = self._crypto.generate_csr(private_key, enrollment_id)
            csr = decode_csr(csr)

        req = HttpDynamicBody()
        req.certificate_request = csr
        req.caname = self.__ca_config.name
        req.profile = profile
        req.attr_reqs = attr_reqs

        res, st = self.http_client.post(
            path=self.__path('enroll'),
            json=req.data,
            auth=(enrollment_id, enrollment_secret),
            ** self.__ca_config.http_options
        )

        if res['success']:
            return base64.b64decode(res['result']['Cert']), \
                base64.b64decode(res['result']['ServerInfo']['CAChain'])
        else:
            raise ValueError("Enrollment failed with errors {0}"
                             .format(res['errors']))
