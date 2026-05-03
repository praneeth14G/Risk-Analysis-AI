# services/memory_service.py
# Stores and retrieves data using Momento cache
import json
import time
from datetime import timedelta

from momento import CacheClient, Configurations, CredentialProvider
from momento.responses import CacheGet

from utils.config import MOMENTO_API_KEY, MOMENTO_CACHE_NAME

def get_client():
    """Create and return a Momento cache client."""
    return CacheClient(
        configuration=Configurations.Laptop.latest(),
        credential_provider=CredentialProvider.from_api_key_v2(
            MOMENTO_API_KEY,
            "api.cache.cell-ap-south-1-1.prod.a.momentohq.com"
        ),
        default_ttl=timedelta(hours=24)
    )


def save_risk_record(username, risk_data):
    """
    Save a risk record for a user.
    Key format: risk:{username}:{timestamp}
    """
    client = get_client()

    key = f"risk:{username}:{int(time.time())}"
    value = json.dumps(risk_data)

    client.set(MOMENTO_CACHE_NAME, key, value)

    return key


def get_risk_history(username):
    """
    Retrieve all risk records for a user.
    We store a list of keys for each user.
    """
    client = get_client()

    keys_key = f"keys:{username}"
    response = client.get(MOMENTO_CACHE_NAME, keys_key)

    if isinstance(response, CacheGet.Hit):
        keys = json.loads(response.value_string)

        records = []

        for key in keys:
            r = client.get(MOMENTO_CACHE_NAME, key)

            if isinstance(r, CacheGet.Hit):
                records.append(
                    json.loads(r.value_string)
                )

        return records

    return []


def save_key_for_user(username, key):
    """Track all keys belonging to a user so we can list history."""
    client = get_client()

    keys_key = f"keys:{username}"

    response = client.get(MOMENTO_CACHE_NAME, keys_key)

    if isinstance(response, CacheGet.Hit):
        keys = json.loads(response.value_string)
    else:
        keys = []

    keys.append(key)

    client.set(
        MOMENTO_CACHE_NAME,
        keys_key,
        json.dumps(keys)
    )