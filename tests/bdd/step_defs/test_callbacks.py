"""Step definitions for service callbacks BDD tests."""

import json
import uuid

from pytest_bdd import given, parsers, scenarios, then, when

from app.enums import CallbackType
from tests.app.db import create_service, create_service_callback_api, create_user

scenarios("../features/services/callbacks.feature")


# -- Given steps --


@given("the service has a delivery receipt callback", target_fixture="callback")
def the_service_has_delivery_callback(service):
    return create_service_callback_api(
        callback_type=CallbackType.DELIVERY_STATUS,
        service=service,
        url="https://example.com/delivery",
        bearer_token="super_secret_token_1234",
    )


@given("the service has an inbound SMS callback", target_fixture="callback")
def the_service_has_inbound_callback(service):
    from app.models import ServiceInboundApi
    from app.dao.service_inbound_api_dao import save_service_inbound_api

    inbound_api = ServiceInboundApi(
        service_id=service.id,
        url="https://example.com/inbound",
        bearer_token="super_secret_token_1234",
        updated_by_id=service.users[0].id,
    )
    save_service_inbound_api(inbound_api)
    return inbound_api


# -- When steps --


@when(
    parsers.parse('I create a delivery receipt callback with URL "{url}"'),
    target_fixture="api_response",
)
def create_delivery_callback(admin_client, service, url):
    resp = admin_client.post(
        f"/service/{service.id}/delivery-receipt-api",
        data={
            "url": url,
            "bearer_token": "new_secret_token_1234",
            "updated_by_id": str(service.users[0].id),
        },
    )
    return {"status_code": resp.status_code, "json": resp.json}


@when("I get the delivery receipt callback", target_fixture="api_response")
def get_delivery_callback(admin_client, service, callback):
    resp = admin_client.get(
        f"/service/{service.id}/delivery-receipt-api/{callback.id}",
    )
    return {"status_code": resp.status_code, "json": resp.json}


@when(
    parsers.parse('I update the callback URL to "{url}"'),
    target_fixture="api_response",
)
def update_delivery_callback(admin_client, service, callback, url):
    resp = admin_client.post(
        f"/service/{service.id}/delivery-receipt-api/{callback.id}",
        data={
            "url": url,
            "bearer_token": "updated_secret_token_1234",
            "updated_by_id": str(service.users[0].id),
        },
    )
    return {"status_code": resp.status_code, "json": resp.json}


@when("I delete the delivery receipt callback", target_fixture="api_response")
def delete_delivery_callback(admin_client, service, callback):
    resp = admin_client.delete(
        f"/service/{service.id}/delivery-receipt-api/{callback.id}",
    )
    return {"status_code": resp.status_code, "json": resp.json if resp.status_code != 204 else {}}


@when(
    parsers.parse('I create an inbound SMS callback with URL "{url}"'),
    target_fixture="api_response",
)
def create_inbound_callback(admin_client, service, url):
    resp = admin_client.post(
        f"/service/{service.id}/inbound-api",
        data={
            "url": url,
            "bearer_token": "new_secret_token_1234",
            "updated_by_id": str(service.users[0].id),
        },
    )
    return {"status_code": resp.status_code, "json": resp.json}


@when("I get the inbound SMS callback", target_fixture="api_response")
def get_inbound_callback(admin_client, service, callback):
    resp = admin_client.get(
        f"/service/{service.id}/inbound-api/{callback.id}",
    )
    return {"status_code": resp.status_code, "json": resp.json}


@when("I update the inbound SMS callback URL", target_fixture="api_response")
def update_inbound_callback(admin_client, service, callback):
    resp = admin_client.post(
        f"/service/{service.id}/inbound-api/{callback.id}",
        data={
            "url": "https://example.com/inbound-updated",
            "bearer_token": "updated_secret_token_1234",
            "updated_by_id": str(service.users[0].id),
        },
    )
    return {"status_code": resp.status_code, "json": resp.json}


@when("I delete the inbound SMS callback", target_fixture="api_response")
def delete_inbound_callback(admin_client, service, callback):
    resp = admin_client.delete(
        f"/service/{service.id}/inbound-api/{callback.id}",
    )
    return {"status_code": resp.status_code, "json": resp.json if resp.status_code != 204 else {}}


# -- Then steps --


@then("the callback URL should be present")
def response_has_callback_url(api_response):
    data = api_response["json"]["data"]
    assert "url" in data
    assert data["url"] is not None
