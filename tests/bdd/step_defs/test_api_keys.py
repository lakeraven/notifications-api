"""Step definitions for API keys BDD tests."""

import json
import uuid

from pytest_bdd import given, parsers, scenarios, then, when

from app.constants import KEY_TYPE_NORMAL, KEY_TYPE_TEAM, KEY_TYPE_TEST
from tests.app.db import (
    create_api_key,
    create_service,
    create_template,
    create_user,
)

scenarios("../features/services/api_keys.feature")


# -- Given steps --


@given(parsers.parse("the service has {count:d} API keys"), target_fixture="api_keys")
def the_service_has_n_api_keys(service, count):
    keys = []
    for i in range(count):
        keys.append(create_api_key(service, key_type=KEY_TYPE_NORMAL, key_name=f"Key {i+1}"))
    return keys


@given("the service has an API key", target_fixture="api_key")
def the_service_has_an_api_key(service):
    return create_api_key(service, key_type=KEY_TYPE_NORMAL, key_name="Test API Key")


@given("the service has a revoked API key", target_fixture="api_key")
def the_service_has_a_revoked_api_key(service, admin_client):
    api_key = create_api_key(service, key_type=KEY_TYPE_NORMAL, key_name="Revoked Key")
    admin_client.post(
        f"/service/{service.id}/api-key/revoke/{api_key.id}",
    )
    return api_key


# -- When steps --


_KEY_TYPE_MAP = {
    "normal": KEY_TYPE_NORMAL,
    "test": KEY_TYPE_TEST,
    "team": KEY_TYPE_TEAM,
}


@when(
    parsers.parse('I create an API key named "{name}" of type "{key_type}"'),
    target_fixture="api_response",
)
def create_api_key_via_api(admin_client, service, name, key_type):
    resp = admin_client.post(
        f"/service/{service.id}/api-key",
        data={
            "name": name,
            "created_by": str(service.created_by.id),
            "key_type": _KEY_TYPE_MAP.get(key_type, key_type),
        },
    )
    return {"status_code": resp.status_code, "json": resp.json}


@when("I list API keys for the service", target_fixture="api_response")
def list_api_keys(admin_client, service):
    resp = admin_client.get(f"/service/{service.id}/api-keys")
    return {"status_code": resp.status_code, "json": resp.json}


@when("I get the API key by ID", target_fixture="api_response")
def get_api_key_by_id(admin_client, service, api_key):
    resp = admin_client.get(f"/service/{service.id}/api-keys/{api_key.id}")
    return {"status_code": resp.status_code, "json": resp.json}


@when("I revoke the API key", target_fixture="api_response")
def revoke_api_key(admin_client, service, api_key):
    resp = admin_client.post(
        f"/service/{service.id}/api-key/revoke/{api_key.id}",
    )
    return {"status_code": resp.status_code, "json": resp.json}


@when("I try to send a notification using the revoked key", target_fixture="api_response")
def send_with_revoked_key(service, api_key, service_api_client):
    template = create_template(service=service)
    service_api_client.set_service(service.id)
    resp = service_api_client.post(
        "/v2/notifications/sms",
        data={
            "phone_number": "+447700900855",
            "template_id": str(template.id),
        },
    )
    return {"status_code": resp.status_code, "json": resp.json}


# -- Then steps --


@then("the response should contain the API key secret")
def response_has_api_key_secret(api_response):
    data = api_response["json"]["data"]
    # The create endpoint returns {"data": "<unsigned_secret>"} — a non-empty string
    assert data is not None
    assert isinstance(data, str)
    assert len(data) > 0


@then(parsers.parse("the response should contain {count:d} API keys"))
def response_has_n_api_keys(api_response, count):
    api_keys = api_response["json"]["apiKeys"]
    assert isinstance(api_keys, list)
    # The service may have additional default keys; check at least count
    assert len(api_keys) >= count, f"Expected at least {count} API keys, got {len(api_keys)}"


@then("the response should contain the key name")
def response_has_key_name(api_response):
    api_keys = api_response["json"]["apiKeys"]
    assert isinstance(api_keys, list)
    assert len(api_keys) >= 1
    assert "name" in api_keys[0]


@then("the API key should be expired")
def api_key_is_expired(admin_client, service, api_key):
    # The GET-by-ID endpoint filters out expired keys (returns 404), so we use
    # the list endpoint which includes recently-expired keys (within 7 days).
    resp = admin_client.get(f"/service/{service.id}/api-keys")
    data = resp.json
    assert resp.status_code == 200, f"GET api keys failed with {resp.status_code}: {data}"
    keys = data["apiKeys"]
    revoked = [k for k in keys if k["id"] == str(api_key.id)]
    assert len(revoked) == 1, f"Revoked key not found in list. Keys: {keys}"
    assert revoked[0]["expiry_date"] is not None, f"Key not expired: {revoked[0]}"
