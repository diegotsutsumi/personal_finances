from .token_store import TokenStore, TokenObject
from typing import Optional
import json
from ..file_helper import write_string
import logging
from .token_store import TokenNotFound


LOGGER = logging.getLogger(__name__)
TOKEN_PATH_PREFIX = "token"


class DiskTokenStore(TokenStore):
    def save_token(self, user_id: str, token: TokenObject) -> Optional[TokenObject]:
        previous_content = write_string(
            f"{TOKEN_PATH_PREFIX}/{user_id}.json", token.model_dump_json()
        )
        try:
            previous_token = TokenObject.model_validate_json(previous_content)
        except json.JSONDecodeError as e:
            LOGGER.warn("error decoding json from token: " + e.msg)
            previous_token = None

        return previous_token

    def get_last_token(self, user_id: str) -> TokenObject:
        try:
            with open(f"{TOKEN_PATH_PREFIX}/{user_id}.json", "r") as token_file:
                return TokenObject.model_validate_json(token_file.read())
        except Exception as e:
            raise TokenNotFound from e
