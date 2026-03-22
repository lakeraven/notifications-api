"""Step definitions for email branding features."""

import uuid

from pytest_bdd import given, parsers, scenarios, then, when

from tests.app.db import create_email_branding

scenarios("../features/branding/email_branding.feature")


# -- Given steps --


@given(
    parsers.parse('an email branding "{name}" exists'),
    target_fixture="email_branding",
)
def email_branding_exists(notify_db_session, name):
    return create_email_branding(name=name)


# -- When steps --


@when("all email brandings are retrieved", target_fixture="api_response")
def get_all_email_brandings(admin_client, api_response):
    resp = admin_client.get("/email-branding")
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


@when(
    parsers.parse('a new email branding "{name}" is created'),
    target_fixture="api_response",
)
def create_new_email_branding(admin_client, api_response, name):
    data = {
        "name": name,
        "colour": "#000000",
        "logo": "test_logo.png",
        "text": name,
    }
    resp = admin_client.post("/email-branding", data=data)
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


@when("the email branding is retrieved by ID", target_fixture="api_response")
def get_email_branding_by_id(admin_client, email_branding, api_response):
    resp = admin_client.get(f"/email-branding/{email_branding.id}")
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


@when(
    parsers.parse('the email branding name is updated to "{name}"'),
    target_fixture="api_response",
)
def update_email_branding_name(admin_client, email_branding, name, api_response):
    data = {
        "name": name,
        "colour": email_branding.colour,
        "logo": email_branding.logo,
        "text": name,
    }
    resp = admin_client.post(
        f"/email-branding/{email_branding.id}",
        data=data,
    )
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


@when("a new email branding is created with a logo", target_fixture="api_response")
def create_email_branding_with_logo(admin_client, api_response):
    data = {
        "name": f"Logo Brand {uuid.uuid4()}",
        "colour": "#FF0000",
        "logo": "custom_logo.png",
        "text": "Logo Brand",
    }
    resp = admin_client.post("/email-branding", data=data)
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


# -- Then steps --


@then(parsers.parse('the response should contain the branding name "{name}"'))
def response_has_branding_name(api_response, name):
    data = api_response["json"]["email_branding"]
    assert data["name"] == name


@then(parsers.parse('the response should contain branding "{name}"'))
def response_contains_branding(api_response, name):
    data = api_response["json"]["email_branding"]
    assert isinstance(data, list)
    names = [b["name"] for b in data]
    assert name in names
