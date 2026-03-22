"""Step definitions for service settings features."""

import uuid

from pytest_bdd import given, scenarios, then, when

from app.enums import NotificationType, ServicePermissionType
from tests.app.db import (
    create_organization,
    create_reply_to_email,
    create_service_data_retention,
    create_service_sms_sender,
)

scenarios("../features/services/service_settings.feature")


# -- Given steps --


@given("an email reply-to address exists", target_fixture="reply_to")
def email_reply_to_exists(notify_db_session, service):
    return create_reply_to_email(service, "reply@example.gov.uk")


@given("an SMS sender exists", target_fixture="sms_sender")
def sms_sender_exists(notify_db_session, service):
    return create_service_sms_sender(service, "12025551234", is_default=False)


@given("data retention settings exist for email", target_fixture="data_retention")
def data_retention_exists(notify_db_session, service):
    return create_service_data_retention(
        service, notification_type=NotificationType.EMAIL, days_of_retention=7
    )


@given("the service belongs to an organization", target_fixture="organization")
def service_has_organization(notify_db_session, service):
    org = create_organization(name="Test Organization")
    service.organization_id = org.id
    from app import db

    db.session.commit()
    return org


# -- When steps --


@when("the email reply-to addresses are retrieved", target_fixture="api_response")
def get_reply_to_addresses(admin_client, service, api_response):
    resp = admin_client.get(f"/service/{service.id}/email-reply-to")
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


@when("an email reply-to address is added", target_fixture="api_response")
def add_reply_to_address(admin_client, service, api_response):
    data = {"email_address": "new-reply@example.gov.uk", "is_default": True}
    resp = admin_client.post(f"/service/{service.id}/email-reply-to", data=data)
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


@when("the email reply-to address is retrieved by ID", target_fixture="api_response")
def get_reply_to_by_id(admin_client, service, reply_to, api_response):
    resp = admin_client.get(
        f"/service/{service.id}/email-reply-to/{reply_to.id}"
    )
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


@when("the email reply-to address is updated", target_fixture="api_response")
def update_reply_to(admin_client, service, reply_to, api_response):
    data = {"email_address": "updated-reply@example.gov.uk", "is_default": True}
    resp = admin_client.post(
        f"/service/{service.id}/email-reply-to/{reply_to.id}",
        data=data,
    )
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


@when("the SMS senders are retrieved", target_fixture="api_response")
def get_sms_senders(admin_client, service, api_response):
    resp = admin_client.get(f"/service/{service.id}/sms-sender")
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


@when("an SMS sender is added", target_fixture="api_response")
def add_sms_sender(admin_client, service, api_response):
    data = {"sms_sender": "12025559999", "is_default": False}
    resp = admin_client.post(f"/service/{service.id}/sms-sender", data=data)
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


@when("the SMS sender is retrieved by ID", target_fixture="api_response")
def get_sms_sender_by_id(admin_client, service, sms_sender, api_response):
    resp = admin_client.get(
        f"/service/{service.id}/sms-sender/{sms_sender.id}"
    )
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


@when("the SMS sender is updated", target_fixture="api_response")
def update_sms_sender(admin_client, service, sms_sender, api_response):
    data = {"sms_sender": "12025558888", "is_default": False}
    resp = admin_client.post(
        f"/service/{service.id}/sms-sender/{sms_sender.id}",
        data=data,
    )
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


@when("the guest list is retrieved", target_fixture="api_response")
def get_guest_list(admin_client, service, api_response):
    resp = admin_client.get(f"/service/{service.id}/guest-list")
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


@when("the guest list is updated", target_fixture="api_response")
def update_guest_list(admin_client, service, api_response):
    data = {
        "email_addresses": ["test@example.gov.uk"],
        "phone_numbers": [],
    }
    resp = admin_client.put(f"/service/{service.id}/guest-list", data=data)
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json() if resp.data else None
    return api_response


@when("the data retention settings are retrieved", target_fixture="api_response")
def get_data_retention(admin_client, service, api_response):
    resp = admin_client.get(f"/service/{service.id}/data-retention")
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


@when("data retention settings are added for email", target_fixture="api_response")
def add_data_retention(admin_client, service, api_response):
    data = {
        "notification_type": "email",
        "days_of_retention": 7,
    }
    resp = admin_client.post(f"/service/{service.id}/data-retention", data=data)
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


@when("the data retention setting is retrieved by ID", target_fixture="api_response")
def get_data_retention_by_id(admin_client, service, data_retention, api_response):
    resp = admin_client.get(
        f"/service/{service.id}/data-retention/{data_retention.id}"
    )
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


@when("the data retention setting is updated", target_fixture="api_response")
def update_data_retention(admin_client, service, data_retention, api_response):
    data = {"days_of_retention": 14}
    resp = admin_client.post(
        f"/service/{service.id}/data-retention/{data_retention.id}",
        data=data,
    )
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


@when("the service permissions are updated", target_fixture="api_response")
def update_service_permissions(admin_client, service, api_response):
    data = {
        "permissions": [
            ServicePermissionType.EMAIL,
            ServicePermissionType.SMS,
        ],
        "created_by": str(service.users[0].id),
    }
    resp = admin_client.post(f"/service/{service.id}", data=data)
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


@when("the service organization is retrieved", target_fixture="api_response")
def get_service_organization(admin_client, service, api_response):
    resp = admin_client.get(f"/service/{service.id}/organization")
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


# -- Then steps --


@then("the response should contain service permissions")
def response_has_permissions(api_response):
    data = api_response["json"]["data"]
    assert "permissions" in data


@then("the response should contain organization details")
def response_has_organization(api_response):
    data = api_response["json"]
    assert data is not None
