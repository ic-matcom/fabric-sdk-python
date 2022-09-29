from typing import List, Dict


def dict_get(_dict):
    def f(key, lambda_default):
        try:
            return _dict[key]
        except KeyError:
            return lambda_default()
    return f


class OrgConfig:
    def __init__(
        self,
        msp_id: str,
        admin_pk: Dict[str, str],
        signed_cert: Dict[str, str],
        peers: List[str] = [],
        ca_list: List[str] = []
    ) -> None:
        self.msp_id = msp_id
        self.admin_pk = admin_pk
        self.signed_cert = signed_cert
        self.peers = peers
        self.ca_list = ca_list

    @staticmethod
    def load(config):
        config_get = dict_get(config)
        return OrgConfig(
            msp_id=config_get('mspid', lambda: None),
            admin_pk=config_get('adminPrivateKey', lambda: {}),
            signed_cert=config_get('signedCert', lambda: {}),
            peers=config_get('peers', lambda: []),
            ca_list=config_get('certificateAuthorities', lambda: [])
        )


class MSPConfig:
    def __init__(
        self,
        name: str,
        url: str,
        http_options: Dict[str, str],
        tls_ca_certs: Dict[str, str],
        registrar: Dict[str, str],
    ) -> None:
        self.name = name
        self.url = url
        self.http_options = http_options
        self.tls_ca_certs = tls_ca_certs
        self.registrar = registrar

    @staticmethod
    def load(config, default_name):
        config_get = dict_get(config)
        return MSPConfig(
            name=config_get('caName', lambda: default_name),
            url=config_get('url', lambda: 'https://localhost:7054'),
            http_options=config_get('httpOptions', lambda: {}),
            tls_ca_certs=config_get('tlsCACerts', lambda: {}),
            registrar=config_get('registrar', lambda: {})
        )


class ClientConfig:
    def __init__(self,
                 organization: str,
                 connection: Dict[str, str],
                 credential_store: Dict[str, str],) -> None:
        self.organization = organization
        self.connection = connection
        self.credential_store = credential_store

    @staticmethod
    def load(config):
        config_get = dict_get(config)
        return ClientConfig(
            organization=config_get('organization', lambda: ''),
            connection=config_get('connection', lambda: {}),
            credential_store=config_get('credentialStore', lambda: {})
        )


class Network:
    def __init__(self, network_name: str) -> None:
        self.org_name = network_name
        self._dict_org = {}
        self._dict_ca = {}
        self.client = []


class ContextClient:
    def __init__(self, client, orgs, ca_list) -> None:
        self.client: ClientConfig = client
        self.orgs: OrgConfig = orgs
        self.ca_list: List[MSPConfig] = ca_list

# TODO: Doc Exception


class ConfigManager:
    def __init__(self) -> None:
        self.description_list = []
        self._networks = {}

    def _select_network(self, name=None) -> Network:
        if name is None:
            try:
                return self._networks['default']
            except KeyError:

                if len(self._networks) == 1:
                    return list(self._networks.values())[0]
                else:
                    raise Exception()
        else:
            try:
                return self._networks[name]
            except KeyError:
                raise Exception()

    def _select_client(self, network: Network, name=None) -> ClientConfig:
        if name is None:
            print(network.client)
            if len(network.client) == 1:
                return network.client[0]
            else:
                raise Exception()
        else:
            try:
                return [client for client in network.client if client.organization == name][0]
            except KeyError:
                raise Exception()

    def client_compile(self, client_name=None, network_name=None) -> ContextClient:
        network = self._select_network(network_name)
        client = self._select_client(network, name=client_name)

        try:
            org: OrgConfig = network._dict_org[client.organization]
        except KeyError:
            raise Exception()

        ca_list = []

        for ca in org.ca_list:
            try:
                ca_list.append(network._dict_ca[ca])
            except KeyError:
                pass

        return ContextClient(client, org, ca_list)

    def add_new_config(self, path, config):
        self.description_list.append((path, config))

        try:
            name = config['name']
        except KeyError:
            name = 'default'

        try:
            network = self._networks[name]
        except KeyError:
            self._networks[name] = Network(name)
            network = self._networks[name]

        self.__find_org_config(config, network)
        self.__find_ca_config(config, network)
        self.__find_client_config(config, network)

    def __find_org_config(self, config, network: Network):
        try:
            data = config['organizations']
        except KeyError:
            return

        for org_name, org_config in data.items():
            try:
                _ = network._dict_org[org_name]
            except KeyError:
                network._dict_org[org_name] = OrgConfig.load(config)

    def __find_ca_config(self, config, network: Network):
        try:
            data = config['certificateAuthorities']
        except KeyError:
            return

        for ca_name, ca_config in data.items():
            try:
                _ = network._dict_ca[ca_name]
            except KeyError:
                network._dict_ca[ca_name] = MSPConfig.load(
                    ca_config, default_name=ca_name)

    def __find_client_config(self, config, network: Network):
        try:
            data = config['client']
        except KeyError:
            return

        network.client.append(ClientConfig.load(data))
