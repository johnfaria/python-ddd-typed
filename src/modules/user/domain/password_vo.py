import hashlib
from secrets import token_hex
from typing import NamedTuple

from core.domain.protocols.value_object_protocol import ValueObject


class PasswordProps(NamedTuple):
    hashed_password: str
    salt: str


class Password(ValueObject[PasswordProps]):
    PASSWORD_ITERATIONS = 100000  # Número de iterações
    PASSWORD_KEYLEN = 32  # Comprimento da chave derivada
    PASSWORD_DIGEST = "sha256"  # Algoritmo de hash

    def __init__(self, props: PasswordProps) -> None:
        super().__init__(props)

    @classmethod
    def create(cls, password: str, salt: str | None = None) -> "Password":
        generated_salt = salt or token_hex(20)
        key = hashlib.pbkdf2_hmac(
            cls.PASSWORD_DIGEST,
            password.encode("utf-8"),
            generated_salt.encode("utf-8"),
            cls.PASSWORD_ITERATIONS,
            cls.PASSWORD_KEYLEN,
        ).hex()
        return cls(PasswordProps(key, generated_salt))

    def verify(self, plain_password: str) -> bool:
        key = hashlib.pbkdf2_hmac(
            self.PASSWORD_DIGEST,
            plain_password.encode("utf-8"),
            self.props.salt.encode("utf-8"),
            self.PASSWORD_ITERATIONS,
            self.PASSWORD_KEYLEN,
        ).hex()
        return self.props.hashed_password == key


if __name__ == "__main__":
    password = Password.create("secret")
    print(password.props)
    result = password.verify("secret")
    print(result)
