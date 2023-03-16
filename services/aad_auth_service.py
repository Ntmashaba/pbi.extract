import msal
from msal.exceptions import MsalServiceError
from msal import ConfidentialClientApplication

class AadAuthService:
    def __init__(self, **connection_args):
        self.auth_url: str = None
        self.tenant_id: str = None
        self.client_id: str = None
        self.client_secret: str = None
        self.scope_base: str = None
        self.username: str = None
        self.password: str = None

        for key, value in connection_args.items():
            setattr(self, key, value)

    def get_access_token(self) -> str:
        try:
            auth = self.auth_url.replace('common', self.tenant_id)
            app = ConfidentialClientApplication(
                self.client_id,
                client_credential=self.client_secret,
                authority=auth,
            )
            result = app.acquire_token_for_client(scopes=[self.scope_base])

            if "access_token" not in result:
                raise ValueError("Access token not found in response")

            return result["access_token"]
        except ValueError:
            raise
        except Exception as e:
            raise Exception(f"Failed to acquire access token: {e}")
