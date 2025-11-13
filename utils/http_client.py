"""
Cliente HTTP con gestión de reintentos y timeouts
"""
import requests
from typing import Optional, Dict, Any
import time


class HTTPClient:
    """Cliente HTTP mejorado con reintentos automáticos"""
    
    def __init__(self, timeout: int = 10, max_retries: int = 3):
        self.timeout = timeout
        self.max_retries = max_retries
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'OrquestadorHackingWeb/1.0'
        })
    
    def get(self, url: str, params: Optional[Dict] = None, **kwargs) -> Optional[requests.Response]:
        """Realizar petición GET con reintentos"""
        return self._request('GET', url, params=params, **kwargs)
    
    def post(self, url: str, data: Optional[Dict] = None, **kwargs) -> Optional[requests.Response]:
        """Realizar petición POST con reintentos"""
        return self._request('POST', url, data=data, **kwargs)
    
    def _request(self, method: str, url: str, **kwargs) -> Optional[requests.Response]:
        """Realizar petición HTTP con reintentos automáticos"""
        kwargs.setdefault('timeout', self.timeout)
        kwargs.setdefault('allow_redirects', True)
        
        for attempt in range(self.max_retries):
            try:
                response = self.session.request(method, url, **kwargs)
                return response
            except requests.exceptions.Timeout:
                if attempt == self.max_retries - 1:
                    return None
                time.sleep(1)
            except requests.exceptions.ConnectionError:
                if attempt == self.max_retries - 1:
                    return None
                time.sleep(1)
            except Exception:
                return None
        
        return None
    
    def close(self):
        """Cerrar la sesión HTTP"""
        self.session.close()
