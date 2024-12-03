import hashlib

def generate_hashes(word):
    hash_md5 = hashlib.md5(word.encode()).hexdigest()
    hash_sha1 = hashlib.sha1(word.encode()).hexdigest()
    hash_sha256 = hashlib.sha256(word.encode()).hexdigest()
    hash_sha512 = hashlib.sha512(word.encode()).hexdigest()
    
    print(f"MD5 Hash: {hash_md5}")
    print(f"SHA-1 Hash: {hash_sha1}")
    print(f"SHA-256 Hash: {hash_sha256}")
    print(f"SHA-512 Hash: {hash_sha512}")

if __name__ == "__main__":
    word = input("Enter a word to generate hashes: ")
    generate_hashes(word)
