from typing import Any, Dict, List
from datetime import datetime, timedelta

from aiohttp import ClientSession

from .product import HOLIDAYS_MODE, AldesProduct

class Oauth2Token:

    def __init__(self, scope: str, token_type: str, access_token: str, expires_in: int, refresh_token: str):
        self.scope         = scope
        self.token_type    = token_type
        self.access_token  = access_token
        self.expires_in    = expires_in
        self.refresh_token = refresh_token

class AldesApi:

    _BASE_URL                 = 'https://aldesiotsuite-aldeswebapi.azurewebsites.net'
    _GRANT_TYPE               = 'grant_type'
    _USERNAME_KEY             = 'username'
    _PASSWORD_KEY             = 'password'
    _AUTHORIZATION_HEADER_KEY = 'Authorization'
    _API_UTC_FORMAT           = '%Y%m%d%H%M%SZ' 

    _token: Oauth2Token = None

    def __init__(self, session: ClientSession, username: str, password: str) -> None:
        self._session  = session
        self._username = username
        self._password = password

    async def close(self):
        await self._session.close()
    
    async def authenticate(self) -> None:
        data: Dict = {
            self._GRANT_TYPE   : self._PASSWORD_KEY,
            self._USERNAME_KEY : self._username,
            self._PASSWORD_KEY : self._password
        }

        async with self._session.post(f'{self._BASE_URL}/oauth2/token', data = data) as response:            
            json = await response.json()
            if response.status == 200:
                self._token = Oauth2Token(**json)
            else:
                raise AuthenticationException()
    
    async def get_products(self) -> List[AldesProduct]:
        if not self._token:
            return []
        
        headers: Dict = {
            self._AUTHORIZATION_HEADER_KEY : f'{self._token.token_type} {self._token.access_token}'
        }
        
        async with self._session.get(f'{self._BASE_URL}/aldesoc/v5/users/me/products', headers = headers) as response:
            json = await response.json()
            if response.status == 200:
                return [AldesProduct(self, product['modem'], product['reference'], self._extract_product_mode(product)) for product in json]
            else:
                return []
    
    async def get_product_data(self, product_id: str) -> Dict[str, Any]:
        if not self._token:
            return {}
        
        headers: Dict = {
            self._AUTHORIZATION_HEADER_KEY : f'{self._token.token_type} {self._token.access_token}'
        }
        
        async with self._session.get(f'{self._BASE_URL}/aldesoc/v5/users/me/products/{product_id}', headers = headers) as response:
            json = await response.json()
            return {'mode': self._extract_product_mode(json)} if response.status == 200 else {}
    
    async def request_set_mode(self, product_id: str, mode: str) -> None:
        if not self._token:
            return

        headers: Dict = {
            self._AUTHORIZATION_HEADER_KEY : f'{self._token.token_type} {self._token.access_token}'
        }

        body: Dict = {
            'id'      : 1,
            'jsonrpc' : '2.0',
            'method'  : 'changeMode',
            'params'  : self._build_mode(mode)
        }

        async with self._session.post(f'{self._BASE_URL}/aldesoc/v5/users/me/products/{product_id}/commands', headers = headers, json = body) as response:
            response.raise_for_status()
    
    def _extract_product_mode(self, product: Any) -> str:
        return list(filter(lambda indicator: indicator['type'] == 'MODE', product['indicators']))[0]['value']
    
    def _build_mode(self, mode: str) -> List[str]:
        if mode == HOLIDAYS_MODE:
            return self._build_holidays_mode(mode)

        return [mode]
    
    def _build_holidays_mode(self, mode: str) -> List[str]:
        utc_now = datetime.utcnow()
        start_utc = utc_now - timedelta(minutes = 10)
        end_utc = utc_now + timedelta(days = 365 * 20)
        return [mode, start_utc.strftime(self._API_UTC_FORMAT), end_utc.strftime(self._API_UTC_FORMAT)]

class AuthenticationException(Exception):
    pass
