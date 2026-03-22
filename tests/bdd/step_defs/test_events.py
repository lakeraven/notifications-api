"""Step definitions for events features."""

import uuid

from pytest_bdd import parsers, scenarios, when

scenarios("../features/other/events.feature")


@when(
    parsers.parse('an event is created with type "{event_type}"'),
    target_fixture="api_response",
)
def create_event(admin_client, api_response, event_type):
    data = {
        "event_type": event_type,
        "data": {"ip_address": "0.0.0.0", "browser_fingerprint": {}},
    }
    resp = admin_client.post("/events", data=data)
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json()
    return api_response
