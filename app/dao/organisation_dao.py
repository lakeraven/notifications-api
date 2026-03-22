# GOV.UK spelling alias — re-exports from organization_dao
from app.dao.organization_dao import *  # noqa: F401,F403
from app.dao.organization_dao import (
    dao_add_service_to_organization as dao_add_service_to_organisation,
    dao_create_organization as dao_create_organisation,
)


def dao_add_user_to_organisation(organisation_id, user_id):
    from app.dao.organization_dao import dao_add_user_to_organization

    return dao_add_user_to_organization(organisation_id, user_id)
