import random
import string

from flask import flash

#TODO refactor
def generate_username(existing_usernames, full_name):
    parts = full_name.split(' ')
    if len(parts) < 2:
        print("Full name must have at least two words")


    last_name = parts[0].capitalize()
    first_name = parts[1].capitalize()
    base_username = f"{last_name}{first_name[0]}"

    username = base_username
    counter = 1

    while username in existing_usernames:
        username = f"{base_username}{counter}"
        counter += 1
    existing_usernames.append(username)
    return username



def generate_password(length=8):
    characters = string.ascii_letters + string.digits  # A-Z, a-z, 0-9
    return ''.join(random.choices(characters, k=length))
