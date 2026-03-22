"""Step definitions for user authentication features."""

from unittest.mock import patch, MagicMock

from pytest_bdd import given, scenarios, then, when

scenarios("../features/users/user_auth.feature")


# -- Given steps --


@given("an SMS verification code has been sent", target_fixture="sms_code")
def sms_code_sent(user, notify_db_session):
    from app.dao.users_dao import create_user_code
    from app.enums import CodeType

    code = "123456"
    create_user_code(user, code, CodeType.SMS)
    return code


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
    with patch("app.user.rest.create_2fa_code"):
        resp = admin_client.post(f"/user/{user.id}/sms-code", data={})
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json() if resp.data else None
    return api_response


@when("an email verification code is requested", target_fixture="api_response")
def request_email_code(admin_client, user, api_response):
    with patch("app.user.rest.create_2fa_code"):
        resp = admin_client.post(f"/user/{user.id}/email-code", data={})
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
def activate_user(admin_client, user, notify_db_session, api_response):
    # Set user to pending first so activate doesn't fail with "User already active"
    from app.dao.users_dao import save_user_attribute
    from app.enums import UserState

    save_user_attribute(user, update_dict={"state": UserState.PENDING})
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
    import uuid as _uuid
    from app.enums import TemplateType

    mock_template = MagicMock(
        id=_uuid.uuid4(),
        version=1,
        template_type=TemplateType.EMAIL,
        service=MagicMock(get_default_reply_to_email_address=MagicMock(return_value=None)),
    )
    mock_notification = MagicMock(id=_uuid.uuid4(), personalisation={})
    with patch("app.user.rest.dao_get_template_by_id", return_value=mock_template), \
         patch("app.user.rest.db.session.get", return_value=mock_template.service), \
         patch("app.user.rest.persist_notification", return_value=mock_notification), \
         patch("app.user.rest.redis_store"), \
         patch("app.user.rest.send_notification_to_queue"):
        data = {"to": user.email_address}
        resp = admin_client.post(f"/user/{user.id}/email-verification", data=data)
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json() if resp.data else None
    return api_response
