from django.db.models import TextChoices


class GenderChoices(TextChoices):
    MALE = "M"
    FEMALE = "F"
    OTHER = "O"

class EventChoices(TextChoices):
    SELF_VKYC_INITIATED = "self_vkyc_initiated"
    SELF_VKYC_SUBMITTED = "self_vkyc_submitted"
    SELF_VKYC_VERIFIED = "self_vkyc_verified"
    SCHEDULE_VKYC_BOOKED = "self_vkyc_booked"
    CALL_SCHEDULED = "call_scheduled"
    SCHEDULED_CALL_STARTED = "schedule_call_started"
    SCHEDULED_CALL_ENDED = "schedule_call_ended"
    SCHEDULED_VKYC_VERIFIED = "scheduled_vkyc_verified"