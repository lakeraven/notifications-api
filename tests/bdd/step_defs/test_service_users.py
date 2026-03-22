"""Step definitions for service user features."""

from pytest_bdd import given, scenarios, then, when

from app.enums import PermissionType

scenarios("../features/services/service_users.feature")


# -- When steps --


@when("the service users are retrieved", target_fixture="api_response")
def get_service_users(admin_client, service, api_response):
    resp = admin_client.get(f"/service/{service.id}/users")
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


@given("the user is added to the service", target_fixture="api_response")
@when("the user is added to the service", target_fixture="api_response")
def add_user_to_service(admin_client, service, new_user, api_response):
    data = {
        "permissions": [
            {"permission": PermissionType.MANAGE_SETTINGS},
            {"permission": PermissionType.SEND_EMAILS},
            {"permission": PermissionType.SEND_TEXTS},
        ],
        "folder_permissions": [],
    }
    resp = admin_client.post(
        f"/service/{service.id}/users/{new_user.id}",
        data=data,
    )
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json() if resp.data else None
    return api_response


@when("the user is removed from the service", target_fixture="api_response")
def remove_user_from_service(admin_client, service, new_user, api_response):
    resp = admin_client.delete(f"/service/{service.id}/users/{new_user.id}")
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json() if resp.data else None
    return api_response


# -- Then steps --


@then("the response should contain a list of users")
def response_has_users_list(api_response):
    data = api_response["json"]["data"]
    assert isinstance(data, list)
    assert len(data) > 0
