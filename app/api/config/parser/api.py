from __future__ import annotations

from app.api.config.models.api import AuthConfig, ApiConfig


def load_auth_config(dct: dict) -> AuthConfig:
    return AuthConfig(
        secret_key=dct["secret-key"],
        token_expire_minutes=dct["token-expire-minutes"]
    )


def load_api_config(dct: dict) -> ApiConfig:
    return ApiConfig(
        host=dct['host'],
        port=dct['port'],
        debug=dct['debug']
    )
