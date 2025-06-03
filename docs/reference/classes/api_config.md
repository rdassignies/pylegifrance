# ApiConfig

```python
class ApiConfig:
    def __init__(
        client_id: str,
        client_secret: str,
        token_url: str = "...",
        api_url: str = "...",
        connect_timeout: float = 3.05,
        read_timeout: float = 27.0,
    )

    @classmethod
    def from_env() -> "ApiConfig"
```

Gère la configuration d'accès à l'API (identifiants, URLs, timeouts).