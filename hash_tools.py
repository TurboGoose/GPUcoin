from hashlib import md5


def check_hash(hash):
    return md5(hash.encode("utf8")).hexdigest().startswith("00000")


def check_hashes(strings):
    return [(s, check_hash(s)) for s in strings]
