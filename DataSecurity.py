import base64
from UserClasses import User

class SecurityManager:
    def checkPermission(self, user: "User", action: str) -> bool:
        permissions = {
            "file_report": ["Student"],
            "review_report": ["Teacher"],
            "assign_staff": ["Administrator"]
        }
        if action in permissions and user.role in permissions[action]:
            return True
        return False

    def encryptData(self, data: str) -> str:
        encoded_bytes = base64.b64encode(data.encode("utf-8"))
        return str(encoded_bytes, "utf-8")

    def decryptData(self, data: str) -> str:
        decoded_bytes = base64.b64decode(data.encode("utf-8"))
        return str(decoded_bytes, "utf-8")