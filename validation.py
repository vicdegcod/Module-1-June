import re
from datetime import datetime


# ==========================================
# NAME VALIDATION
# ==========================================

def validate_name(name):

    name = name.strip()

    if name == "":
        return False, "Name cannot be empty."

    if len(name) < 3:
        return False, "Name must be at least 3 characters."

    if not all(char.isalpha() or char.isspace() for char in name):
        return False, "Name should contain letters only."

    return True, "Valid"


# ==========================================
# AGE VALIDATION
# ==========================================

def validate_age(age):

    try:

        age = int(age)

        if age < 1 or age > 120:
            return False, "Age must be between 1 and 120."

        return True, "Valid"

    except ValueError:

        return False, "Age must be a valid number."


# ==========================================
# GENDER VALIDATION
# ==========================================

def validate_gender(gender):

    valid_genders = ["Male", "Female", "Other"]

    if gender not in valid_genders:

        return False, "Please select a valid gender."

    return True, "Valid"


# ==========================================
# EMAIL VALIDATION
# ==========================================

def validate_email(email):

    email = email.strip()

    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

    if re.match(pattern, email):

        return True, "Valid"

    return False, "Invalid email address."


# ==========================================
# PHONE VALIDATION
# ==========================================

def validate_phone(phone):

    phone = phone.strip()

    pattern = r"^(?:\+254|0)[17]\d{8}$"

    if re.match(pattern, phone):

        return True, "Valid"

    return False, "Enter a valid Kenyan phone number."


# ==========================================
# SESSION VALIDATION
# ==========================================

def validate_sessions(sessions):

    try:

        sessions = int(sessions)

        if sessions < 0:

            return False, "Sessions cannot be negative."

        return True, "Valid"

    except ValueError:

        return False, "Sessions must be a whole number."


# ==========================================
# DATE VALIDATION
# ==========================================

def validate_date(date_text):

    try:

        datetime.strptime(date_text, "%Y-%m-%d")

        return True, "Valid"

    except ValueError:

        return False, "Date must be in YYYY-MM-DD format."


# ==========================================
# PASSWORD VALIDATION
# ==========================================

def validate_password(password):

    if len(password) < 6:

        return False, "Password must be at least 6 characters."

    if not any(char.isupper() for char in password):

        return False, "Password must contain an uppercase letter."

    if not any(char.islower() for char in password):

        return False, "Password must contain a lowercase letter."

    if not any(char.isdigit() for char in password):

        return False, "Password must contain a number."

    return True, "Valid"