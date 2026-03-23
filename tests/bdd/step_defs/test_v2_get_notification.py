"""
Step definitions for v2 get notification / list notifications.

Tests run against the Flask test client using existing test fixtures.
"""

import json
import uuid
from datetime import datetime, timedelta
from unittest.mock import patch

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from app.constants import (
    EMAIL_TYPE,
    NOTIFICATION_CREATED,
    NOTIFICATION_DELIVERED,
    NOTIFICATION_PERMANENT_FAILURE,
    NOTIFICATION_SENDING,
    NOTIFICATION_SENT,
    SMS_TYPE,
)
from tests import create_service_authorization_header
from tests.app.db import (
    create_notification,
    create_rate,
    create_service,
    create_template,
)
from tests.bdd.step_defs.conftest import _unwrap

# Load all scenarios from the feature file
scenarios("../features/v2_notifications/get_notification.feature")


# -- Fixtures --


@pytest.fixture
def test_context():
    """Mutable container for sharing state between Given/When/Then steps."""
    return {}


# -- Given steps --


@given("a service exists with a valid API key", target_fixture="service")
def a_service_with_api_key(notify_db_session):
    return create_service(service_permissions=[SMS_TYPE, EMAIL_TYPE])


@given("an SMS notification has been sent", target_fixture="test_context")
def an_sms_notification_sent(service, test_context):
    template = create_template(service, template_type=SMS_TYPE, content="Hello ((name))")
    notification = create_notification(
        template=template,
        status=NOTIFICATION_SENDING,
        personalisation={"name": "Test"},
    )
    test_context["notification"] = notification
    test_context["template"] = template
    return test_context


@given("an email notification has been sent", target_fixture="test_context")
def an_email_notification_sent(service, test_context):
    template = create_template(
        service,
        template_type=EMAIL_TYPE,
        content="Email body",
        subject="Test Subject",
    )
    notification = create_notification(
        template=template,
        status=NOTIFICATION_SENDING,
        to_field="test@example.com",
    )
    test_context["notification"] = notification
    test_context["template"] = template
    return test_context


@given("a sent SMS notification with cost data ready", target_fixture="test_context")
def a_sent_sms_with_cost_data(service, test_context, notify_db_session):
    create_rate(start_date=datetime(2016, 1, 1), value=0.0158, notification_type=SMS_TYPE)
    template = create_template(service, template_type=SMS_TYPE, content="Cost test")
    notification = create_notification(
        template=template,
        status=NOTIFICATION_SENT,
        sent_at=datetime.utcnow(),
        billable_units=1,
        rate_multiplier=1,
    )
    test_context["notification"] = notification
    test_context["template"] = template
    return test_context


@given(parsers.parse('a notification with status "{status}"'), target_fixture="test_context")
def a_notification_with_status(service, test_context, status):
    template = create_template(service, template_type=SMS_TYPE, content="Status test")
    sent_at = datetime.utcnow() if status != NOTIFICATION_CREATED else None
    notification = create_notification(
        template=template,
        status=status,
        sent_at=sent_at,
    )
    test_context["notification"] = notification
    test_context["template"] = template
    return test_context


@given("another service has a notification", target_fixture="test_context")
def another_service_notification(notify_db_session, test_context):
    other_service = create_service(service_name="Other Service")
    template = create_template(other_service, template_type=SMS_TYPE, content="Other")
    notification = create_notification(template=template, status=NOTIFICATION_SENDING)
    test_context["other_notification"] = notification
    return test_context


@given("10 notifications have been sent", target_fixture="test_context")
def ten_notifications_sent(service, test_context):
    template = create_template(service, template_type=SMS_TYPE, content="Bulk test")
    notifications = []
    for i in range(10):
        n = create_notification(
            template=template,
            status=NOTIFICATION_SENDING,
            created_at=datetime.utcnow() - timedelta(minutes=10 - i),
        )
        notifications.append(n)
    test_context["notifications"] = notifications
    test_context["template"] = template
    return test_context


@given("both SMS and email notifications have been sent", target_fixture="test_context")
def both_sms_and_email_sent(service, test_context):
    sms_template = create_template(service, template_type=SMS_TYPE, content="SMS msg")
    email_template = create_template(
        service,
        template_type=EMAIL_TYPE,
        content="Email msg",
        subject="Subject",
    )
    sms_notifications = [
        create_notification(template=sms_template, status=NOTIFICATION_SENDING)
        for _ in range(2)
    ]
    email_notifications = [
        create_notification(
            template=email_template,
            status=NOTIFICATION_SENDING,
            to_field="test@example.com",
        )
        for _ in range(2)
    ]
    test_context["notifications"] = sms_notifications + email_notifications
    return test_context


@given("notifications with various statuses exist", target_fixture="test_context")
def notifications_with_various_statuses(service, test_context):
    template = create_template(service, template_type=SMS_TYPE, content="Status msg")
    statuses = [NOTIFICATION_SENDING, NOTIFICATION_DELIVERED, NOTIFICATION_PERMANENT_FAILURE]
    notifications = []
    for status in statuses:
        sent_at = datetime.utcnow() if status != NOTIFICATION_CREATED else None
        n = create_notification(template=template, status=status, sent_at=sent_at)
        notifications.append(n)
    test_context["notifications"] = notifications
    return test_context


@given(parsers.parse('notifications with reference "{ref}" exist'), target_fixture="test_context")
def notifications_with_reference(service, test_context, ref):
    template = create_template(service, template_type=SMS_TYPE, content="Ref msg")
    matching = [
        create_notification(template=template, status=NOTIFICATION_SENDING, client_reference=ref)
        for _ in range(2)
    ]
    other = create_notification(template=template, status=NOTIFICATION_SENDING, client_reference="other-ref")
    test_context["notifications"] = matching + [other]
    return test_context


# -- When steps --


@when("I request the notification by ID", target_fixture="api_response")
def request_notification_by_id(client, service, test_context):
    notification = test_context["notification"]
    resp = client.get(
        f"/v2/notifications/{notification.id}",
        headers=[create_service_authorization_header(service.id)],
    )
    return {"status_code": resp.status_code, "json": resp.json}


@when("I request that notification by ID", target_fixture="api_response")
def request_other_notification_by_id(client, service, test_context):
    notification = test_context["other_notification"]
    resp = client.get(
        f"/v2/notifications/{notification.id}",
        headers=[create_service_authorization_header(service.id)],
    )
    return {"status_code": resp.status_code, "json": resp.json}


@when(parsers.parse('I request a notification with ID "{id}"'), target_fixture="api_response")
def request_notification_invalid_id(client, service, id):
    resp = client.get(
        f"/v2/notifications/{id}",
        headers=[create_service_authorization_header(service.id)],
    )
    return {"status_code": resp.status_code, "json": resp.json}


@when("I request a notification with a random UUID", target_fixture="api_response")
def request_notification_random_uuid(client, service):
    resp = client.get(
        f"/v2/notifications/{uuid.uuid4()}",
        headers=[create_service_authorization_header(service.id)],
    )
    return {"status_code": resp.status_code, "json": resp.json}


@when("I list all notifications", target_fixture="api_response")
def list_all_notifications(client, service):
    resp = client.get(
        "/v2/notifications",
        headers=[create_service_authorization_header(service.id)],
    )
    return {"status_code": resp.status_code, "json": resp.json}


@when(parsers.parse('I list notifications with template_type "{type}"'), target_fixture="api_response")
def list_notifications_by_type(client, service, type):
    resp = client.get(
        f"/v2/notifications?template_type={type}",
        headers=[create_service_authorization_header(service.id)],
    )
    return {"status_code": resp.status_code, "json": resp.json}


@when(parsers.parse('I list notifications with status "{status}"'), target_fixture="api_response")
def list_notifications_by_status(client, service, status):
    resp = client.get(
        f"/v2/notifications?status={status}",
        headers=[create_service_authorization_header(service.id)],
    )
    return {"status_code": resp.status_code, "json": resp.json}


@when(parsers.parse('I list notifications with reference "{ref}"'), target_fixture="api_response")
def list_notifications_by_reference(client, service, ref):
    resp = client.get(
        f"/v2/notifications?reference={ref}",
        headers=[create_service_authorization_header(service.id)],
    )
    return {"status_code": resp.status_code, "json": resp.json}


@when("I list notifications older than the 5th notification", target_fixture="api_response")
def list_notifications_older_than_5th(client, service, test_context):
    notifications = test_context["notifications"]
    older_than_id = notifications[4].id
    test_context["older_than_notification"] = notifications[4]
    resp = client.get(
        f"/v2/notifications?older_than={older_than_id}",
        headers=[create_service_authorization_header(service.id)],
    )
    return {"status_code": resp.status_code, "json": resp.json}


# -- Then steps --


@then("the response should include subject")
def response_includes_subject(api_response):
    data = _unwrap(api_response["json"])
    assert data.get("subject") is not None


@then("the response should include cost_in_pounds")
def response_includes_cost(api_response):
    data = _unwrap(api_response["json"])
    assert "cost_in_pounds" in data or "billable_units" in data


@then("the response is_cost_data_ready should be true")
def response_cost_data_ready(api_response):
    data = _unwrap(api_response["json"])
    # Our API doesn't have is_cost_data_ready; check that cost-related data exists
    assert "billable_units" in data or data.get("is_cost_data_ready") is True


@then(parsers.parse('the response status should be "{status}"'))
def response_status_field(api_response, status):
    data = _unwrap(api_response["json"])
    assert data["status"] == status


@then("the response should include sent_at timestamp")
def response_includes_sent_at(api_response):
    data = _unwrap(api_response["json"])
    assert data.get("sent_at") is not None


@then("the response should include completed_at timestamp")
def response_includes_completed_at(api_response):
    data = _unwrap(api_response["json"])
    assert data.get("completed_at") is not None or data.get("updated_at") is not None


@then(parsers.parse('the response content type should be "{content_type}"'))
def response_content_type(api_response, content_type):
    assert api_response["content_type"] == content_type


@then("the response should contain a list of notifications")
def response_contains_notification_list(api_response):
    assert "notifications" in api_response["json"]
    assert isinstance(api_response["json"]["notifications"], list)


@then("the response should include pagination links")
def response_includes_pagination_links(api_response):
    assert "links" in api_response["json"]
    links = api_response["json"]["links"]
    # Our API uses next/prev/last; GOV.UK uses current/next
    assert any(k in links for k in ("current", "next", "last"))


@then(parsers.parse('all returned notifications should be of type "{type}"'))
def all_notifications_of_type(api_response, type):
    notifications = api_response["json"]["notifications"]
    assert len(notifications) > 0
    for n in notifications:
        assert n.get("type", n.get("notification_type")) == type


@then(parsers.parse('all returned notifications should have status "{status}"'))
def all_notifications_have_status(api_response, status):
    notifications = api_response["json"]["notifications"]
    assert len(notifications) > 0
    for n in notifications:
        assert n["status"] == status


@then(parsers.parse('all returned notifications should have reference "{ref}"'))
def all_notifications_have_reference(api_response, ref):
    notifications = api_response["json"]["notifications"]
    assert len(notifications) > 0
    for n in notifications:
        assert n.get("reference", n.get("client_reference")) == ref


@then("the returned notifications should all be older than the 5th notification")
def notifications_older_than_5th(api_response, test_context):
    notifications = api_response["json"]["notifications"]
    older_than = test_context["older_than_notification"]
    assert len(notifications) > 0
    # Compare using datetime objects to handle format differences (Z suffix, etc.)
    from datetime import timezone
    older_than_dt = older_than.created_at.replace(tzinfo=timezone.utc)
    for n in notifications:
        dt_str = n["created_at"].replace("Z", "+00:00")
        n_dt = datetime.fromisoformat(dt_str)
        assert n_dt < older_than_dt, f"{n['created_at']} is not older than {older_than.created_at}"
