"""Step definitions for organization lifecycle features."""

import uuid

from pytest_bdd import given, parsers, scenarios, then, when

from tests.app.db import create_organization, create_service

scenarios("../features/organizations/organization_lifecycle.feature")


# -- Given steps --


@given(
    parsers.parse('an organization "{name}" exists'),
    target_fixture="organization",
)
def organization_exists(notify_db_session, name):
    return create_organization(name=name)


@given(
    parsers.parse('an organization "{name}" exists with domain "{domain}"'),
    target_fixture="organization",
)
def organization_with_domain_exists(notify_db_session, name, domain):
    return create_organization(name=name, domains=[domain])


@given("a service belongs to the organization", target_fixture="org_service")
def service_belongs_to_org(notify_db_session, organization):
    return create_service(
        service_name="Org Service",
        organization=organization,
    )


# -- When steps --


@when(
    parsers.parse('a new organization "{name}" is created'),
    target_fixture="api_response",
)
def create_new_organization(admin_client, api_response, name):
    data = {"name": name, "active": True, "organization_type": "federal"}
    resp = admin_client.post("/organizations", data=data)
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


@when("the organization is retrieved by ID", target_fixture="api_response")
def get_organization_by_id(admin_client, organization, api_response):
    resp = admin_client.get(f"/organizations/{organization.id}")
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


@when("all organizations are retrieved", target_fixture="api_response")
def get_all_organizations(admin_client, api_response):
    resp = admin_client.get("/organizations")
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


@when(
    parsers.parse('the organization name is updated to "{name}"'),
    target_fixture="api_response",
)
def update_organization_name(admin_client, organization, name, api_response):
    data = {"name": name}
    resp = admin_client.post(f"/organizations/{organization.id}", data=data)
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json() if resp.data else None
    return api_response


@when("the organization's services are retrieved", target_fixture="api_response")
def get_org_services(admin_client, organization, api_response):
    resp = admin_client.get(f"/organizations/{organization.id}/services")
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


@when("the service is linked to the organization", target_fixture="api_response")
def link_service_to_org(admin_client, organization, service, api_response):
    data = {"service_id": str(service.id)}
    resp = admin_client.post(
        f"/organizations/{organization.id}/service",
        data=data,
    )
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json() if resp.data else None
    return api_response


@when(
    parsers.parse('an organization is looked up by domain "{domain}"'),
    target_fixture="api_response",
)
def lookup_org_by_domain(admin_client, api_response, domain):
    resp = admin_client.get(f"/organizations/by-domain?domain={domain}")
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


# -- Then steps --


@then("the response should contain the organization details")
def response_has_org_details(api_response):
    data = api_response["json"]
    assert "id" in data or "name" in data


@then(parsers.parse('the response should contain the organization name "{name}"'))
def response_has_org_name(api_response, name):
    data = api_response["json"]
    assert data["name"] == name


@then("the response should contain a list of organizations")
def response_has_org_list(api_response):
    data = api_response["json"]
    assert isinstance(data, list)
    assert len(data) > 0
