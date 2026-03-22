"""Step definitions for API key features."""

import uuid

from pytest_bdd import given, parsers, scenarios, then, when

from app.enums import KeyType
from tests.app.db import create_api_key

scenarios("../features/services/api_keys.feature")


# -- Given steps --


@given(
    parsers.parse('the service has a "{key_type}" API key'),
    target_fixture="api_key",
)
def service_has_api_key(notify_db_session, service, key_type):
    key_type_enum = KeyType(key_type)
    return create_api_key(service, key_type=key_type_enum)


# -- When steps --


@when(
    parsers.parse('a "{key_type}" API key is created for the service'),
    target_fixture="api_response",
)
def create_api_key_for_service(admin_client, service, key_type, api_response):
    data = {
        "name": f"test-{key_type}-key-{uuid.uuid4()}",
        "key_type": key_type,
        "created_by": str(service.users[0].id),
    }
    resp = admin_client.post(f"/service/{service.id}/api-key", data=data)
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


@when("all API keys are retrieved for the service", target_fixture="api_response")
def get_all_api_keys(admin_client, service, api_response):
    resp = admin_client.get(f"/service/{service.id}/api-keys")
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


@when("the API key is retrieved by ID", target_fixture="api_response")
def get_api_key_by_id(admin_client, service, api_key, api_response):
    resp = admin_client.get(f"/service/{service.id}/api-keys/{api_key.id}")
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


@when("the API key is revoked", target_fixture="api_response")
def revoke_api_key(admin_client, service, api_key, api_response):
    resp = admin_client.post(
        f"/service/{service.id}/api-key/revoke/{api_key.id}",
    )
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json() if resp.data else None
    return api_response


@when("the revoked API key is used to access the service", target_fixture="api_response")
def use_revoked_key(service_api_client, service, api_key, api_response):
    service_api_client.set_service(str(service.id))
    resp = service_api_client.get(f"/v2/notifications", key_type="normal")
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json() if resp.data else None
    return api_response


# -- Then steps --


@then("the response should contain the API key data")
def response_has_api_key(api_response):
    data = api_response["json"]["data"]
    assert "id" in data or isinstance(data, str)


@then("the response should contain a list of API keys")
def response_has_api_keys_list(api_response):
    data = api_response["json"]["apiKeys"]
    assert isinstance(data, list)
    assert len(data) > 0
