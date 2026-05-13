from django.core.files.storage import Storage
from smb.SMBConnection import SMBConnection
import io, os


class SMBStorage(Storage):
    def __init__(
        self, host=None, share=None, username=None, password=None, domain="", port=445
    ):
        from django.conf import settings

        opts = settings.STORAGES["default"]["OPTIONS"]
        self.host = host or opts["host"]
        self.share = share or opts["share"]
        self.username = username or opts["username"]
        self.password = password or opts["password"]
        self.domain = domain or opts.get("domain", "")
        self.port = int(port or opts.get("port", 445))

    def _connect(self):
        conn = SMBConnection(
            self.username,
            self.password,
            "django",
            self.host,
            domain=self.domain,
            use_ntlm_v2=True,
        )
        conn.connect(self.host, self.port)
        return conn

    def _save(self, name, content):
        conn = self._connect()
        conn.storeFile(self.share, name, content)
        conn.close()
        return name

    def _open(self, name, mode="rb"):
        conn = self._connect()
        buf = io.BytesIO()
        conn.retrieveFile(self.share, name, buf)
        conn.close()
        buf.seek(0)
        return buf

    def exists(self, name):
        try:
            conn = self._connect()
            conn.getAttributes(self.share, name)
            conn.close()
            return True
        except Exception:
            return False

    def url(self, name):
        return f"/media/{name}"
