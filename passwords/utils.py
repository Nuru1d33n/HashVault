import re

def identify_hash_type(hash_value):
    hash_types = {
        'md5': re.compile(r'^[a-f0-9]{32}$', re.IGNORECASE),
        'sha1': re.compile(r'^[a-f0-9]{40}$', re.IGNORECASE),
        'sha224': re.compile(r'^[a-f0-9]{56}$', re.IGNORECASE),
        'sha256': re.compile(r'^[a-f0-9]{64}$', re.IGNORECASE),
        'sha384': re.compile(r'^[a-f0-9]{96}$', re.IGNORECASE),
        'sha512': re.compile(r'^[a-f0-9]{128}$', re.IGNORECASE),
        'sha3_256': re.compile(r'^[a-f0-9]{64}$', re.IGNORECASE)
    }

    for hash_type, pattern in hash_types.items():
        if pattern.match(hash_value):
            return hash_type
    return 'Unknown'
