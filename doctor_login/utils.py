# utils.py

import uuid

def generate_booking_id(user, doctor, slot):
    return f"{user.id}-{doctor.id}-{slot}-{uuid.uuid4().hex[:6].upper()}"


from .models import docDetails

def free_slot(doctor, appointment_id):
    """
    Frees the slot associated with the given appointment ID.
    """
    for i in range(1, 8):
        slot_id_field = f'slot{i}_id'
        slot_field = f'slot{i}'
        if getattr(doctor, slot_id_field) == str(appointment_id):
            setattr(doctor, slot_field, False)
            setattr(doctor, slot_id_field, '')
            doctor.save()
            break  # Exit after freeing the relevant slot

def assign_slot(doctor, appointment):
    """
    Assigns the first available slot to the appointment.
    """
    for i in range(1, 8):
        slot_id_field = f'slot{i}_id'
        slot_field = f'slot{i}'
        if not getattr(doctor, slot_field):
            setattr(doctor, slot_field, True)
            setattr(doctor, slot_id_field, str(appointment.id))
            doctor.save()
            break
    else:
        # Handle the case where no slots are available
        raise Exception("No available slots to assign the appointment.")