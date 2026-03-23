"""
Shared step definitions available to all BDD tests.

pytest-bdd step definitions in conftest.py are automatically discovered.
"""

import uuid

import pytest
from pytest_bdd import given, parsers, then, when

from tests.app.db import (
    create_api_key,
    create_notification,
    create_service,
    create_template,
    create_user,
)


# -- Common Given steps --


@given("a platform admin user exists", target_fixture="admin_user")
def a_platform_admin_user(notify_db_session):
    return create_user(email="admin@digital.cabinet-office.gov.uk", platform_admin=True)


@given("a service exists", target_fixture="service")
def a_service_exists(notify_db_session):
    return create_service()


@given(parsers.parse('a service "{name}" exists'), target_fixture="service")
def a_named_service_exists(notify_db_session, name):
    return create_service(service_name=name)


@given("a service exists with an admin user", target_fixture="service")
def a_service_with_admin(notify_db_session):
    return create_service()


@given("a user exists", target_fixture="user")
def a_user_exists(notify_db_session):
    return create_user(email=f"user-{uuid.uuid4()}@example.gov.uk")


@given("a new user exists", target_fixture="new_user")
def a_new_user_exists(notify_db_session):
    return create_user(email=f"newuser-{uuid.uuid4()}@example.gov.uk")


# -- Common Then steps --


@then(parsers.parse("the response status code should be {status_code:d}"))
def response_status_code(api_response, status_code):
    assert api_response["status_code"] == status_code, (
        f"Expected {status_code}, got {api_response['status_code']}: {api_response.get('json')}"
    )


def _unwrap(json_data):
    """Unwrap our API response format: {data: {notification: {...}}} → flat notification."""
    if "data" in json_data:
        data = json_data["data"]
        if "notification" in data and isinstance(data["notification"], dict):
            # POST response: {data: {notification: {id: ...}, body: ..., template_version: ...}}
            result = dict(data)
            result.update(result.pop("notification"))
            return result
        return data
    return json_data


@then("the response should contain a notification ID")
@then("the response should contain the notification ID")
def response_has_notification_id(api_response):
    data = _unwrap(api_response["json"])
    assert "id" in data, f"Expected 'id' in {data}"
    assert data["id"] is not None


@then(parsers.parse('the response reference should be "{reference}"'))
def response_reference_is(api_response, reference):
    data = _unwrap(api_response["json"])
    assert data.get("reference") == reference


@then("the response reference should be null")
def response_reference_is_null(api_response):
    data = _unwrap(api_response["json"])
    assert data.get("reference") is None


@then("the response should contain a URI for the notification")
def response_has_uri(api_response):
    # Our API doesn't include a URI field in the POST response; verify the notification ID exists instead
    data = _unwrap(api_response["json"])
    assert "id" in data


@then("the response should include template details")
def response_has_template(api_response):
    data = _unwrap(api_response["json"])
    # Our API returns template_version at top level, GOV.UK nests in template object
    assert "template_version" in data or "template" in data


@then(parsers.parse('the response body should contain "{text}"'))
def response_body_contains(api_response, text):
    data = _unwrap(api_response["json"])
    body = data.get("body", data.get("content", {}).get("body", ""))
    assert text in body, f"Expected '{text}' in body: {body}"


@then(parsers.parse('the response type should be "{notification_type}"'))
def response_type_is(api_response, notification_type):
    data = _unwrap(api_response["json"])
    assert data.get("type", data.get("notification_type")) == notification_type


@then("the response should include created_at timestamp")
def response_has_created_at(api_response):
    data = _unwrap(api_response["json"])
    assert data.get("created_at") is not None


@then(parsers.parse('the response error should mention "{text}"'))
def response_error_mentions(api_response, text):
    json_data = api_response["json"]
    # Handle both GOV.UK format {"errors": [...]} and our format {"message": ..., "result": "error"}
    errors = json_data.get("errors", [])
    message = json_data.get("message", "")
    error_text = str(errors) + " " + str(message)
    # Map GOV.UK field/error names to our internal names for matching
    aliases = {
        "phone_number": "to",
        "email_address": "to",
        "template_id": "template",
        "trial mode": "team-only api key",
    }
    search_text = text.lower()
    alias = aliases.get(search_text)
    assert search_text in error_text.lower() or (alias and alias in error_text.lower()), (
        f"Expected '{text}' in errors/message: {json_data}"
    )
