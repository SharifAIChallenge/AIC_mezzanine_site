import hashlib

from django.core.files import File
from django.utils.encoding import force_bytes
from queued_storage.backends import QueuedStorage
from storages.backends.hashpath import HashPathStorage


class SyncingStorage(QueuedStorage):
    def get_storage(self, name):
        if self.local.exists(name):
            return self.local
        return self.remote

    def open(self, name, mode='rb'):
        if self.using_remote(name):
            if not self.remote.exists(name):
                raise IOError('File has not been synced yet.')
            local_file = self.get_storage(name).open(name, 'rb')
            content = File(local_file)
            self.local._save(name, content)
        return self.get_storage(name).open(name, mode)


class SyncingHashStorage(SyncingStorage):
    def __init__(self, remote, *args, **kwargs):
        local = 'storages.backends.hashpath.HashPathStorage'
        super(SyncingHashStorage, self).__init__(local=local, remote=remote, *args, **kwargs)

    def open(self, name, mode='rb'):
        if self.using_remote(name):
            if not self.remote.exists(name):
                raise IOError('File has not been synced yet. File does not exists.')
            local_file = self.get_storage(name).open(name, 'rb')
            content = File(local_file)
            sha1 = hashlib.sha1()
            for chunk in content.chunks():
                sha1.update(force_bytes(chunk))
            sha1sum = sha1.hexdigest()
            if not str(sha1sum) == str(name.split("/")[-1]):
                raise IOError('File has not been synced yet. Hash Conflict.')
            self.local._save(name, content)
        return self.get_storage(name).open(name, mode)

