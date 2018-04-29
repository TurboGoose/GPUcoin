from hashlib import md5


def check_hash(hash):
    return md5(hash.encode("utf8")).hexdigest().startswith("0000")


def check_string(string):
    try:
        user, hash_mes = string.split("-", maxsplit=1)
        if check_hash(hash_mes) and user.isdigit():
            return True
        return False
    except ValueError:
        return False


def check_strings(strings):
    return [(s, check_string(s)) for s in strings]
