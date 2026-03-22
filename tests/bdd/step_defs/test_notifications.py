"""Step definitions for service notification features."""

from datetime import datetime

from pytest_bdd import given, scenarios, then, when

from app.enums import NotificationType, TemplateType
from tests.app.db import create_notification, create_template

scenarios("../features/services/notifications.feature")


# -- Given steps --


@given("the service has sent notifications", target_fixture="notifications")
def service_has_notifications(notify_db_session, service):
    template = create_template(service=service, template_type=TemplateType.EMAIL)
    notifications = [
        create_notification(template=template),
        create_notification(template=template),
    ]
    return notifications


@given("the service has sent a notification", target_fixture="notification")
def service_has_notification(notify_db_session, service):
    template = create_template(service=service, template_type=TemplateType.EMAIL)
    return create_notification(template=template)


# -- When steps --


@when("the service notifications are retrieved", target_fixture="api_response")
def get_service_notifications(admin_client, service, api_response):
    resp = admin_client.get(f"/service/{service.id}/notifications")
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


@when("the notification is retrieved by ID", target_fixture="api_response")
def get_notification_by_id(admin_client, service, notification, api_response):
    resp = admin_client.get(
        f"/service/{service.id}/notifications/{notification.id}"
    )
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


@when("the monthly notification stats are retrieved", target_fixture="api_response")
def get_monthly_stats(admin_client, service, api_response):
    year = datetime.utcnow().year
    resp = admin_client.get(f"/service/{service.id}/notifications/monthly?year={year}")
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


@when(
    "notification statistics are retrieved for today",
    target_fixture="api_response",
)
def get_notification_stats_today(admin_client, service, api_response):
    resp = admin_client.get(f"/service/{service.id}/statistics?today_only=True")
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response


# -- Then steps --


@then("the response should contain a list of notifications")
def response_has_notifications_list(api_response):
    data = api_response["json"]
    assert "notifications" in data
    assert isinstance(data["notifications"], list)
    assert len(data["notifications"]) > 0


@then("the response should contain an empty notifications list")
def response_has_empty_notifications(api_response):
    data = api_response["json"]
    assert "notifications" in data
    assert isinstance(data["notifications"], list)
    assert len(data["notifications"]) == 0
