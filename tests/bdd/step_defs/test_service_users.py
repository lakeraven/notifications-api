"""Step definitions for service users BDD tests."""

import json
import uuid

from pytest_bdd import given, parsers, scenarios, then, when

from app.dao.services_dao import dao_add_user_to_service
from tests.app.db import create_service, create_user

scenarios("../features/services/service_users.feature")


# -- Given steps --


@given("the service has 2 users", target_fixture="second_user")
def the_service_has_2_users(service, notify_db_session):
    user = create_user(email=f"second-{uuid.uuid4()}@digital.cabinet-office.gov.uk")
    dao_add_user_to_service(service, user)
    return user


# -- When steps --


@when("I list users for the service", target_fixture="api_response")
def list_service_users(admin_client, service):
    resp = admin_client.get(f"/service/{service.id}/users")
    return {"status_code": resp.status_code, "json": resp.json}


@when("I add the user to the service", target_fixture="api_response")
def add_user_to_service(admin_client, service, new_user):
    resp = admin_client.post(
        f"/service/{service.id}/users/{new_user.id}",
        data={
            "permissions": [{"permission": "manage_settings"}],
            "folder_permissions": [],
        },
    )
    return {"status_code": resp.status_code, "json": resp.json}


@when("I remove the second user from the service", target_fixture="api_response")
def remove_user_from_service(admin_client, service, second_user):
    resp = admin_client.delete(f"/service/{service.id}/users/{second_user.id}")
    return {"status_code": resp.status_code, "json": resp.json}


# -- Then steps --


@then("the response should contain at least 1 user")
def response_has_at_least_one_user(api_response):
    data = api_response["json"]["data"]
    assert isinstance(data, list)
    assert len(data) >= 1


@then(parsers.parse("the service should have {count:d} user"))
def service_should_have_n_users(admin_client, service, count):
    resp = admin_client.get(f"/service/{service.id}/users")
    data = resp.json["data"]
    assert len(data) == count
