import re

def suggest_specialist(text):
    text = text.lower()

    # Check for greetings first
    greetings = ['hi', 'hello']
    if any(greeting in text for greeting in greetings):
        return "Hello! Please tell me your symptoms."

    keywords = {
        'Orthodontist': ['braces', 'overbite', 'underbite', 'straighten teeth', 'invisalign', 'retainer'],
        'Dentist': ['cavity', 'toothache', 'gum', 'teeth cleaning', 'root canal', 'wisdom teeth'],
        'Cardiologist': ['heart', 'chest pain', 'blood pressure', 'palpitations', 'irregular heartbeat'],
        'Surgeon': ['surgery', 'operation', 'transplant', 'appendectomy', 'hysterectomy', 'gallbladder'],
        'Orthopedic Surgeon': ['joint pain', 'arthritis', 'fracture', 'tendon', 'ligament', 'bone', 'jaw', 'leg',
                               'hands', 'hand', 'skull', 'foot', 'swollen'],
        'Endocrinologist': ['hormone', 'thyroid', 'diabetes', 'adrenal', 'pituitary', 'insulin'],
        'Dermatologist': ['skin', 'acne', 'eczema', 'psoriasis', 'rash', 'melanoma'],
        'Allergist': ['allergy', 'asthma', 'hay fever', 'hives', 'eczema', 'anaphylaxis', 'itching', 'red spots'],
        'Internal Medicine Specialist': ['infection', 'diagnosis', 'chronic illness', 'health maintenance',
                                         'prevention'],
        'Anesthesiologist': ['anesthesia', 'pain management', 'epidural', 'spinal', 'nerve block', 'sedation'],
        'Neurologist': ['brain', 'spine', 'nerve', 'seizure', 'stroke', 'migraine'],
        'Physiotherapist': ['rehabilitation', 'exercise', 'stretching', 'strengthening', 'mobility', 'injury'],
    }

    specialist_scores = {}

    for specialist, specialist_keywords in keywords.items():
        specialist_scores[specialist] = 0
        for keyword in specialist_keywords:
            if re.search(r'\b' + keyword + r'\b', text):
                specialist_scores[specialist] += 1

    # Check if there are any specialist scores greater than 0
    if not any(score > 0 for score in specialist_scores.values()):
        return ("I'm sorry, I couldn't understand your symptoms. "
                "Please provide more information or try rephrasing your query.<br>"
                "Available specialists:<br>"
                "1. Cardiologist<br>"
                "2. Orthopedic Surgeon<br>"
                "3. Endocrinologist<br>"
                "4. Dermatologist<br>"
                "5. Allergist<br>"
                "6. Internal Medicine Specialist<br>"
                "7. Anesthesiologist<br>"
                "8. Neurologist<br>"
                "9. Dentist<br>"
                "10. Physiotherapist")

    suggested_specialist = max(specialist_scores, key=specialist_scores.get)
    return f"I recommend you book an appointment with a/an {suggested_specialist}."