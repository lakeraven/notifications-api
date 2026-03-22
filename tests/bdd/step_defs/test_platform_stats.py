"""Step definitions for platform statistics features."""

from datetime import datetime

from pytest_bdd import scenarios, when

scenarios("../features/platform/platform_stats.feature")


# -- When steps --


@when("the platform statistics are retrieved", target_fixture="api_response")
def get_platform_stats(admin_client, api_response):
    resp = admin_client.get("/platform-stats")
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


@when("usage for all services is retrieved", target_fixture="api_response")
def get_usage_for_all_services(admin_client, api_response):
    year = datetime.utcnow().year
    resp = admin_client.get(
        f"/platform-stats/usage-for-all-services?year={year}"
    )
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


@when("data for the billing report is retrieved", target_fixture="api_response")
def get_billing_report_data(admin_client, api_response):
    today = datetime.utcnow().strftime("%Y-%m-%d")
    resp = admin_client.get(
        f"/platform-stats/data-for-billing-report?start_date={today}&end_date={today}"
    )
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


@when("the daily volumes report is retrieved", target_fixture="api_response")
def get_daily_volumes_report(admin_client, api_response):
    today = datetime.utcnow().strftime("%Y-%m-%d")
    resp = admin_client.get(
        f"/platform-stats/daily-volumes-report?start_date={today}&end_date={today}"
    )
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


@when("volumes by service are retrieved", target_fixture="api_response")
def get_volumes_by_service(admin_client, api_response):
    today = datetime.utcnow().strftime("%Y-%m-%d")
    resp = admin_client.get(
        f"/platform-stats/volumes-by-service?start_date={today}&end_date={today}"
    )
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response
