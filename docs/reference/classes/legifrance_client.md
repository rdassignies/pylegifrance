# LegifranceClient

```python
class LegifranceClient:
    def __init__(config: Optional[ApiConfig] = None)
    def update_api_keys(self, legifrance_api_key=None, legifrance_api_secret=None)
    def call_api(self, route: str, data: str)
    def ping(self, route: str = "consult/ping")
    def get(self, route: str)
```

Gère l'authentification et les appels à l'API Legifrance.