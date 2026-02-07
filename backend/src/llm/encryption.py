"""Encrypt/decrypt user API keys for storage."""

import base64
import hashlib
import logging

from cryptography.fernet import Fernet, InvalidToken

from src.config import settings

logger = logging.getLogger(__name__)

# Fernet keys are 44 chars, base64url alphabet
_B64URL_CHARS = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_")


def _normalize_fernet_key(key: str) -> str:
    """
    Produce a valid Fernet key from env. Accepts:
    - 64-char hex string -> 32 bytes, base64url-encoded.
    - 44-char base64url string -> use as-is (standard Fernet key).
    - Any other string -> SHA256(secret) -> 32 bytes -> base64url (e.g. 63-char hex or password).
    """
    key = key.strip().strip("'\"")
    if not key:
        return key
    # 64 hex chars -> exact 32-byte key
    hex_chars = "0123456789abcdefABCDEF"
    hex_only = "".join(c for c in key if c in hex_chars)
    if len(hex_only) == 64:
        try:
            key_bytes = bytes.fromhex(hex_only)
            return base64.urlsafe_b64encode(key_bytes).decode()
        except ValueError:
            pass
    # 44-char base64url -> assume standard Fernet key
    if len(key) == 44 and all(c in _B64URL_CHARS for c in key):
        return key
    # Any other secret: derive 32 bytes with SHA256
    return base64.urlsafe_b64encode(hashlib.sha256(key.encode()).digest()).decode()


def _get_fernet() -> Fernet | None:
    key = (settings.llm_config_encryption_key or "").strip()
    if not key:
        return None
    try:
        normalized = _normalize_fernet_key(key)
        return Fernet(normalized.encode())
    except Exception as e:
        logger.warning("LLM config encryption key invalid: %s", e)
        return None


def encrypt_api_key(plain: str) -> str | None:
    """Encrypt a plain API key for storage. Returns None if encryption not configured."""
    f = _get_fernet()
    if not f:
        return None
    return f.encrypt(plain.encode()).decode()


def decrypt_api_key(encrypted: str) -> str | None:
    """Decrypt a stored API key. Returns None if decryption fails or not configured."""
    f = _get_fernet()
    if not f:
        return None
    try:
        return f.decrypt(encrypted.encode()).decode()
    except InvalidToken:
        return None
