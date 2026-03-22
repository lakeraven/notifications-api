"""Step definitions for template CRUD features."""

import uuid

from pytest_bdd import given, parsers, scenarios, then, when

from app.enums import TemplateType
from tests.app.db import create_template

scenarios("../features/templates/template_crud.feature")


# -- Given steps --


@given(
    parsers.parse('an "{template_type}" template exists'),
    target_fixture="template",
)
def template_exists(notify_db_session, service, template_type):
    tt = TemplateType(template_type)
    return create_template(
        service=service,
        template_type=tt,
        template_name=f"Test {template_type} template",
    )


# -- When steps --


@when(
    parsers.parse('an "{template_type}" template is created with name "{name}"'),
    target_fixture="api_response",
)
def create_template_step(admin_client, service, template_type, name, api_response):
    data = {
        "name": name,
        "template_type": template_type,
        "content": "Hello ((name)), this is a test.",
        "service": str(service.id),
        "created_by": str(service.users[0].id),
    }
    if template_type == "email":
        data["subject"] = "Test subject"
    resp = admin_client.post(
        f"/service/{service.id}/template",
        data=data,
    )
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


@when("the template is retrieved by ID", target_fixture="api_response")
def get_template_by_id(admin_client, service, template, api_response):
    resp = admin_client.get(
        f"/service/{service.id}/template/{template.id}"
    )
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


@when("all templates are retrieved for the service", target_fixture="api_response")
def get_all_templates(admin_client, service, api_response):
    resp = admin_client.get(f"/service/{service.id}/template")
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


@when(
    parsers.parse('the template name is updated to "{name}"'),
    target_fixture="api_response",
)
def update_template_name(admin_client, service, template, name, api_response):
    data = {
        "name": name,
        "content": template.content,
        "created_by": str(service.users[0].id),
    }
    if template.template_type != TemplateType.SMS:
        data["subject"] = template.subject
    resp = admin_client.post(
        f"/service/{service.id}/template/{template.id}",
        data=data,
    )
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


@when(
    parsers.parse("the template version {version:d} is retrieved"),
    target_fixture="api_response",
)
def get_template_version(admin_client, service, template, version, api_response):
    resp = admin_client.get(
        f"/service/{service.id}/template/{template.id}/version/{version}"
    )
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


@when("all template versions are retrieved", target_fixture="api_response")
def get_all_template_versions(admin_client, service, template, api_response):
    resp = admin_client.get(
        f"/service/{service.id}/template/{template.id}/versions"
    )
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


@when("the template preview is requested", target_fixture="api_response")
def get_template_preview(admin_client, service, template, api_response):
    resp = admin_client.get(
        f"/service/{service.id}/template/{template.id}/preview"
    )
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


@when(
    'an "email" template is created with personalisation',
    target_fixture="api_response",
)
def create_template_with_personalisation(admin_client, service, api_response):
    data = {
        "name": "Personalised template",
        "template_type": "email",
        "content": "Hello ((name)), your ref is ((reference)).",
        "subject": "Your update ((name))",
        "service": str(service.id),
        "created_by": str(service.users[0].id),
    }
    resp = admin_client.post(
        f"/service/{service.id}/template",
        data=data,
    )
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


@when("the template content is updated", target_fixture="api_response")
def update_template_content(admin_client, service, template, api_response):
    data = {
        "name": template.name,
        "content": "Updated content for the template.",
        "created_by": str(service.users[0].id),
    }
    if template.template_type != TemplateType.SMS:
        data["subject"] = template.subject
    resp = admin_client.post(
        f"/service/{service.id}/template/{template.id}",
        data=data,
    )
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


@when(
    parsers.parse('a template is created with invalid type "{template_type}"'),
    target_fixture="api_response",
)
def create_template_invalid_type(admin_client, service, template_type, api_response):
    data = {
        "name": "Bad template",
        "template_type": template_type,
        "content": "Hello.",
        "service": str(service.id),
        "created_by": str(service.users[0].id),
    }
    resp = admin_client.post(
        f"/service/{service.id}/template",
        data=data,
    )
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


@when("a template is created with an empty name", target_fixture="api_response")
def create_template_empty_name(admin_client, service, api_response):
    data = {
        "name": "",
        "template_type": "email",
        "content": "Hello.",
        "subject": "Test",
        "service": str(service.id),
        "created_by": str(service.users[0].id),
    }
    resp = admin_client.post(
        f"/service/{service.id}/template",
        data=data,
    )
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


# -- Then steps --


@then("the response should contain the template details")
def response_has_template_details(api_response):
    data = api_response["json"]["data"]
    assert "id" in data
    assert "name" in data


@then("the response should contain a list of templates")
def response_has_templates_list(api_response):
    data = api_response["json"]["data"]
    assert isinstance(data, list)
    assert len(data) > 0


@then(parsers.parse('the response should contain the template name "{name}"'))
def response_has_template_name(api_response, name):
    data = api_response["json"]["data"]
    assert data["name"] == name


@then("the response should contain the template body")
def response_has_template_body(api_response):
    data = api_response["json"]
    assert "body" in data or "content" in data.get("data", data)
