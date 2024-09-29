import base64

class User:
    def __init__(self, id: int, login: str, first_name: str, last_name: str, password: str):
        self._login = login
        self._id = id
        self._first_name = first_name
        self._last_name = last_name
        self._password = self.encryption_pass(password)

    # Кодирует пароль через Base64
    def encryption_pass(self, password: str) -> str:
        bytes_string = password.encode('utf-8')
        base64_encoded = base64.b64encode(bytes_string)
        base64_string = base64_encoded.decode('utf-8')
        return base64_string

    # Декодируем пароль из Base64
    def decode_pass(self, password: str) -> str:
        decoded_bytes = base64.b64decode(password)
        return decoded_bytes.decode('utf-8')