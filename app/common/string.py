import re
import string
import random
import dns.resolver


def validate_email(email, check_dns=False):
    email = email.strip()
    if not email:
        return False

    pattern = '^([_a-z0-9-]+(\.[_a-z0-9-]+)*)' +\
             '@([a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4}))$'
    matches = re.findall(pattern, email)
    if not matches:
        return False

    if check_dns:
        try:
            domain = matches[0][2]
            records = dns.resolver.query(domain, 'MX')
            mxRecord = records[0].exchange
            mxRecord = str(mxRecord)
            if not mxRecord:
                return False
        except Exception:
                return False

    return True


def random_str(num, is_digits_only=False):
    if is_digits_only:
        population = string.digits
    else:
        population = string.ascii_letters + string.digits

    return ''.join(random.choices(population, k=num))
