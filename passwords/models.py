import hashlib
import os
from django.utils import timezone
from django.db import models

# hashlib.
# hashlib.algorithms_available   hashlib.pbkdf2_hmac(           hashlib.sha3_256(
# hashlib.algorithms_guaranteed  hashlib.scrypt(                hashlib.sha3_384(
# hashlib.blake2b(               hashlib.sha1(                  hashlib.sha3_512(
# hashlib.blake2s(               hashlib.sha224(                hashlib.sha512(
# hashlib.file_digest(           hashlib.sha256(                hashlib.shake_128(
# hashlib.md5(                   hashlib.sha384(                hashlib.shake_256(
# hashlib.new(                   hashlib.sha3_224(         


class Password(models.Model):
    """
    Store plaintext passwords in the database.
    """
    value = models.CharField(max_length=255, unique=True)  # Store the plaintext password
    created_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        """
        Save the password and generate associated hashes.
        """
        super().save(*args, **kwargs)  # Save the password first
        # List of algorithms to use for hashing
        algorithms = [
            'md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512',
            'sha3_224', 'sha3_256', 'sha3_384', 'sha3_512',
            'blake2b', 'blake2s', 'pbkdf2_hmac', 'scrypt', 'shake_128',
            'shake_256'
        ]

        # Create a PasswordHash entry for each algorithm
        for algorithm in algorithms:
            hash_value = PasswordHash.generate_hash(self.value, algorithm)
            PasswordHash.objects.create(password=self, hash_value=hash_value, algorithm=algorithm)

    @classmethod
    def create_password(cls, value):
        """
        Create a password entry if it doesn't already exist.
        """
        if cls.objects.filter(value=value).exists():
            return None  # Indicate that the password already exists
        return cls.objects.create(value=value)

    def __str__(self):
        return self.value


class PasswordHash(models.Model):
    """
    Store password hashes along with the algorithm used to generate them.
    """
    password = models.ForeignKey(Password, related_name='password_hashes', on_delete=models.CASCADE)
    hash_value = models.CharField(max_length=255)  # Store the hashed password
    algorithm = models.CharField(max_length=50, choices=[
        ('md5', 'MD5'),
        ('sha1', 'SHA-1'),
        ('sha224', 'SHA-224'),
        ('sha256', 'SHA-256'),
        ('sha384', 'SHA-384'),
        ('sha512', 'SHA-512'),
        ('sha3_224', 'SHA3-224'),
        ('sha3_256', 'SHA3-256'),
        ('sha3_384', 'SHA3-384'),
        ('sha3_512', 'SHA3-512'),
        ('blake2b', 'Blake2b'),
        ('blake2s', 'Blake2s'),
        ('pbkdf2_hmac', 'PBKDF2 HMAC'),
        ('scrypt', 'Scrypt'),
        ('shake_128', 'Shake-128'),
        ('shake_256', 'Shake-256'),
    ], default='sha256')  # Default algorithm can be SHA-256
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.algorithm} - {self.hash_value}'

    @classmethod
    def generate_hash(cls, password: str, algorithm: str):
        """
        Generate a hash for the given password and algorithm.
        """
        # Ensure the password is encoded in bytes
        # password_bytes = password.encode()
        password_bytes = password.encode('utf-8')

        if algorithm == 'md5':
            hash_value = hashlib.md5(password_bytes).hexdigest()
        elif algorithm == 'sha1':
            hash_value = hashlib.sha1(password_bytes).hexdigest()
        elif algorithm == 'sha224':
            hash_value = hashlib.sha224(password_bytes).hexdigest()
        elif algorithm == 'sha256':
            hash_value = hashlib.sha256(password_bytes).hexdigest()
        elif algorithm == 'sha384':
            hash_value = hashlib.sha384(password_bytes).hexdigest()
        elif algorithm == 'sha512':
            hash_value = hashlib.sha512(password_bytes).hexdigest()
        elif algorithm == 'sha3_224':
            hash_value = hashlib.sha3_224(password_bytes).hexdigest()
        elif algorithm == 'sha3_256':
            hash_value = hashlib.sha3_256(password_bytes).hexdigest()
        elif algorithm == 'sha3_384':
            hash_value = hashlib.sha3_384(password_bytes).hexdigest()
        elif algorithm == 'sha3_512':
            hash_value = hashlib.sha3_512(password_bytes).hexdigest()
        elif algorithm == 'blake2b':
            hash_value = hashlib.blake2b(password_bytes).hexdigest()
        elif algorithm == 'blake2s':
            hash_value = hashlib.blake2s(password_bytes).hexdigest()
        elif algorithm == 'pbkdf2_hmac':
            salt = os.urandom(16)  # Generate a unique salt
            hash_value = hashlib.pbkdf2_hmac('sha256', password_bytes, salt, 100000).hex()
        elif algorithm == 'scrypt':
            salt = os.urandom(16)  # Generate a unique salt
            hash_value = hashlib.scrypt(password_bytes, salt=salt, n=16384, r=8, p=1).hex()
        elif algorithm == 'shake_128':
            hash_value = hashlib.shake_128(password_bytes).hexdigest(64)  # Adjust output length as needed
        elif algorithm == 'shake_256':
            hash_value = hashlib.shake_256(password_bytes).hexdigest(64)
        else:
            raise ValueError(f"Unsupported algorithm: {algorithm}")

        return hash_value
