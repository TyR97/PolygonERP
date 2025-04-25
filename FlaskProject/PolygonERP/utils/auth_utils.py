admin_titles = ['senior developer', 'hr', 'accountant', 'sysadmin', 'dev']
existing_usernames = []

def is_user_admin(job_title):
   return job_title.lower() in admin_titles

def generate_username(full_name):
    parts = full_name.split(' ')
    if len(parts) < 2:
        raise ValueError("Full name must have at least two words")

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