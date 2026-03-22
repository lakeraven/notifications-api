"""Step definitions for complaint features."""

from pytest_bdd import given, scenarios, then, when

from tests.app.db import create_complaint

scenarios("../features/other/complaints.feature")


# -- Given steps --


@given("a complaint exists", target_fixture="complaint")
def complaint_exists(notify_db_session):
    return create_complaint()


# -- When steps --


@when("all complaints are retrieved", target_fixture="api_response")
def get_all_complaints(admin_client, api_response):
    resp = admin_client.get("/complaint")
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


@when("the complaint count is retrieved for today", target_fixture="api_response")
def get_complaint_count(admin_client, api_response):
    resp = admin_client.get("/complaint/count-by-date-range")
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


# -- Then steps --


@then("the response should contain a list of complaints")
def response_has_complaints_list(api_response):
    data = api_response["json"]
    assert "complaints" in data
    assert isinstance(data["complaints"], list)
    assert len(data["complaints"]) > 0
