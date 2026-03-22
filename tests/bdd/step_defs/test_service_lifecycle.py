"""Step definitions for service lifecycle features."""

import json
import uuid
from datetime import datetime

from pytest_bdd import parsers, scenarios, then, when

from app.enums import NotificationType

scenarios("../features/services/service_lifecycle.feature")


# -- When steps --


@when(
    parsers.parse('a new service "{name}" is created'),
    target_fixture="api_response",
)
def create_new_service(admin_client, admin_user, name, api_response):
    user_id = str(admin_user.id)
    data = {
        "name": name,
        "user_id": user_id,
        "message_limit": 1000,
        "total_message_limit": 100000,
        "restricted": False,
        "active": True,
        "email_from": name.lower().replace(" ", "."),
        "created_by": user_id,
        "service_type": "government",
    }
    resp = admin_client.post("/service", data=data)
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


@when("the service is retrieved by ID", target_fixture="api_response")
def get_service_by_id(admin_client, service, api_response):
    resp = admin_client.get(f"/service/{service.id}")
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


@when("all services are retrieved", target_fixture="api_response")
def get_all_services(admin_client, api_response):
    resp = admin_client.get("/service")
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


@when(
    parsers.parse('the service name is updated to "{name}"'),
    target_fixture="api_response",
)
def update_service_name(admin_client, service, name, api_response):
    data = {"name": name, "created_by": str(service.users[0].id)}
    resp = admin_client.post(f"/service/{service.id}", data=data)
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


@when("the service is archived", target_fixture="api_response")
def archive_service(admin_client, service, api_response):
    resp = admin_client.post(f"/service/{service.id}/archive")
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json() if resp.data else None
    return api_response


@when("the service is suspended", target_fixture="api_response")
def suspend_service(admin_client, service, api_response):
    resp = admin_client.post(f"/service/{service.id}/suspend")
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json() if resp.data else None
    return api_response


@when("the service is resumed", target_fixture="api_response")
def resume_service(admin_client, service, api_response):
    resp = admin_client.post(f"/service/{service.id}/resume")
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json() if resp.data else None
    return api_response


@when("the service history is retrieved", target_fixture="api_response")
def get_service_history(admin_client, service, api_response):
    resp = admin_client.get(f"/service/{service.id}/history")
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


@when("the service statistics are retrieved", target_fixture="api_response")
def get_service_statistics(admin_client, service, api_response):
    today = datetime.utcnow().strftime("%Y-%m-%d")
    resp = admin_client.get(f"/service/{service.id}/statistics?today_only=True")
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


@when("the service notification count is retrieved", target_fixture="api_response")
def get_service_notification_count(admin_client, service, api_response):
    resp = admin_client.get(f"/service/{service.id}/notification-count")
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


@when(
    parsers.parse('services are searched by name "{name}"'),
    target_fixture="api_response",
)
def search_services_by_name(admin_client, name, api_response):
    resp = admin_client.get(f"/service/find-services-by-name?name={name}")
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


@when("live services data is retrieved", target_fixture="api_response")
def get_live_services_data(admin_client, api_response):
    resp = admin_client.get("/service/live-services-data")
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


@when("monthly data by service is retrieved", target_fixture="api_response")
def get_monthly_data_by_service(admin_client, api_response):
    resp = admin_client.get("/service/monthly-data-by-service")
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


# -- Then steps --


@then("the response should contain the service details")
def response_has_service_details(api_response):
    data = api_response["json"]["data"]
    assert "id" in data
    assert "name" in data


@then(parsers.parse('the response should contain the service name "{name}"'))
def response_has_service_name(api_response, name):
    data = api_response["json"]["data"]
    assert data["name"] == name


@then("the response should contain a list of services")
def response_has_services_list(api_response):
    data = api_response["json"]["data"]
    assert isinstance(data, list)
    assert len(data) > 0


@then("the response should contain service history data")
def response_has_history(api_response):
    data = api_response["json"]["data"]
    assert isinstance(data, dict)
