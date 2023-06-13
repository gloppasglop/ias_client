class Connection(object):
    
    def __init__(
            self,
            url=None,
            username=None,
            password=None,
            token=None,
            insecure=False,
            ca_file=None
            ) -> None:
        
        self._url = url
        self._username = username
        self._password = password
        self._token = token
        self._insecure = insecure
        self._ca_file = ca_file

        
        return


    def _get_access_token(self) -> str:

        print("TOKEN")
        return 'dsdsdsaasaadsadasdasdasd'

    def authenticate(self) -> str:

        try:
            if self._token is None:
                self._token = self._get_access_token()
            return self._token
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            raise
    
    def _send(self,query) -> object:
        
        self.authenticate()
        return {}
