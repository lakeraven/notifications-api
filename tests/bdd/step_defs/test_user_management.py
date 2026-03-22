"""Step definitions for user management features."""

import uuid

from pytest_bdd import given, parsers, scenarios, then, when

from tests.app.db import create_user

scenarios("../features/users/user_management.feature")


# -- When steps --


@when(
    parsers.parse('a new user is created with email "{email}"'),
    target_fixture="api_response",
)
def create_new_user(admin_client, api_response, email):
    data = {
        "name": "New Test User",
        "email_address": email,
        "mobile_number": "+12025551234",
        "password": "password123password",
        "auth_type": "sms_auth",
    }
    resp = admin_client.post("/user", data=data)
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


@when("the user is retrieved by ID", target_fixture="api_response")
def get_user_by_id(admin_client, user, api_response):
    resp = admin_client.get(f"/user/{user.id}")
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


@when("all users are retrieved", target_fixture="api_response")
def get_all_users(admin_client, api_response):
    resp = admin_client.get("/user/get-all-users")
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


@when(
    parsers.parse('the user name is updated to "{name}"'),
    target_fixture="api_response",
)
def update_user_name(admin_client, user, name, api_response):
    data = {"name": name}
    resp = admin_client.post(f"/user/{user.id}", data=data)
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


@when("the user is archived", target_fixture="api_response")
def archive_user(admin_client, user, api_response):
    resp = admin_client.post(f"/user/{user.id}/archive")
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json() if resp.data else None
    return api_response


@when("users are searched by email", target_fixture="api_response")
def search_users_by_email(admin_client, user, api_response):
    data = {"email": user.email_address}
    resp = admin_client.post("/user/find-users-by-email", data=data)
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


@when(
    "the user's organizations and services are retrieved",
    target_fixture="api_response",
)
def get_user_orgs_and_services(admin_client, user, api_response):
    resp = admin_client.get(f"/user/{user.id}/organizations-and-services")
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


@when("the all users report is retrieved", target_fixture="api_response")
def get_all_users_report(admin_client, api_response):
    resp = admin_client.get("/user/report-all-users")
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


# -- Then steps --


@then("the response should contain the user details")
def response_has_user_details(api_response):
    data = api_response["json"]["data"]
    assert "id" in data
    assert "name" in data
