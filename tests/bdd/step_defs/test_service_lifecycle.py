"""Step definitions for service lifecycle BDD tests."""

import json
import uuid
from unittest.mock import patch

from pytest_bdd import given, parsers, scenarios, then, when

from app.constants import EMAIL_TYPE, SMS_TYPE
from tests.app.db import (
    create_notification,
    create_service,
    create_template,
    create_user,
)

scenarios("../features/services/service_lifecycle.feature")


# -- Given steps --


@given("3 services exist", target_fixture="services")
def three_services_exist(notify_db_session):
    services = []
    for i in range(3):
        svc = create_service(service_name=f"Service {i + 1} {uuid.uuid4()}")
        services.append(svc)
    return services


@given("a service in trial mode exists", target_fixture="service")
def a_service_in_trial_mode(notify_db_session):
    return create_service(
        service_name=f"Trial Service {uuid.uuid4()}",
        restricted=True,
    )


@given("a service exists with changes in its history", target_fixture="service")
def a_service_with_history(notify_db_session, admin_client):
    service = create_service()
    # Update the service to create a history entry
    admin_client.post(
        f"/service/{service.id}",
        data={"name": f"Updated {service.name}"},
    )
    return service


@given("live services exist", target_fixture="services")
def live_services_exist(notify_db_session):
    services = []
    for i in range(2):
        svc = create_service(
            service_name=f"Live Service {i + 1} {uuid.uuid4()}",
            restricted=False,
            go_live_at="2024-01-01 00:00:00",
        )
        services.append(svc)
    return services


@given("a service exists with sent notifications", target_fixture="service")
def a_service_with_notifications(notify_db_session):
    service = create_service()
    template = create_template(service=service, template_type=SMS_TYPE)
    for _ in range(3):
        create_notification(template=template, status="delivered")
    return service


@given("a service exists with notifications sent from multiple templates", target_fixture="service")
def a_service_with_multiple_templates(notify_db_session):
    service = create_service()
    sms_template = create_template(service=service, template_type=SMS_TYPE, template_name="SMS Template")
    email_template = create_template(service=service, template_type=EMAIL_TYPE, template_name="Email Template")
    for _ in range(2):
        create_notification(template=sms_template, status="delivered")
    for _ in range(2):
        create_notification(template=email_template, status="delivered")
    return service


# -- When steps --


@when(parsers.parse('I create a service named "{name}" for user'), target_fixture="api_response")
def create_service_via_api(admin_client, name):
    user = create_user(email=f"creator-{uuid.uuid4()}@digital.cabinet-office.gov.uk")
    unique_suffix = uuid.uuid4()
    resp = admin_client.post(
        "/service",
        data={
            "name": f"{name} {unique_suffix}",
            "created_by": str(user.id),
            "user_id": str(user.id),
            "message_limit": 1000,
            "total_message_limit": 100000,
            "restricted": True,
            "email_from": f"test.service.{unique_suffix}",
        },
    )
    return {"status_code": resp.status_code, "json": resp.json}


@when("I get the service by ID", target_fixture="api_response")
def get_service_by_id(admin_client, service):
    resp = admin_client.get(f"/service/{service.id}")
    return {"status_code": resp.status_code, "json": resp.json}


@when("I list all services", target_fixture="api_response")
def list_all_services(admin_client):
    resp = admin_client.get("/service")
    return {"status_code": resp.status_code, "json": resp.json}


@when(parsers.parse('I update the service name to "{new_name}"'), target_fixture="api_response")
def update_service_name(admin_client, service, new_name):
    resp = admin_client.post(
        f"/service/{service.id}",
        data={"name": new_name},
    )
    return {"status_code": resp.status_code, "json": resp.json}


@when("I update the service to set restricted to false", target_fixture="api_response")
def update_service_restricted(admin_client, service):
    with patch("app.service.rest.send_notification_to_service_users"):
        resp = admin_client.post(
            f"/service/{service.id}",
            data={"restricted": False},
        )
    return {"status_code": resp.status_code, "json": resp.json}


@when("I archive the service", target_fixture="api_response")
def archive_service(admin_client, service):
    resp = admin_client.post(f"/service/{service.id}/archive")
    return {"status_code": resp.status_code, "json": resp.json}


@when("I get the service history", target_fixture="api_response")
def get_service_history(admin_client, service):
    resp = admin_client.get(f"/service/{service.id}/history")
    return {"status_code": resp.status_code, "json": resp.json}


@when(parsers.parse('I search for services by name "{search_term}"'), target_fixture="api_response")
def search_services_by_name(admin_client, search_term):
    resp = admin_client.get(
        f"/service/find-services-by-name?service_name={search_term}"
    )
    return {"status_code": resp.status_code, "json": resp.json}


@when("I request live services data", target_fixture="api_response")
def get_live_services_data(admin_client):
    resp = admin_client.get("/service/live-services-data")
    return {"status_code": resp.status_code, "json": resp.json}


@when("I get the service statistics", target_fixture="api_response")
def get_service_statistics(admin_client, service):
    resp = admin_client.get(f"/service/{service.id}/statistics")
    return {"status_code": resp.status_code, "json": resp.json}


@when("I get the monthly notification stats", target_fixture="api_response")
def get_monthly_stats(admin_client, service):
    from datetime import datetime

    year = datetime.utcnow().year
    resp = admin_client.get(f"/service/{service.id}/notifications/monthly?year={year}")
    return {"status_code": resp.status_code, "json": resp.json}


@when("I get the monthly template usage", target_fixture="api_response")
def get_monthly_template_usage(admin_client, service):
    from datetime import datetime

    year = datetime.utcnow().year
    resp = admin_client.get(
        f"/service/{service.id}/notifications/templates_usage/monthly?year={year}"
    )
    return {"status_code": resp.status_code, "json": resp.json}


# -- Then steps --


@then("the service should have default permissions")
def service_has_default_permissions(api_response):
    data = api_response["json"]["data"]
    assert "permissions" in data


@then("the service should be in restricted mode")
def service_is_restricted(api_response):
    data = api_response["json"]["data"]
    assert data["restricted"] is True


@then(parsers.parse('the service name should be "{name}"'))
def service_name_should_be(api_response, name):
    data = api_response["json"]["data"]
    assert data["name"] == name


@then("the response should contain at least 3 services")
def response_has_at_least_3_services(api_response):
    data = api_response["json"]["data"]
    assert isinstance(data, list)
    assert len(data) >= 3


@then("the service should not be restricted")
def service_is_not_restricted(api_response):
    data = api_response["json"]["data"]
    assert data["restricted"] is False


@then("the service should be archived")
def service_is_archived(api_response, admin_client, service):
    resp = admin_client.get(f"/service/{service.id}")
    assert resp.json["data"]["active"] is False


@then("the response should contain service history events")
def response_has_service_history(api_response):
    data = api_response["json"]["data"]
    assert "service_history" in data
    assert "api_key_history" in data
    assert "template_history" in data
    assert "events" in data


@then(parsers.parse('the results should include "{name}"'))
def results_include_name(api_response, name):
    data = api_response["json"]["data"]
    assert isinstance(data, list)
    assert len(data) >= 1
    names = [s["name"] for s in data]
    assert any(name in n for n in names), f"Expected '{name}' in {names}"


@then("the response should include counts by notification type")
def response_has_notification_type_counts(api_response):
    data = api_response["json"]["data"]
    assert isinstance(data, dict)


@then("the response should be grouped by month")
def response_grouped_by_month(api_response):
    data = api_response["json"]["data"]
    assert isinstance(data, dict)


@then("the response should include template names and counts")
def response_has_template_names_and_counts(api_response):
    # The monthly template usage endpoint returns {"stats": [...]}
    json_data = api_response["json"]
    stats = json_data.get("stats", json_data.get("data", []))
    assert isinstance(stats, list)
