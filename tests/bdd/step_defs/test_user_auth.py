"""Step definitions for user authentication features."""

import json
import uuid

from pytest_bdd import given, scenarios, then, when

scenarios("../features/users/user_auth.feature")


# -- Given steps --


@given("an SMS verification code has been sent", target_fixture="sms_code")
def sms_code_sent(admin_client, user):
    admin_client.post(f"/user/{user.id}/sms-code")
    return "12345"


# -- When steps --


@when("the user's password is verified", target_fixture="api_response")
def verify_password(admin_client, user, api_response):
    data = {"password": "password"}
    resp = admin_client.post(f"/user/{user.id}/verify/password", data=data)
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json() if resp.data else None
    return api_response


@when("an incorrect password is verified", target_fixture="api_response")
def verify_wrong_password(admin_client, user, api_response):
    data = {"password": "wrong-password"}
    resp = admin_client.post(f"/user/{user.id}/verify/password", data=data)
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json() if resp.data else None
    return api_response


@when("an SMS verification code is requested", target_fixture="api_response")
def request_sms_code(admin_client, user, api_response):
    resp = admin_client.post(f"/user/{user.id}/sms-code")
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json() if resp.data else None
    return api_response


@when("an email verification code is requested", target_fixture="api_response")
def request_email_code(admin_client, user, api_response):
    resp = admin_client.post(f"/user/{user.id}/email-code")
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json() if resp.data else None
    return api_response


@when("the SMS code is verified", target_fixture="api_response")
def verify_sms_code(admin_client, user, sms_code, api_response):
    data = {"code_type": "sms", "code": sms_code}
    resp = admin_client.post(f"/user/{user.id}/verify/code", data=data)
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json() if resp.data else None
    return api_response


@when("a wrong SMS code is verified", target_fixture="api_response")
def verify_wrong_sms_code(admin_client, user, api_response):
    data = {"code_type": "sms", "code": "00000"}
    resp = admin_client.post(f"/user/{user.id}/verify/code", data=data)
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json() if resp.data else None
    return api_response


@when("the user's failed login count is reset", target_fixture="api_response")
def reset_failed_login_count(admin_client, user, api_response):
    resp = admin_client.post(f"/user/{user.id}/reset-failed-login-count")
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json() if resp.data else None
    return api_response


@when("the user is retrieved by email", target_fixture="api_response")
def get_user_by_email(admin_client, user, api_response):
    resp = admin_client.get(f"/user/email?email={user.email_address}")
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


@when("a nonexistent user is retrieved by email", target_fixture="api_response")
def get_nonexistent_user_by_email(admin_client, api_response):
    resp = admin_client.get("/user/email?email=nonexistent@example.gov.uk")
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json() if resp.data else None
    return api_response


@when("the user is activated", target_fixture="api_response")
def activate_user(admin_client, user, api_response):
    resp = admin_client.post(f"/user/{user.id}/activate")
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json() if resp.data else None
    return api_response


@when("the user is deactivated", target_fixture="api_response")
def deactivate_user(admin_client, user, api_response):
    resp = admin_client.post(f"/user/{user.id}/deactivate")
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json() if resp.data else None
    return api_response


@when("an email verification is sent", target_fixture="api_response")
def send_email_verification(admin_client, user, api_response):
    data = {"to": user.email_address}
    resp = admin_client.post(f"/user/{user.id}/email-verification", data=data)
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json() if resp.data else None
    return api_response
