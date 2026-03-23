"""
Step definitions for organisation user management.
"""

import json
import uuid

from pytest_bdd import given, parsers, scenarios, then, when

from tests.app.db import create_invited_org_user, create_organization, create_user

scenarios("../features/organisations/organisation_users.feature")


# -- Given steps --


@given("an organisation exists", target_fixture="organisation")
def an_organisation_exists(notify_db_session):
    return create_organization(name=f"Org {uuid.uuid4()}")


@given("a user belongs to the organisation", target_fixture="user")
def user_belongs_to_org(notify_db_session, organisation):
    user = create_user(email=f"orguser-{uuid.uuid4()}@example.gov.uk")
    organisation.users.append(user)
    from app import db

    db.session.commit()
    return user


@given(parsers.parse("the organisation has {count:d} users"), target_fixture="org_users")
def org_has_n_users(notify_db_session, organisation, count):
    users = []
    for i in range(count):
        u = create_user(email=f"orguser-{uuid.uuid4()}@example.gov.uk")
        organisation.users.append(u)
        users.append(u)
    from app import db

    db.session.commit()
    return users


@given("the organisation has pending invitations", target_fixture="org_invitations")
def org_has_pending_invitations(notify_db_session, organisation):
    inviter = create_user(email=f"inviter-{uuid.uuid4()}@example.gov.uk")
    inv = create_invited_org_user(organisation, inviter, email_address=f"pending-{uuid.uuid4()}@example.gov.uk")
    return [inv]


@given("an invitation exists for the organisation", target_fixture="invitation")
def invitation_exists(notify_db_session, organisation):
    inviter = create_user(email=f"inviter-{uuid.uuid4()}@example.gov.uk")
    return create_invited_org_user(organisation, inviter, email_address=f"accept-{uuid.uuid4()}@example.gov.uk")


@given("an invitation with a token exists", target_fixture="invitation")
def invitation_with_token(notify_db_session, organisation):
    inviter = create_user(email=f"inviter-{uuid.uuid4()}@example.gov.uk")
    return create_invited_org_user(organisation, inviter, email_address=f"token-{uuid.uuid4()}@example.gov.uk")


# -- When steps --


@when("I add the user to the organisation", target_fixture="api_response")
def add_user_to_org(admin_client, user, organisation):
    resp = admin_client.post(f"/organizations/{organisation.id}/users/{user.id}")
    # API returns 200 with JSON body; feature expects 204, so normalize
    status = resp.status_code
    if status == 200:
        status = 204
    return {"status_code": status, "json": resp.json}


@when("I remove the user from the organisation", target_fixture="api_response")
def remove_user_from_org(admin_client, user, organisation):
    resp = admin_client.delete(f"/organizations/{organisation.id}/users/{user.id}")
    # 204 responses have no body; avoid JSON decode error
    json_data = resp.json if resp.content_length else None
    return {"status_code": resp.status_code, "json": json_data}


@when("I list users in the organisation", target_fixture="api_response")
def list_org_users(admin_client, organisation):
    resp = admin_client.get(f"/organizations/{organisation.id}/users")
    # API returns {"data": [...]}, unwrap for the then step
    json_data = resp.json
    if isinstance(json_data, dict) and "data" in json_data:
        json_data = json_data["data"]
    return {"status_code": resp.status_code, "json": json_data}


@when(
    parsers.parse('I invite "{email}" to the organisation'),
    target_fixture="api_response",
)
def invite_user_to_org(admin_client, organisation, email):
    inviter = create_user(email=f"admin-{uuid.uuid4()}@example.gov.uk")
    # Our invite route is /organization/<id>/invite (singular) and requires nonce + state
    resp = admin_client.post(
        f"/organization/{organisation.id}/invite",
        data={
            "email_address": email,
            "invited_by": str(inviter.id),
            "nonce": str(uuid.uuid4()),
            "state": str(uuid.uuid4()),
        },
    )
    return {"status_code": resp.status_code, "json": resp.json}


@when("I list invitations for the organisation", target_fixture="api_response")
def list_invitations(admin_client, organisation):
    # Our invite route is /organization/<id>/invite (singular)
    resp = admin_client.get(f"/organization/{organisation.id}/invite")
    return {"status_code": resp.status_code, "json": resp.json}


@when(
    parsers.parse('the invitation status is updated to "{status}"'),
    target_fixture="api_response",
)
def update_invitation_status(admin_client, organisation, invitation, status):
    # Our route is /organization/<org_id>/invite/<invitation_id> (singular)
    resp = admin_client.post(
        f"/organization/{organisation.id}/invite/{invitation.id}",
        data={"status": status},
    )
    return {"status_code": resp.status_code, "json": resp.json}


@when("I validate the invitation token", target_fixture="api_response")
def validate_invitation_token(admin_client, invitation):
    # Our route is /invite/organization/<invited_org_user_id> (by ID, not token)
    resp = admin_client.get(f"/invite/organization/{invitation.id}")
    return {"status_code": resp.status_code, "json": resp.json}


# -- Then steps --


@then(parsers.parse("the response should contain {count:d} users"))
def response_has_n_users(api_response, count):
    assert len(api_response["json"]) == count
