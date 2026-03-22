"""Step definitions for provider details features."""

from pytest_bdd import scenarios, then, when

from app.dao.provider_details_dao import get_provider_details_by_notification_type
from app.enums import NotificationType

scenarios("../features/providers/provider_details.feature")


# -- When steps --


@when("all providers are retrieved", target_fixture="api_response")
def get_all_providers(admin_client, api_response):
    resp = admin_client.get("/provider-details")
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


@when("a provider is retrieved by ID", target_fixture="api_response")
def get_provider_by_id(admin_client, notify_db_session, api_response):
    providers = get_provider_details_by_notification_type(NotificationType.SMS)
    provider = providers[0]
    resp = admin_client.get(f"/provider-details/{provider.id}")
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    api_response["provider"] = provider
    return api_response


@when("the provider version history is retrieved", target_fixture="api_response")
def get_provider_versions(admin_client, notify_db_session, api_response):
    providers = get_provider_details_by_notification_type(NotificationType.SMS)
    provider = providers[0]
    resp = admin_client.get(f"/provider-details/{provider.id}/versions")
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


@when("a provider priority is updated", target_fixture="api_response")
def update_provider_priority(admin_client, admin_user, notify_db_session, api_response):
    providers = get_provider_details_by_notification_type(NotificationType.SMS)
    provider = providers[0]
    data = {
        "priority": provider.priority,
        "created_by": str(admin_user.id),
    }
    resp = admin_client.post(f"/provider-details/{provider.id}", data=data)
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


@when("a provider is set to inactive", target_fixture="api_response")
def set_provider_inactive(admin_client, admin_user, notify_db_session, api_response):
    providers = get_provider_details_by_notification_type(NotificationType.SMS)
    provider = providers[0]
    data = {
        "active": False,
        "created_by": str(admin_user.id),
    }
    resp = admin_client.post(f"/provider-details/{provider.id}", data=data)
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


# -- Then steps --


@then("the response should contain a list of providers")
def response_has_providers_list(api_response):
    data = api_response["json"]["provider_details"]
    assert isinstance(data, list)
    assert len(data) > 0


@then("the response should contain the provider details")
def response_has_provider_details(api_response):
    data = api_response["json"]["provider_details"]
    assert "id" in data
    assert "identifier" in data
