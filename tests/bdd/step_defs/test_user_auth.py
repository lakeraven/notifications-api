"""
Step definitions for user authentication flows.

Tests run against the Flask test client using existing test fixtures.
"""

import json
import uuid
from unittest.mock import MagicMock

from pytest_bdd import given, parsers, scenarios, then, when

from app.constants import EMAIL_TYPE, SMS_TYPE
from app.dao.users_dao import create_secret_code, create_user_code
from tests.app.db import (
    create_user,
    create_webauthn_credential,
)

# Load all scenarios from the feature file
scenarios("../features/users/user_auth.feature")


def _safe_response(resp):
    """Build an api_response dict, handling empty bodies (e.g. 204 No Content)."""
    return {
        "status_code": resp.status_code,
        "json": resp.get_json(silent=True),
    }


# -- Given steps --


@given("an active user exists with a password", target_fixture="user")
def active_user_with_password(notify_db_session):
    return create_user(
        email=f"authuser-{uuid.uuid4()}@example.gov.uk",
        state="active",
    )


@given("the user has a pending 2FA code", target_fixture="verify_code")
def user_has_pending_2fa(user, notify_db_session):
    code = create_secret_code()
    create_user_code(user, code, SMS_TYPE)
    return code


@given("the user has failed login attempts")
def user_has_failed_logins(user, notify_db_session):
    user.failed_login_count = 3
    from app.dao.users_dao import save_model_user

    save_model_user(user)


@given("the user has a WebAuthn credential", target_fixture="webauthn_cred")
def user_has_webauthn(user, notify_db_session):
    return create_webauthn_credential(user, name="test-key")


@given("a pending user exists", target_fixture="pending_user")
def a_pending_user(notify_db_session):
    return create_user(
        email=f"pending-{uuid.uuid4()}@example.gov.uk",
        state="pending",
    )


# -- When steps --


@when("I verify the user's password", target_fixture="api_response")
def verify_correct_password(admin_client, user):
    data = {"password": "password"}
    resp = admin_client.post(f"/user/{user.id}/verify/password", data=data)
    return _safe_response(resp)


@when("I verify an incorrect password", target_fixture="api_response")
def verify_incorrect_password(admin_client, user):
    data = {"password": "wrong-password-123"}
    resp = admin_client.post(f"/user/{user.id}/verify/password", data=data)
    return _safe_response(resp)


@when("I request an SMS 2FA code for the user", target_fixture="api_response")
def request_sms_2fa(admin_client, user, mocker):
    mocker.patch("app.celery.provider_tasks.deliver_sms.apply_async")
    mocker.patch("app.user.rest.create_2fa_code")
    data = {}
    resp = admin_client.post(f"/user/{user.id}/sms-code", data=data)
    return _safe_response(resp)


@when("I request an email 2FA code for the user", target_fixture="api_response")
def request_email_2fa(admin_client, user, mocker):
    mocker.patch("app.celery.provider_tasks.deliver_email.apply_async")
    mocker.patch("app.user.rest.create_2fa_code")
    data = {}
    resp = admin_client.post(f"/user/{user.id}/email-code", data=data)
    return _safe_response(resp)


@when("I verify the correct 2FA code", target_fixture="api_response")
def verify_correct_2fa(admin_client, user, verify_code):
    data = {
        "code": verify_code,
        "code_type": SMS_TYPE,
    }
    resp = admin_client.post(f"/user/{user.id}/verify/code", data=data)
    return _safe_response(resp)


@when("I verify an incorrect 2FA code", target_fixture="api_response")
def verify_incorrect_2fa(admin_client, user, verify_code):
    data = {
        "code": "000000",
        "code_type": SMS_TYPE,
    }
    resp = admin_client.post(f"/user/{user.id}/verify/code", data=data)
    return _safe_response(resp)


@when("I reset the failed login count", target_fixture="api_response")
def reset_failed_login_count(admin_client, user):
    resp = admin_client.post(f"/user/{user.id}/reset-failed-login-count", data={})
    return _safe_response(resp)


@when("I complete the WebAuthn login flow", target_fixture="api_response")
def complete_webauthn_login(admin_client, user, webauthn_cred):
    data = {
        "successful": True,
    }
    resp = admin_client.post(f"/user/{user.id}/complete/webauthn-login", data=data)
    return _safe_response(resp)


@when("I request a password reset for the user", target_fixture="api_response")
def request_password_reset(admin_client, user, mocker):
    mocker.patch("app.celery.provider_tasks.deliver_email.apply_async")
    data = {"email": user.email_address}
    resp = admin_client.post("/user/reset-password", data=data)
    return _safe_response(resp)


@when("I update the user's password", target_fixture="api_response")
def update_password(admin_client, user):
    data = {"_password": "NewValidPassword456!"}
    resp = admin_client.post(f"/user/{user.id}/update-password", data=data)
    return _safe_response(resp)


@when("I send the email verification", target_fixture="api_response")
def send_email_verification(admin_client, pending_user, mocker):
    mocker.patch("app.celery.provider_tasks.deliver_email.apply_async")
    mocker.patch("app.user.rest.persist_notification")
    mocker.patch("app.user.rest.send_notification_to_queue")
    mocker.patch("app.user.rest.redis_store")
    mock_template = MagicMock()
    mock_template.template_type = "email"
    mocker.patch("app.user.rest.dao_get_template_by_id", return_value=mock_template)
    mock_service = MagicMock()
    mock_service.get_default_reply_to_email_address.return_value = None
    mocker.patch("app.user.rest.db.session.get", return_value=mock_service)
    data = {}
    resp = admin_client.post(f"/user/{pending_user.id}/email-verification", data=data)
    return _safe_response(resp)


@when(
    parsers.parse('I send a change email verification to "{email}"'),
    target_fixture="api_response",
)
def send_change_email_verification(admin_client, user, email, mocker):
    mocker.patch("app.celery.provider_tasks.deliver_email.apply_async")
    mocker.patch("app.user.rest.persist_notification")
    mocker.patch("app.user.rest.send_notification_to_queue")
    mocker.patch("app.user.rest.redis_store")
    mock_template = MagicMock()
    mock_template.template_type = "email"
    mocker.patch("app.user.rest.dao_get_template_by_id", return_value=mock_template)
    mock_service = MagicMock()
    mock_service.get_default_reply_to_email_address.return_value = None
    mocker.patch("app.user.rest.db.session.get", return_value=mock_service)
    data = {"email": email}
    resp = admin_client.post(f"/user/{user.id}/change-email-verification", data=data)
    return _safe_response(resp)
