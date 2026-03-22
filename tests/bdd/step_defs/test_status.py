"""Step definitions for platform status features."""

from pytest_bdd import parsers, scenarios, when

scenarios("../features/other/status.feature")


@when(
    parsers.parse('a GET request is made to "{path}"'),
    target_fixture="api_response",
)
def get_request_to(client, path, api_response, notify_db_session):
    resp = client.get(path)
    api_response["status_code"] = resp.status_code
    api_response["json"] = resp.get_json() if resp.data else None
    return api_response
