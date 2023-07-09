import jwt
from datetime import datetime, timezone, timedelta
class Connection(object):
    
    def __init__(
            self,
            url=None,
            username=None,
            password=None,
            tokens=None,
            insecure=False,
            ca_file=None
            ) -> None:

        self._url = url
        self._username = username
        self._password = password
        self._tokens = tokens
        self._insecure = insecure
        self._ca_file = ca_file


        return


    def _get_tokens(self) -> dict:

        access_token = jwt.encode({"exp": datetime.now(tz=timezone.utc)+timedelta(days=2),'payload': "TUTU"}, "secret")
        refresh_token = jwt.encode({"exp": datetime.now(tz=timezone.utc)+timedelta(days=10),'payload': "TATA"}, "secret")

        return {'access_token': access_token,'refresh_token': refresh_token}

    def authenticate(self) -> dict:

        print("AUTH")
        try:
            if self._tokens is None or self._tokens['access_token'] is None:
                self._tokens = self._get_tokens()
            else:
                # Check if token has expired
                decoded_access=jwt.decode(self._tokens["access_token"], options={"verify_signature": False})
                decoded_refresh=jwt.decode(self._tokens["refresh_token"], options={"verify_signature": False})
                if ( decoded_access["exp"] < datetime.now().timestamp() ):
                    print("EXPIRED")
                    self._tokens = self._get_tokens()
                else:
                    print("VALID")

            return self._tokens
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            raise

    def _send(self,query) -> object:

        self.authenticate()
        return {}
