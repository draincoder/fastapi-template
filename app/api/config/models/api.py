from dataclasses import dataclass


@dataclass
class ApiConfig:
    host: str
    port: int
    debug: bool


@dataclass
class AuthConfig:
    secret_key: str
    token_expire_minutes: int = 30
