from hashlib import md5


def check_hash(hash):
    try:

        user_id, string = hash.split("-", maxsplit=1)
        if not user_id.isdigit():
            return False

        return md5(hash.encode("utf8")).hexdigest().startswith("00000")

    except ValueError:
        return False


def check_hashes(strings):
    return [(s, check_hash(s)) for s in strings]
