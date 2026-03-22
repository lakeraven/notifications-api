"""Step definitions for billing usage features."""

from datetime import datetime

from pytest_bdd import given, parsers, scenarios, then, when

from tests.app.db import create_annual_billing

scenarios("../features/billing/billing_usage.feature")


# -- Given steps --


@given("a free SMS fragment limit exists", target_fixture="annual_billing")
def free_sms_limit_exists(notify_db_session, service):
    year = datetime.utcnow().year
    return create_annual_billing(
        service_id=service.id,
        free_sms_fragment_limit=250000,
        financial_year_start=year,
    )


# -- When steps --


@when(
    "the monthly usage is retrieved for the current year",
    target_fixture="api_response",
)
def get_monthly_usage(admin_client, service, api_response):
    year = datetime.utcnow().year
    resp = admin_client.get(
        f"/service/{service.id}/billing/monthly-usage?year={year}"
    )
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


@when("the yearly usage summary is retrieved", target_fixture="api_response")
def get_yearly_usage(admin_client, service, api_response):
    year = datetime.utcnow().year
    resp = admin_client.get(
        f"/service/{service.id}/billing/yearly-usage-summary?year={year}"
    )
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


@when("the free SMS fragment limit is retrieved", target_fixture="api_response")
def get_free_sms_limit(admin_client, service, api_response):
    year = datetime.utcnow().year
    resp = admin_client.get(
        f"/service/{service.id}/billing/free-sms-fragment-limit?financial_year_start={year}"
    )
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


@when(
    parsers.parse("the free SMS fragment limit is set to {limit:d}"),
    target_fixture="api_response",
)
def set_free_sms_limit(admin_client, service, limit, api_response):
    year = datetime.utcnow().year
    data = {
        "free_sms_fragment_limit": limit,
        "financial_year_start": year,
    }
    resp = admin_client.post(
        f"/service/{service.id}/billing/free-sms-fragment-limit",
        data=data,
    )
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json() if resp.data else None
    return api_response
