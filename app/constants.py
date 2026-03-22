# GOV.UK-compatible constants.
# Maps flat constant names to our StrEnum values for convergence.
# Over time, we can migrate callers to use these directly and retire enums.py.

import enum

from app.enums import (
    AuthType,
    BrandType,
    CallbackType,
    CodeType,
    InvitedUserStatus,
    JobStatus,
    KeyType,
    NotificationStatus,
    NotificationType,
    OrganizationType,
    PermissionType,
    ServicePermissionType,
    TemplateProcessType,
    TemplateType,
)

# -- Notification statuses --

NOTIFICATION_CANCELLED = NotificationStatus.CANCELLED
NOTIFICATION_CREATED = NotificationStatus.CREATED
NOTIFICATION_SENDING = NotificationStatus.SENDING
NOTIFICATION_SENT = NotificationStatus.SENT
NOTIFICATION_DELIVERED = NotificationStatus.DELIVERED
NOTIFICATION_PENDING = NotificationStatus.PENDING
NOTIFICATION_FAILED = NotificationStatus.FAILED
NOTIFICATION_TECHNICAL_FAILURE = NotificationStatus.TECHNICAL_FAILURE
NOTIFICATION_TEMPORARY_FAILURE = NotificationStatus.TEMPORARY_FAILURE
NOTIFICATION_PERMANENT_FAILURE = NotificationStatus.PERMANENT_FAILURE
NOTIFICATION_PENDING_VIRUS_CHECK = NotificationStatus.PENDING_VIRUS_CHECK
NOTIFICATION_VALIDATION_FAILED = NotificationStatus.VALIDATION_FAILED
NOTIFICATION_VIRUS_SCAN_FAILED = NotificationStatus.VIRUS_SCAN_FAILED

NOTIFICATION_STATUS_TYPES_FAILED = list(NotificationStatus.failed_types())
NOTIFICATION_STATUS_TYPES_COMPLETED = list(NotificationStatus.completed_types())
NOTIFICATION_STATUS_SUCCESS = list(NotificationStatus.success_types())
NOTIFICATION_STATUS_TYPES_BILLABLE = list(NotificationStatus.billable_types())
NOTIFICATION_STATUS_TYPES_BILLABLE_SMS = list(NotificationStatus.billable_sms_types())
NOTIFICATION_STATUS_TYPES_SENT_EMAILS = list(NotificationStatus.sent_email_types())
NOTIFICATION_STATUS_TYPES = [s.value for s in NotificationStatus]
NOTIFICATION_STATUS_TYPES_NON_BILLABLE = list(NotificationStatus.non_billable_types())

# -- Template / notification types --

SMS_TYPE = TemplateType.SMS
EMAIL_TYPE = TemplateType.EMAIL
LETTER_TYPE = TemplateType.LETTER
ALL_TYPE = "all"
TEMPLATE_TYPES = [SMS_TYPE, EMAIL_TYPE, LETTER_TYPE]
NOTIFICATION_TYPES = [SMS_TYPE, EMAIL_TYPE, LETTER_TYPE]

# -- API key types --

KEY_TYPE_NORMAL = KeyType.NORMAL
KEY_TYPE_TEAM = KeyType.TEAM
KEY_TYPE_TEST = KeyType.TEST

# -- User permissions --

MANAGE_USERS = PermissionType.MANAGE_USERS
MANAGE_TEMPLATES = PermissionType.MANAGE_TEMPLATES
MANAGE_SETTINGS = PermissionType.MANAGE_SETTINGS
SEND_TEXTS = PermissionType.SEND_TEXTS
SEND_EMAILS = PermissionType.SEND_EMAILS
SEND_LETTERS = "send_letters"
MANAGE_API_KEYS = PermissionType.MANAGE_API_KEYS
PLATFORM_ADMIN = PermissionType.PLATFORM_ADMIN
VIEW_ACTIVITY = PermissionType.VIEW_ACTIVITY

PERMISSION_LIST = [
    MANAGE_USERS,
    MANAGE_TEMPLATES,
    MANAGE_SETTINGS,
    SEND_TEXTS,
    SEND_EMAILS,
    SEND_LETTERS,
    MANAGE_API_KEYS,
    PLATFORM_ADMIN,
    VIEW_ACTIVITY,
]

# -- Service permissions --

INTERNATIONAL_SMS_TYPE = ServicePermissionType.INTERNATIONAL_SMS
INBOUND_SMS_TYPE = ServicePermissionType.INBOUND_SMS
EMAIL_AUTH = ServicePermissionType.EMAIL_AUTH
EDIT_FOLDER_PERMISSIONS = ServicePermissionType.EDIT_FOLDER_PERMISSIONS
INTERNATIONAL_LETTERS = "international_letters"
UPLOAD_DOCUMENT = ServicePermissionType.UPLOAD_DOCUMENT
SCHEDULE_NOTIFICATIONS = ServicePermissionType.SCHEDULE_NOTIFICATIONS

SERVICE_PERMISSION_TYPES = [
    EMAIL_TYPE,
    SMS_TYPE,
    LETTER_TYPE,
    INTERNATIONAL_SMS_TYPE,
    INBOUND_SMS_TYPE,
    EMAIL_AUTH,
    EDIT_FOLDER_PERMISSIONS,
    INTERNATIONAL_LETTERS,
]

# -- Auth types --

SMS_AUTH_TYPE = AuthType.SMS
EMAIL_AUTH_TYPE = AuthType.EMAIL
WEBAUTHN_AUTH_TYPE = AuthType.WEBAUTHN
USER_AUTH_TYPES = [SMS_AUTH_TYPE, EMAIL_AUTH_TYPE, WEBAUTHN_AUTH_TYPE]
VERIFY_CODE_TYPES = [EMAIL_TYPE, SMS_TYPE]

# -- Service callbacks --


class ServiceCallbackTypes(enum.StrEnum):
    delivery_status = CallbackType.DELIVERY_STATUS
    complaint = CallbackType.COMPLAINT
    inbound_sms = "inbound_sms"


# -- Branding --

BRANDING_ORG = BrandType.ORG
BRANDING_BOTH = BrandType.BOTH
BRANDING_ORG_BANNER = BrandType.ORG_BANNER
BRANDING_TYPES = [BRANDING_ORG, BRANDING_BOTH, BRANDING_ORG_BANNER]

# -- Job statuses --

JOB_STATUS_PENDING = JobStatus.PENDING
JOB_STATUS_IN_PROGRESS = JobStatus.IN_PROGRESS
JOB_STATUS_FINISHED = JobStatus.FINISHED
JOB_STATUS_SENDING_LIMITS_EXCEEDED = JobStatus.SENDING_LIMITS_EXCEEDED
JOB_STATUS_SCHEDULED = JobStatus.SCHEDULED
JOB_STATUS_CANCELLED = JobStatus.CANCELLED
JOB_STATUS_READY_TO_SEND = JobStatus.READY_TO_SEND
JOB_STATUS_SENT_TO_DVLA = JobStatus.SENT_TO_DVLA
JOB_STATUS_ERROR = JobStatus.ERROR

# -- Invite statuses --

INVITE_PENDING = InvitedUserStatus.PENDING
INVITE_ACCEPTED = InvitedUserStatus.ACCEPTED
INVITE_CANCELLED = InvitedUserStatus.CANCELLED
INVITED_USER_STATUS_TYPES = [INVITE_PENDING, INVITE_ACCEPTED, INVITE_CANCELLED]

# -- Organisation types --

ORG_TYPE_FEDERAL = OrganizationType.FEDERAL
ORG_TYPE_STATE = OrganizationType.STATE
ORG_TYPE_OTHER = OrganizationType.OTHER

# -- Providers --

SES_PROVIDER = "ses"
SNS_PROVIDER = "sns"

# -- Recipient types --

MOBILE_TYPE = "mobile"
GUEST_LIST_RECIPIENT_TYPE = [MOBILE_TYPE, EMAIL_TYPE]

# -- Letter postage (stubs for convergence) --

FIRST_CLASS = "first"
SECOND_CLASS = "second"
POSTAGE_TYPES = [FIRST_CLASS, SECOND_CLASS]

# -- Miscellaneous --

PRECOMPILED_TEMPLATE_NAME = "Pre-compiled PDF"
