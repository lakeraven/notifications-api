"""
Step definitions for getting / listing notifications.

Endpoints:
  GET /notifications/<uuid>   — single notification
  GET /notifications           — list notifications
"""

import uuid

from pytest_bdd import given, parsers, scenario, then, when

from app.enums import (
    KeyType,
    NotificationStatus,
    NotificationType,
    ServicePermissionType,
    TemplateType,
)
from tests.app.db import (
    create_api_key,
    create_notification,
    create_service,
    create_template,
    create_user,
)

# ---------------------------------------------------------------------------
# Scenarios
# ---------------------------------------------------------------------------

FEATURE = "../features/v2_notifications/get_notification.feature"


@scenario(FEATURE, "Get an SMS notification by ID")
def test_get_sms_notification():
    pass


@scenario(FEATURE, "Get an email notification by ID")
def test_get_email_notification():
    pass


@scenario(FEATURE, "Reject request for notification from another service")
def test_reject_other_service_notification():
    pass


@scenario(FEATURE, "Reject request with invalid notification ID")
def test_reject_invalid_id():
    pass


@scenario(FEATURE, "Reject request with nonexistent notification ID")
def test_reject_nonexistent_id():
    pass


@scenario(FEATURE, "List notifications with default pagination")
def test_list_notifications():
    pass


@scenario(FEATURE, "List notifications filtered by template type")
def test_list_filtered_by_type():
    pass


@scenario(FEATURE, "List notifications filtered by status")
def test_list_filtered_by_status():
    pass


@scenario(FEATURE, "List notifications filtered by reference")
def test_list_filtered_by_reference():
    pass


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _get(client, service, path, key_type=KeyType.NORMAL):
    from tests import create_service_authorization_header

    headers = [
        create_service_authorization_header(service.id, key_type),
    ]
    return client.get(path, headers=headers)


def _store_response(api_response, resp):
    api_response["status_code"] = resp.status_code
    try:
        api_response["json"] = resp.get_json()
    except Exception:
        api_response["json"] = None


# ---------------------------------------------------------------------------
# Given steps
# ---------------------------------------------------------------------------


@given("a service exists with a valid API key", target_fixture="service")
def service_with_key(notify_db_session):
    service = create_service(
        service_permissions=[
            ServicePermissionType.SMS,
            ServicePermissionType.EMAIL,
        ],
    )
    create_api_key(service, key_type=KeyType.NORMAL)
    return service


@given("an SMS notification has been sent", target_fixture="sms_notification")
def sms_notification_sent(service):
    template = create_template(service, template_type=TemplateType.SMS)
    notification = create_notification(
        template=template,
        status=NotificationStatus.CREATED,
    )
    return notification


@given("an email notification has been sent", target_fixture="email_notification")
def email_notification_sent(service):
    template = create_template(
        service,
        template_type=TemplateType.EMAIL,
        subject="Test subject",
    )
    notification = create_notification(
        template=template,
        status=NotificationStatus.CREATED,
    )
    return notification


@given("another service has a notification", target_fixture="other_notification")
def other_service_notification(notify_db_session):
    other_service = create_service(
        service_name="Other Service",
        service_permissions=[ServicePermissionType.SMS],
    )
    template = create_template(other_service, template_type=TemplateType.SMS)
    return create_notification(template=template)


@given(
    parsers.parse("{count:d} notifications have been sent"),
    target_fixture="many_notifications",
)
def many_notifications_sent(service, count):
    template = create_template(
        service,
        template_type=TemplateType.SMS,
        template_name=f"Bulk SMS {uuid.uuid4()}",
    )
    notifications = []
    for _ in range(count):
        notifications.append(
            create_notification(template=template, status=NotificationStatus.CREATED)
        )
    return notifications


@given(
    "both SMS and email notifications have been sent",
    target_fixture="mixed_notifications",
)
def mixed_notifications(service):
    sms_tmpl = create_template(
        service,
        template_type=TemplateType.SMS,
        template_name=f"Mixed SMS {uuid.uuid4()}",
    )
    email_tmpl = create_template(
        service,
        template_type=TemplateType.EMAIL,
        template_name=f"Mixed Email {uuid.uuid4()}",
        subject="Mixed",
    )
    return {
        "sms": [
            create_notification(template=sms_tmpl, status=NotificationStatus.CREATED)
            for _ in range(3)
        ],
        "email": [
            create_notification(template=email_tmpl, status=NotificationStatus.CREATED)
            for _ in range(3)
        ],
    }


@given(
    "notifications with various statuses exist",
    target_fixture="status_notifications",
)
def notifications_various_statuses(service):
    template = create_template(
        service,
        template_type=TemplateType.SMS,
        template_name=f"Status SMS {uuid.uuid4()}",
    )
    results = {}
    for status in (
        NotificationStatus.CREATED,
        NotificationStatus.SENDING,
        NotificationStatus.DELIVERED,
    ):
        results[status] = create_notification(template=template, status=status)
    return results


@given(
    parsers.parse('notifications with reference "{reference}" exist'),
    target_fixture="ref_notifications",
)
def notifications_with_reference(service, reference):
    template = create_template(
        service,
        template_type=TemplateType.SMS,
        template_name=f"Ref SMS {uuid.uuid4()}",
    )
    return [
        create_notification(
            template=template,
            client_reference=reference,
            status=NotificationStatus.CREATED,
        )
        for _ in range(3)
    ]


# ---------------------------------------------------------------------------
# When steps
# ---------------------------------------------------------------------------


@when("I request the notification by ID")
def request_notification_by_id(client, service, api_response, sms_notification, request):
    # Use the most recently created notification fixture available.
    # email_notification overrides sms_notification when present.
    notification = request.getfixturevalue("email_notification") if "email_notification" in request.fixturenames else sms_notification
    resp = _get(client, service, f"/notifications/{notification.id}")
    _store_response(api_response, resp)


@when("I request that notification by ID")
def request_other_notification(client, service, other_notification, api_response):
    resp = _get(client, service, f"/notifications/{other_notification.id}")
    _store_response(api_response, resp)


@when(parsers.parse('I request a notification with ID "{bad_id}"'))
def request_notification_invalid_id(client, service, api_response, bad_id):
    resp = _get(client, service, f"/notifications/{bad_id}")
    _store_response(api_response, resp)


@when("I request a notification with a random UUID")
def request_notification_random_uuid(client, service, api_response):
    resp = _get(client, service, f"/notifications/{uuid.uuid4()}")
    _store_response(api_response, resp)


@when("I list all notifications")
def list_all_notifications(client, service, api_response):
    resp = _get(client, service, "/notifications")
    _store_response(api_response, resp)


@when(parsers.parse('I list notifications with template_type "{template_type}"'))
def list_notifications_by_type(client, service, api_response, template_type):
    resp = _get(client, service, f"/notifications?template_type={template_type}")
    _store_response(api_response, resp)


@when(parsers.parse('I list notifications with status "{status}"'))
def list_notifications_by_status(client, service, api_response, status):
    resp = _get(client, service, f"/notifications?status={status}")
    _store_response(api_response, resp)


@when(parsers.parse('I list notifications with reference "{reference}"'))
def list_notifications_by_reference(client, service, api_response, reference):
    resp = _get(client, service, f"/notifications?reference={reference}")
    _store_response(api_response, resp)


# ---------------------------------------------------------------------------
# Then steps
# ---------------------------------------------------------------------------


@then("the response should contain the notification ID")
def response_contains_notification_id(api_response):
    data = api_response["json"]
    # GET single wraps in data.notification
    notification = data.get("data", {}).get("notification", data)
    assert notification.get("id") is not None


@then("the response should contain a list of notifications")
def response_has_notification_list(api_response):
    data = api_response["json"]
    assert "notifications" in data
    assert isinstance(data["notifications"], list)
    assert len(data["notifications"]) > 0


@then("the response should include pagination links")
def response_has_pagination_links(api_response):
    data = api_response["json"]
    assert "links" in data


@then(parsers.parse('all returned notifications should be of type "{ntype}"'))
def all_notifications_of_type(api_response, ntype):
    data = api_response["json"]
    notifications = data.get("notifications", [])
    assert len(notifications) > 0, "Expected at least one notification"
    for n in notifications:
        assert n.get("type") == ntype or n.get("template", {}).get("template_type") == ntype, (
            f"Expected type '{ntype}', got {n}"
        )


@then(parsers.parse('all returned notifications should have status "{status}"'))
def all_notifications_with_status(api_response, status):
    data = api_response["json"]
    notifications = data.get("notifications", [])
    assert len(notifications) > 0, "Expected at least one notification"
    for n in notifications:
        assert n.get("status") == status, f"Expected status '{status}', got '{n.get('status')}'"


@then(parsers.parse('all returned notifications should have reference "{reference}"'))
def all_notifications_with_reference(api_response, reference):
    data = api_response["json"]
    notifications = data.get("notifications", [])
    assert len(notifications) > 0, "Expected at least one notification"
    for n in notifications:
        assert n.get("client_reference") == reference or n.get("reference") == reference, (
            f"Expected reference '{reference}', got {n}"
        )
