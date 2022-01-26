import hashlib


def compute_hash(raw_string: str) -> str:
    return hashlib.sha256(raw_string.encode()).hexdigest()


def compare_hash(raw_string: str, hash_string: str) -> bool:
    return compute_hash(raw_string) == hash_string
