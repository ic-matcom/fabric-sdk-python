class Context:
    def __init__(self, description) -> None:
        self.all_description = description

        self.doc_msp_configs()

    def doc_msp_configs(self):
        try:
            certificateAuthorities = self.all_description['certificateAuthorities']
        except KeyError:
            return

        self.certificateAuthorities = [
            MSPConfigDoc(value) for value in certificateAuthorities.values()
        ]

    def __str__(self) -> str:

        result = "SDK Context:\n\n"

        try:
            msp_text = ""
            for msp in self.certificateAuthorities:
                msp_text += str(msp) + '\n'

            result += '\tCertificateAuthorities:\n' + msp_text
        except AttributeError:
            pass

        return result


class MSPConfigDoc:
    def __init__(self, dic_config) -> None:
        self.name = dic_config['caName']
        self.url = dic_config['url']

    def __str__(self) -> str:
        return f'\t\t- {self.name}: {self.url}'
