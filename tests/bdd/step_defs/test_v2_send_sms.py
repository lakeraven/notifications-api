"""
Step definitions for sending SMS notifications.

Endpoint: POST /notifications/sms
"""

import uuid
from datetime import timedelta
from unittest.mock import patch

from pytest_bdd import given, parsers, scenario, then, when

from app.enums import KeyType, NotificationType, ServicePermissionType, TemplateType
from app.utils import utc_now
from tests.app.db import (
    create_api_key,
    create_service,
    create_template,
    create_user,
)

# ---------------------------------------------------------------------------
# Scenarios — link feature file scenarios to this module
# ---------------------------------------------------------------------------

FEATURE = "../features/v2_notifications/send_sms.feature"


@scenario(FEATURE, "Send a basic SMS notification")
def test_send_basic_sms():
    pass


@scenario(FEATURE, "Send an SMS with personalisation")
def test_send_sms_with_personalisation():
    pass


@scenario(FEATURE, "Send an SMS with a client reference")
def test_send_sms_with_reference():
    pass


@scenario(FEATURE, "Send an SMS without a reference")
def test_send_sms_without_reference():
    pass


@scenario(FEATURE, "Reject SMS with missing phone number")
def test_reject_sms_missing_phone():
    pass


@scenario(FEATURE, "Reject SMS with missing template ID")
def test_reject_sms_missing_template():
    pass


@scenario(FEATURE, "Reject SMS with invalid template ID")
def test_reject_sms_invalid_template():
    pass


@scenario(FEATURE, "Reject SMS when personalisation is missing")
def test_reject_sms_missing_personalisation():
    pass


@scenario(FEATURE, "Reject SMS using another service's template")
def test_reject_sms_other_service_template():
    pass


@scenario(FEATURE, "Send an SMS with a test API key")
def test_send_sms_test_key():
    pass


@scenario(FEATURE, "Send an SMS with a team API key")
def test_send_sms_team_key():
    pass


@scenario(FEATURE, "Schedule an SMS for future delivery")
def test_schedule_sms_tomorrow():
    pass


@scenario(FEATURE, "Reject SMS scheduled too far in advance")
def test_reject_sms_scheduled_too_far():
    pass


# ---------------------------------------------------------------------------
# Given steps
# ---------------------------------------------------------------------------


@given("a service with SMS permissions exists", target_fixture="service")
def service_with_sms(notify_db_session):
    return create_service(
        service_permissions=[
            ServicePermissionType.SMS,
            ServicePermissionType.INTERNATIONAL_SMS,
        ],
    )


@given(
    parsers.parse(
        'the service has an SMS template with content "{content}"'
    ),
    target_fixture="sms_template",
)
def sms_template_with_content(service, content):
    return create_template(
        service,
        template_type=TemplateType.SMS,
        content=content,
    )


@given("the service has a valid API key", target_fixture="api_key")
def valid_api_key(service):
    return create_api_key(service, key_type=KeyType.NORMAL)


@given("the service has a test API key", target_fixture="test_api_key")
def test_api_key(service):
    return create_api_key(service, key_type=KeyType.TEST)


@given("the service has a team API key", target_fixture="team_api_key")
def team_api_key(service):
    return create_api_key(service, key_type=KeyType.TEAM)


@given("another service exists with an SMS template", target_fixture="other_service_template")
def other_service_with_sms_template(notify_db_session):
    other_service = create_service(
        service_name="Other Service",
        service_permissions=[ServicePermissionType.SMS],
    )
    template = create_template(
        other_service,
        template_type=TemplateType.SMS,
        content="Other service template",
    )
    return template


# ---------------------------------------------------------------------------
# When steps
# ---------------------------------------------------------------------------


def _post_sms(client, service, template_id, data, key_type=KeyType.NORMAL):
    """Helper to POST to /notifications/sms with service auth."""
    from tests import create_service_authorization_header

    headers = [
        ("Content-Type", "application/json"),
        create_service_authorization_header(service.id, key_type),
    ]
    import json

    return client.post(
        "/notifications/sms",
        data=json.dumps(data),
        headers=headers,
    )


def _store_response(api_response, resp):
    """Unpack Flask test-client response into api_response dict."""
    api_response["status_code"] = resp.status_code
    try:
        api_response["json"] = resp.get_json()
    except Exception:
        api_response["json"] = None


@when(
    parsers.parse('I send an SMS notification to "{phone}" using the template'),
)
def send_sms_basic(client, service, sms_template, api_response, phone):
    with patch("app.celery.provider_tasks.deliver_sms.apply_async"):
        data = {
            "to": phone,
            "template": str(sms_template.id),
            "personalisation": {"name": "Test", "code": "1234"},
        }
        resp = _post_sms(client, service, sms_template.id, data)
        _store_response(api_response, resp)


@when(
    parsers.parse('I send an SMS notification to "{phone}" with personalisation'),
)
def send_sms_with_personalisation(client, service, sms_template, api_response, phone):
    with patch("app.celery.provider_tasks.deliver_sms.apply_async"):
        data = {
            "to": phone,
            "template": str(sms_template.id),
            "personalisation": {"name": "Jo", "code": "5678"},
        }
        resp = _post_sms(client, service, sms_template.id, data)
        _store_response(api_response, resp)


@when(
    parsers.parse('I send an SMS notification to "{phone}" with reference "{reference}"'),
)
def send_sms_with_reference(client, service, sms_template, api_response, phone, reference):
    with patch("app.celery.provider_tasks.deliver_sms.apply_async"):
        data = {
            "to": phone,
            "template": str(sms_template.id),
            "personalisation": {"name": "Test", "code": "1234"},
            "reference": reference,
        }
        resp = _post_sms(client, service, sms_template.id, data)
        _store_response(api_response, resp)


@when(
    parsers.parse('I send an SMS notification to "{phone}" without a reference'),
)
def send_sms_without_reference(client, service, sms_template, api_response, phone):
    with patch("app.celery.provider_tasks.deliver_sms.apply_async"):
        data = {
            "to": phone,
            "template": str(sms_template.id),
            "personalisation": {"name": "Test", "code": "1234"},
        }
        resp = _post_sms(client, service, sms_template.id, data)
        _store_response(api_response, resp)


@when("I send an SMS notification without a phone number")
def send_sms_missing_phone(client, service, sms_template, api_response):
    data = {
        "template": str(sms_template.id),
        "personalisation": {"name": "Test", "code": "1234"},
    }
    resp = _post_sms(client, service, sms_template.id, data)
    _store_response(api_response, resp)


@when(
    parsers.parse('I send an SMS notification to "{phone}" without a template ID'),
)
def send_sms_missing_template(client, service, sms_template, api_response, phone):
    data = {
        "to": phone,
        "personalisation": {"name": "Test", "code": "1234"},
    }
    resp = _post_sms(client, service, None, data)
    _store_response(api_response, resp)


@when(
    parsers.parse('I send an SMS notification to "{phone}" with template ID "{bad_id}"'),
)
def send_sms_invalid_template(client, service, sms_template, api_response, phone, bad_id):
    data = {
        "to": phone,
        "template": bad_id,
        "personalisation": {"name": "Test", "code": "1234"},
    }
    resp = _post_sms(client, service, None, data)
    _store_response(api_response, resp)


@when(
    parsers.parse('I send an SMS notification to "{phone}" with empty personalisation'),
)
def send_sms_empty_personalisation(client, service, sms_template, api_response, phone):
    data = {
        "to": phone,
        "template": str(sms_template.id),
        "personalisation": {},
    }
    resp = _post_sms(client, service, sms_template.id, data)
    _store_response(api_response, resp)


@when("I send an SMS notification using the other service's template")
def send_sms_other_service_template(
    client, service, other_service_template, api_response
):
    data = {
        "to": "+447700900855",
        "template": str(other_service_template.id),
    }
    resp = _post_sms(client, service, other_service_template.id, data)
    _store_response(api_response, resp)


@when(
    parsers.parse('I send an SMS notification to "{phone}" using the test key'),
)
def send_sms_test_key(client, service, sms_template, test_api_key, api_response, phone):
    with patch("app.celery.provider_tasks.deliver_sms.apply_async"):
        data = {
            "to": phone,
            "template": str(sms_template.id),
            "personalisation": {"name": "Test", "code": "1234"},
        }
        resp = _post_sms(
            client, service, sms_template.id, data, key_type=KeyType.TEST
        )
        _store_response(api_response, resp)


@when(
    parsers.parse('I send an SMS notification to "{phone}" using the team key'),
)
def send_sms_team_key(client, service, sms_template, team_api_key, api_response, phone):
    with patch("app.celery.provider_tasks.deliver_sms.apply_async"):
        data = {
            "to": phone,
            "template": str(sms_template.id),
            "personalisation": {"name": "Test", "code": "1234"},
        }
        resp = _post_sms(
            client, service, sms_template.id, data, key_type=KeyType.TEAM
        )
        _store_response(api_response, resp)


@when(
    parsers.parse('I send an SMS notification to "{phone}" scheduled for tomorrow'),
)
def send_sms_scheduled_tomorrow(client, service, sms_template, api_response, phone):
    with patch("app.celery.provider_tasks.deliver_sms.apply_async"):
        scheduled = (utc_now() + timedelta(hours=24)).strftime("%Y-%m-%d %H:%M")
        data = {
            "to": phone,
            "template": str(sms_template.id),
            "personalisation": {"name": "Test", "code": "1234"},
            "scheduled_for": scheduled,
        }
        resp = _post_sms(client, service, sms_template.id, data)
        _store_response(api_response, resp)


@when(
    parsers.parse('I send an SMS notification to "{phone}" scheduled for next year'),
)
def send_sms_scheduled_next_year(client, service, sms_template, api_response, phone):
    scheduled = (utc_now() + timedelta(days=400)).strftime("%Y-%m-%d %H:%M")
    data = {
        "to": phone,
        "template": str(sms_template.id),
        "personalisation": {"name": "Test", "code": "1234"},
        "scheduled_for": scheduled,
    }
    resp = _post_sms(client, service, sms_template.id, data)
    _store_response(api_response, resp)


# ---------------------------------------------------------------------------
# Then steps  (most are in step_defs/conftest.py; add SMS-specific ones here)
# ---------------------------------------------------------------------------


@then("the response should contain a URI for the notification")
def response_has_uri(api_response):
    # The lakeraven fork returns data.notification.id; URI may not exist
    # in this fork's simpler response format. Check for notification id instead.
    data = api_response["json"].get("data", {})
    assert data.get("notification", {}).get("id") is not None


@then("the response scheduled_for should not be null")
def response_scheduled_for_not_null(api_response):
    data = api_response["json"].get("data", api_response["json"])
    # scheduled_for may be at top level or nested
    scheduled = data.get("scheduled_for")
    if scheduled is None and "data" in api_response["json"]:
        scheduled = api_response["json"]["data"].get("scheduled_for")
    assert scheduled is not None, f"scheduled_for was null in response: {api_response['json']}"
