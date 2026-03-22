"""Step definitions for service callback features."""

import uuid

from pytest_bdd import given, scenarios, then, when

from tests.app.db import create_service_callback_api

scenarios("../features/services/callbacks.feature")


# -- Given steps --


@given("a delivery receipt callback exists", target_fixture="delivery_callback")
def delivery_callback_exists(notify_db_session, service):
    from app.enums import CallbackType

    return create_service_callback_api(
        service=service,
        url="https://example.com/delivery",
        callback_type=CallbackType.DELIVERY_STATUS,
    )


@given("an inbound API callback exists", target_fixture="inbound_callback")
def inbound_callback_exists(notify_db_session, service):
    from app.dao.service_inbound_api_dao import save_service_inbound_api
    from app.models import ServiceInboundApi

    inbound_api = ServiceInboundApi(
        service_id=service.id,
        url="https://example.com/inbound",
        bearer_token="some_super_secret",
        updated_by_id=service.users[0].id,
    )
    save_service_inbound_api(inbound_api)
    return inbound_api


# -- When steps --


@when("a delivery receipt callback is created", target_fixture="api_response")
def create_delivery_callback(admin_client, service, api_response):
    data = {
        "url": "https://example.com/delivery",
        "bearer_token": "some_super_secret",
        "updated_by_id": str(service.users[0].id),
    }
    resp = admin_client.post(
        f"/service/{service.id}/delivery-receipt-api",
        data=data,
    )
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


@when("the delivery receipt callback is retrieved", target_fixture="api_response")
def get_delivery_callback(admin_client, service, delivery_callback, api_response):
    resp = admin_client.get(
        f"/service/{service.id}/delivery-receipt-api/{delivery_callback.id}"
    )
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


@when("the delivery receipt callback URL is updated", target_fixture="api_response")
def update_delivery_callback(admin_client, service, delivery_callback, api_response):
    data = {
        "url": "https://example.com/updated-delivery",
        "updated_by_id": str(service.users[0].id),
    }
    resp = admin_client.post(
        f"/service/{service.id}/delivery-receipt-api/{delivery_callback.id}",
        data=data,
    )
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


@when("the delivery receipt callback is deleted", target_fixture="api_response")
def delete_delivery_callback(admin_client, service, delivery_callback, api_response):
    resp = admin_client.delete(
        f"/service/{service.id}/delivery-receipt-api/{delivery_callback.id}"
    )
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json() if resp.data else None
    return api_response


@when("an inbound API callback is created", target_fixture="api_response")
def create_inbound_callback(admin_client, service, api_response):
    data = {
        "url": "https://example.com/inbound",
        "bearer_token": "some_super_secret",
        "updated_by_id": str(service.users[0].id),
    }
    resp = admin_client.post(
        f"/service/{service.id}/inbound-api",
        data=data,
    )
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


@when("the inbound API callback is retrieved", target_fixture="api_response")
def get_inbound_callback(admin_client, service, inbound_callback, api_response):
    resp = admin_client.get(
        f"/service/{service.id}/inbound-api/{inbound_callback.id}"
    )
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


@when("the inbound API callback URL is updated", target_fixture="api_response")
def update_inbound_callback(admin_client, service, inbound_callback, api_response):
    data = {
        "url": "https://example.com/updated-inbound",
        "updated_by_id": str(service.users[0].id),
    }
    resp = admin_client.post(
        f"/service/{service.id}/inbound-api/{inbound_callback.id}",
        data=data,
    )
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


@when("the inbound API callback is deleted", target_fixture="api_response")
def delete_inbound_callback(admin_client, service, inbound_callback, api_response):
    resp = admin_client.delete(
        f"/service/{service.id}/inbound-api/{inbound_callback.id}"
    )
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json() if resp.data else None
    return api_response
