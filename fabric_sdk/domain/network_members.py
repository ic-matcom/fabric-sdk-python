from enum import Enum
from typing import Optional


class NetworkMember:
    """
    All member in Hyperledger Fabric Network(HFN) must have an id and some role.
    That member can specify their password or secret, or set it when they will enroll.   
    That member is affiliated with any organization, if not specified then it will be 
    the same as the organization of the registering member. 
    """

    def __init__(self, enrollment_id: str, role: str, affiliation: str = None,  enrollment_secret: str = None) -> None:
        """
        :param enrollment_id: The registered ID to use for enrollment
        :type enrollment_id: str

        :param enrollment_secret: The secret associated with the
                                     enrollment ID
        :type enrollment_secret: str

        :param role: Optional type of role for this user.
                        When not including, use a null for this parameter.
        :type role: str
        :param affiliation: Affiliation with which this user will be
             associated
        :type affiliation: str
        """

        self.enrollment_id = enrollment_id
        self.enrollment_secret = enrollment_secret
        self.role = role
        self.affiliation = affiliation


class EnrolledMember(NetworkMember):
    """
    EnrolledMember is a CA-certified member of the network , so
    this member can communicate with all member of the HFN and uses
    all the functions of the network  
    """

    def __init__(
        self,
        enrollment_id: str,
        enrollment_secret: str,
        role: str,
        affiliation: str,
        enrollment_cert: str,
        ca_cert_chain: bytes,
        private_key: bytes = None,
    ) -> None:
        """
        :param enrollment_id: The registered ID to use for enrollment
        :type enrollment_id: str

        :param enrollment_secret: The secret associated with the
                                     enrollment ID
        :type enrollment_secret: str

        :param role: Optional type of role for this user.
                        When not including, use a null for this parameter.
        :type role: str
        :param affiliation: Affiliation with which this user will be
             associated
        :type affiliation: str

        :param enrollment_cert: PEM-encoded X509 certificate (Default value = None)
        :type enrollment_cert: bytes
        """

        super().__init__(enrollment_id, enrollment_secret, role, affiliation)

        self.enrollment_cert = enrollment_cert
        self.ca_cert_chain = ca_cert_chain
        self.private_key = private_key

    def reenroll(
        self,
        enrollmentCert: str,
        caCertChain: str,
        private_key: str = None
    ) -> 'EnrolledMember':

        return EnrolledMember(
            enrollmentCert=enrollmentCert,
            caCertChain=caCertChain,
            private_key=private_key,
            ** self.__dict__
        )


class UnenrolledMember(NetworkMember):
    """
    Unenrolled member is a registered member, but in this moment 
    he not enroll yet. This member can request a certificate from 
    the CA, but he can't uses the rest of the network functions    
    """

    def __init__(
        self,
        enrollment_id: str,
        enrollment_secret: str,
        role: str,
        affiliation: str,
        csr: str = None

    ) -> None:
        """
        :param enrollment_id: The registered ID to use for enrollment
        :type enrollment_id: str

        :param enrollment_secret: The secret associated with the
                                     enrollment ID
        :type enrollment_secret: str

        :param role: Optional type of role for this user.
                        When not including, use a null for this parameter.
        :type role: str
        :param affiliation: Affiliation with which this user will be
             associated
        :type affiliation: str

        :param csr: Optional. PEM-encoded PKCS#10 Certificate Signing
             Request. The message sent from client side to Fabric-ca for the
              digital identity certificate. (Default value = None)
        :type csr: str
        """

        super().__init__(enrollment_id, enrollment_secret, role, affiliation)

        self.csr = csr

    def enroll(
        self,
        enrollmentCert: str,
        caCertChain: str,
        private_key: str = None
    ) -> EnrolledMember:

        return EnrolledMember(
            enrollmentCert=enrollmentCert,
            caCertChain=caCertChain,
            private_key=private_key,
            ** self.__dict__
        )


class UnregisteredMember(NetworkMember):
    """
    The lowest status of an HFN member is that of an unregistered member.
    That member will attempt to join the network. This member is unable 
    to apply to the CA for a certificate.   
    """

    def registry(self, secret) -> UnenrolledMember:
        return UnenrolledMember(
            secret=secret,
            **self.__dict__
        )


class User(UnregisteredMember):
    def __init__(self, enrollment_id: str, enrollment_secret: str, affiliation: str) -> None:
        super().__init__(enrollment_id, enrollment_secret, 'client', affiliation)


class Admin(UnregisteredMember):
    def __init__(self, enrollment_id: str, enrollment_secret: str, affiliation: str) -> None:
        super().__init__(enrollment_id, enrollment_secret, 'admin', affiliation)


class Organization(UnregisteredMember):
    def __init__(self, name, enrollment_id: str, enrollment_secret: str) -> None:
        super().__init__(enrollment_id, enrollment_secret, 'org', name)


class Peer(UnregisteredMember):
    def __init__(self, enrollment_id: str, enrollment_secret: str, affiliation: str) -> None:
        super().__init__(enrollment_id, enrollment_secret, 'peer', affiliation)


class RevokeReason(Enum):
    """
    See https://godoc.org/golang.org/x/crypto/ocsp for valid values
    """

    UNSPECIFIED = (1, 'unspecified')
    KEY_COMPROMISE = (2, 'keycompromise')
    CA_COMPROMISE = (3, 'cacompromise')
    AFFILIATION_CHANGE = (4, 'affiliationchange')
    SUPERSEDED = (5, 'superseded')
    CESSATION_OF_OPERATION = (6, 'cessationofoperation')
    CERTIFICATE_HOLD = (7, 'certificatehold')
    REVOKE_FROM_CLR = (8, 'removefromcrl')
    PRIVILEGE_WITH_DRAW = (9, 'privilegewithdrawn')
    AACOMPROMISE = (10, 'aacompromise')


class RevokeRequest:
    """
    Request to revoke an existing certificate (enrollment certificate or
    transaction certificate), or revoke all certificates issued to an
    enrollment id. If revoking a particular certificate, then both the
    Authority Key Identifier and serial number are required. If
    revoking by enrollment id, then all future requests to enroll this
    id will be rejected.
    """

    def __init__(
        self,
        reason: RevokeReason,
        enrollment_id: Optional[str] = None,
        aki: Optional[str] = None,
        serial: Optional[str] = None,
        gen_crl: bool = False
    ) -> None:
        """
        :param enrollment_id: enrollmentID ID to revoke
        :type enrollment_id: Optional[str]

        :param aki: Authority Key Identifier string, hex encoded, for the
             specific certificate to revoke
        :type aki: Optional[str]

        :param serial: Serial number string, hex encoded, for the specific
             certificate to revoke
        :type serial: Optional[str]

        :param reason: The reason for revocation.
        :type reason: RevokeReason

        :param gen_crl: GenCRL specifies whether to generate a CRL
        :type gen_crl: bool

        :raises RequestException: errors in requests.exceptions
        :raises ValueError: Failed response, json parse error, args missing
        """

        self.reason = reason
        self.enrollment_id = enrollment_id
        self.aki = aki
        self.serial = serial
        self.gen_crl = gen_crl
