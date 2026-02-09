import bcrypt


def hash_password(plain_password: str) -> str:
    """
    Hashes a plain text password using the bcrypt algorithm.

    A random salt is automatically generated to enhance security.
    The returned password is UTF-8 encoded and ready to be stored.

    :param plain_password: plain text password to hash.
    :type plain_password: str
    :return: Hashed password suitable for database storage
    :rtype: str
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(plain_password.encode('utf-8'), salt).decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies tha a plain text password matches a hashed password.
    The function compares the provided password with the stored hash
    using bcrypt, without ever decrypting the password.

    :param plain_password: plain text password to verify.
    :type plain_password: str
    :param hashed_password: stored hashed password.
    :type hashed_password: str
    :return: True if the passwords match, False otherwise.
    :rtype: bool

    """
    return bcrypt.checkpw(
        plain_password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )
