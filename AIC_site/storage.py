from django.core.files import File
from queued_storage.backends import QueuedStorage


class SyncingStorage(QueuedStorage):
    def get_storage(self, name):
        if self.local.exists(name):
            return self.local
        return self.remote

    def open(self, name, mode='rb'):
        if self.using_remote(name):
            if not self.remote.exists(name):
                return None
            local_file = self.get_storage(name).open(name, 'rb')
            content = File(local_file)
            self.local._save(name, content)
        return self.get_storage(name).open(name, mode)