def generate_context_airlinecrm(task, details):
    if task == "TASK_CANCEL_FLIGHT": #make sure context has the word "booking"
        context = f"Cancel the flight booking with confirmation code {details['confirmation-code']}"
        return context
    elif task == "TASK_FIND_BOOKING": #make sure context has the word "booking"
        context = f"Find the flight booking with confirmation code {details['confirmation-code']}"
        return context
    elif task == "TASK_FIND_FLIGHT": 
        context = f"Search for a flight from {details['flight']['from']} to {details['flight']['to']}, leaving on {details['flight']['departure']} at {details['flight']['outward-departure-time']} and returning on {details['flight']['return']} at {details['flight']['return-arrival-time']}"
        return context
    elif task == "TASK_BOOK_FLIGHT":
        context = f"I want to search for a flight from {details['flight']['from']} to {details['flight']['to']}, leaving on {details['flight']['departure']} at {details['flight']['outward-departure-time']} and returning on {details['flight']['return']} at {details['flight']['return-arrival-time']}"
        context = context + f". I want to book a flight. "
        context = context + f". My passenger details are as follows. Title: {details['passenger']['title']}, Firstname: {details['passenger']['firstname']}, Lastname: {details['passenger']['lastname']}, Gender: {details['passenger']['gender']}, DOB: {details['passenger']['dob']}, Email: {details['passenger']['email']}"
        context = context + f". My payment details are as follows. Card Number: {details['payment-details']['card-number']}, Expiry: {details['payment-details']['expiry']}, Security Code: {details['payment-details']['security_code']}, Name on card: {details['payment-details']['name-on-card']}"
        return context
    elif task == "TASK_UPDATE_PASSENGER_DETAILS":
        context = f"Find my flight booking with confirmation code {details['confirmation-code']}."
        context = context + f" I want to update the following passenger details. "
        for key, value in details['passenger'].items():
            context = context + f" {key}: {value} "
        return context