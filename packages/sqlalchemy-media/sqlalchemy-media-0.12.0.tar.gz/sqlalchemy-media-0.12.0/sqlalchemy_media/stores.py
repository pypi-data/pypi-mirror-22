from io import BytesIO
from os import makedirs, remove
from os.path import abspath, join, dirname, exists, split
from typing import Iterable

from sqlalchemy import event
from sqlalchemy.util.langhelpers import symbol

from sqlalchemy_media.context import get_id as get_context_id
from sqlalchemy_media.exceptions import ContextError, DefaultStoreError, \
    S3Error, OS2Error
from sqlalchemy_media.helpers import copy_stream
from sqlalchemy_media.optionals import ensure_aws4auth, ensure_os2auth, ensure_paramiko
from sqlalchemy_media.typing_ import FileLike

# Importing optional stuff required by http based store
try:
    # noinspection PyPackageRequirements
    import requests
except ImportError:  # pragma: no cover
    requests = None

# Importing optional stuff required by S3 store
try:
    # noinspection PyPackageRequirements
    from requests_aws4auth import AWS4Auth
except ImportError:  # pragma: no cover
    AWS4Auth = None

# Importing optional stuff required by OS2 store
try:
    # noinspection PyPackageRequirements
    from aliyunauth import OssAuth as OS2Auth
except ImportError:  # pragma: no cover
    OS2Auth = None


# Global variable to store contexts
_context_stacks = {}

# Global variable to store store factories
_factories = {}

# Global variable to store observing attributes
_observing_attributes = set()


class Store:
    """
    The abstract base class for all stores.
    """

    # noinspection PyMethodMayBeStatic
    def cleanup(self):
        """
        In derived class should cleanup all dirty stuff created while storing and deleting file.
        If not overridden, no error will be raised.

        .. seealso:: :meth:`.StoreManager.cleanup`

        """
        pass

    def put(self, filename: str, stream: FileLike) -> int:
        """
        **[Abstract]**

        Should be overridden in inherited class and puts the file-like object as the given filename in the store.

        .. versionchanged:: 0.5

           - ``min_length`` has been removed.
           - ``max_length`` has been removed.

        :param filename: the target filename.
        :param stream: the source file-like object
        :return: length of the stored file.
        """
        raise NotImplementedError()  # pragma: no cover

    def delete(self, filename: str) -> None:
        """
        **[Abstract]**

        Should be overridden in inherited class and deletes the given file.

        :param filename: The filename to delete

        """
        raise NotImplementedError()  # pragma: no cover

    def open(self, filename: str, mode: str='rb') -> FileLike:
        """
        **[Abstract]**

        Should be overridden in inherited class and return a file-like object representing the file in the store.

        .. note:: Caller of this method is responsible to close the file-like object.

        :param filename: The filename to open.
        :param mode: same as the `mode` in famous :func:`.open` function.

        """
        raise NotImplementedError()  # pragma: no cover

    def locate(self, attachment) -> str:
        """
        **[Abstract]**

        If overridden in the inherited class, should locates the file's url to share in public space.

        :param attachment: The :class:`.Attachment` object to
        """
        raise NotImplementedError()  # pragma: no cover


class FileSystemStore(Store):
    """
    Store for dealing with local file-system.

    """

    def __init__(self, root_path: str, base_url: str, chunk_size: int=32768):
        self.root_path = abspath(root_path)
        self.base_url = base_url.rstrip('/')
        self.chunk_size = chunk_size

    def _get_physical_path(self, filename: str) -> str:
        return join(self.root_path, filename)

    def put(self, filename: str, stream: FileLike):
        physical_path = self._get_physical_path(filename)
        physical_directory = dirname(physical_path)

        if not exists(physical_directory):
            makedirs(physical_directory, exist_ok=True)

        with open(physical_path, mode='wb') as target_file:
            return copy_stream(
                stream,
                target_file,
                chunk_size=self.chunk_size
            )

    def delete(self, filename: str):
        physical_path = self._get_physical_path(filename)
        remove(physical_path)

    def open(self, filename: str, mode: str='rb') -> FileLike:
        return open(self._get_physical_path(filename), mode=mode)

    def locate(self, attachment) -> str:
        return '%s/%s' % (self.base_url, attachment.path)


class S3Store(Store):
    """
    Store for dealing with s3 of aws

    .. versionadded:: 0.9.0

    .. versionadded:: 0.9.6

       - ``prefix``

    """
    BASE_URL_FORMAT = 'https://{0}.s3.amazonaws.com'

    DEFAULT_MAX_AGE = 60 * 60 * 24 * 365

    def __init__(self, bucket: str, access_key: str, secret_key: str,
                 region: str, max_age: int = DEFAULT_MAX_AGE,
                 prefix: str = None, public_base_url: str = None):
        self.bucket = bucket
        self.access_key = access_key
        self.secret_key = secret_key
        self.region = region
        self.max_age = max_age
        self.prefix = prefix
        self.base_url = self.BASE_URL_FORMAT.format(bucket)
        if prefix:
            self.base_url = '{0}/{1}'.format(self.base_url, prefix)
        if public_base_url is None:
            self.public_base_url = self.base_url
        elif public_base_url.endswith('/'):
            self.public_base_url = public_base_url.rstrip('/')
        else:
            self.public_base_url = public_base_url

    def _get_s3_url(self, filename: str):
        return '{0}/{1}'.format(self.base_url, filename)

    def _upload_file(self, url: str, data: str, content_type: str,
                     rrs: bool = False, acl: str = 'private'):
        ensure_aws4auth()

        auth = AWS4Auth(self.access_key, self.secret_key, self.region, 's3')
        if rrs:
            storage_class = 'REDUCED_REDUNDANCY'
        else:
            storage_class = 'STANDARD'
        headers = {
            'Cache-Control': 'max-age=' + str(self.max_age),
            'x-amz-acl': acl,
            'x-amz-storage-class': storage_class
        }
        if content_type:
            headers['Content-Type'] = content_type
        res = requests.put(url, auth=auth, data=data, headers=headers)
        if not 200 <= res.status_code < 300:
            raise S3Error(res.text)

    def put(self, filename: str, stream: FileLike):
        url = self._get_s3_url(filename)
        data = stream.read()
        content_type = getattr(stream, 'content_type', None)
        rrs = getattr(stream, 'reproducible', False)
        self._upload_file(url, data, content_type, rrs=rrs)
        return len(data)

    def delete(self, filename: str):
        ensure_aws4auth()
        url = self._get_s3_url(filename)
        auth = AWS4Auth(self.access_key, self.secret_key, self.region, 's3')
        res = requests.delete(url, auth=auth)
        if not 200 <= res.status_code < 300:
            raise S3Error(res.text)

    def open(self, filename: str, mode: str='rb') -> FileLike:
        ensure_aws4auth()
        url = self._get_s3_url(filename)
        auth = AWS4Auth(self.access_key, self.secret_key, self.region, 's3')
        res = requests.get(url, auth=auth)
        if not 200 <= res.status_code < 300:
            raise S3Error(res.text)
        return BytesIO(res.content)

    def locate(self, attachment) -> str:
        return '%s/%s' % (self.public_base_url, attachment.path)


class OS2Store(Store):
    """
    Store for dealing with oss of aliyun

    """
    BASE_URL_FORMAT = 'https://{0}.oss-{1}.aliyuncs.com'

    DEFAULT_MAX_AGE = 60 * 60 * 24 * 365

    def __init__(self, bucket: str, access_key: str, secret_key: str,
                 region: str, max_age: int = DEFAULT_MAX_AGE,
                 base_headers: dict = None, prefix: str = None, public_base_url: str = None):
        self.bucket = bucket
        self.access_key = access_key
        self.secret_key = secret_key
        self.region = region
        self.max_age = max_age
        self.prefix = prefix
        self.base_url = self.BASE_URL_FORMAT.format(bucket, region)
        if prefix:
            self.base_url = '{0}/{1}'.format(self.base_url, prefix)
        if public_base_url is None:
            self.public_base_url = self.base_url
        elif public_base_url.endswith('/'):
            self.public_base_url = public_base_url.rstrip('/')
        else:
            self.public_base_url = public_base_url
        self.base_headers = base_headers or {}

    def _get_os2_url(self, filename: str):
        return '{0}/{1}'.format(self.base_url, filename)

    def _upload_file(self, url: str, data: str, content_type: str,
                     acl: str = 'private'):
        ensure_os2auth()

        auth = OS2Auth(self.bucket, self.access_key, self.secret_key)
        headers = self.base_headers.copy()
        headers.update({
            'Cache-Control': 'max-age=' + str(self.max_age),
            'x-oss-object-acl': acl
        })
        if content_type:
            headers['Content-Type'] = content_type
        res = requests.put(url, auth=auth, data=data, headers=headers)
        if not 200 <= res.status_code < 300:
            raise OS2Error(res.text)

    def put(self, filename: str, stream: FileLike):
        url = self._get_os2_url(filename)
        data = stream.read()
        content_type = getattr(stream, 'content_type', None)
        self._upload_file(url, data, content_type)
        return len(data)

    def delete(self, filename: str):
        ensure_os2auth()
        url = self._get_os2_url(filename)
        auth = OS2Auth(self.bucket, self.access_key, self.secret_key)
        headers = self.base_headers.copy()
        res = requests.delete(url, auth=auth, headers=headers)
        if not 200 <= res.status_code < 300:
            raise OS2Error(res.text)

    def open(self, filename: str, mode: str='rb') -> FileLike:
        ensure_os2auth()
        url = self._get_os2_url(filename)
        auth = OS2Auth(self.bucket, self.access_key, self.secret_key)
        headers = self.base_headers.copy()
        res = requests.get(url, auth=auth, headers=headers)
        if not 200 <= res.status_code < 300:
            raise OS2Error(res.text)
        return BytesIO(res.content)

    def locate(self, attachment) -> str:
        return '%s/%s' % (self.public_base_url, attachment.path)


class SSHStore(Store):
    """
    Store for SSH protocol. aka SFTP

    """

    def __init__(self, hostname, root_path, base_url, ssh_config_file=None, **kwargs):
        ensure_paramiko()
        from sqlalchemy_media.ssh import SSHClient

        self.root_path = root_path
        self.base_url = base_url.rstrip('/')
        if isinstance(hostname, SSHClient):
            self.ssh_client = hostname
        else:
            self.ssh_client = SSHClient()
            self.ssh_client.load_config_file(filename=ssh_config_file)
            self.ssh_client.connect(hostname, **kwargs)

        self.ssh_client.sftp.chdir(None)

    def _get_remote_path(self, filename):
        return join(self.root_path, filename)

    def put(self, filename: str, stream: FileLike) -> int:
        remote_filename = self._get_remote_path(filename)
        remote_directory = dirname(remote_filename)
        self.ssh_client.exec_command(b'mkdir -p "%s"' % remote_directory.encode())
        result = self.ssh_client.sftp.putfo(stream, remote_filename)
        return result.st_size

    def delete(self, filename: str) -> None:
        remote_filename = self._get_remote_path(filename)
        self.ssh_client.remove(remote_filename)

    def open(self, filename: str, mode: str='rb'):
        remote_filename = self._get_remote_path(filename)
        return self.ssh_client.sftp.open(remote_filename, mode=mode)

    def locate(self, attachment) -> str:
        return '%s/%s' % (self.base_url, attachment.path)


class StoreManager(object):
    """

    This is an context manager.

    Before using you must register at least one store factory function as default with-in store registry with
    :meth:`register` by passing `default=true` during registration.

    This object will call the registered factory functions to instantiate one per
    :func:`sqlalchemy_media.context.get_id`.

    .. testcode::

        import functools

        from sqlalchemy.orm.session import Session

        from sqlalchemy_media import StoreManager, FileSystemStore

        StoreManager.register('fs', functools.partial(FileSystemStore, '/tmp/sa_temp_fs', 'http'), default=True)
        StoreManager.register('fs2', functools.partial(FileSystemStore, '/tmp/sa_temp_fs2', 'http'))

        with StoreManager(Session) as store_manager:
            assert StoreManager.get_current_store_manager() == store_manager

            print(store_manager.get().root_path)  # fs1 default store
            print(store_manager.get('fs2').root_path)  # fs2 store

    This would output:

    .. testoutput::

        /tmp/sa_temp_fs
        /tmp/sa_temp_fs2

    """

    _stores = None
    _default = None
    _files_to_delete_after_commit = None
    _files_to_delete_after_rollback = None
    _files_orphaned = None

    #: If :data:`.True` the orphaned attachments will be gathered and deleted after session commit.
    delete_orphan = False

    def __init__(self, session, delete_orphan=False):
        self.session = session
        self.delete_orphan = delete_orphan
        self.reset_files_state()

    def __enter__(self):
        """
        Enters the context: bind events and push itself into context stack.

        :return: self
        """
        self.bind_events()
        _context_stacks.setdefault(get_context_id(), []).append(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Destroy the context, pop itself from context stack and unbind all events.
        """
        _context_stacks.setdefault(get_context_id(), []).pop()
        self.unbind_events()
        self.cleanup()

    @property
    def stores(self) -> dict:
        """
        The mapping `str -> store factory`.

        :type: dict[str] -> callable
        """
        if self._stores is None:
            self._stores = {}
        # noinspection PyTypeChecker
        return self._stores

    @classmethod
    def get_current_store_manager(cls) -> 'StoreManager':
        """
        Find the current :class:`StoreManager` in context stack if any. else :exc:`.ContextError` will be raised.
        """
        try:
            return _context_stacks.setdefault(get_context_id(), [])[-1]
        except IndexError:
            raise ContextError('Not in store manager context.')

    def cleanup(self):
        """
        Calls the :meth:`.Store.cleanup` for each store is :attr:`.stores` and clears the :attr:`.stores` also.

        """
        for store in self.stores.values():
            store.cleanup()
        self.stores.clear()

    @classmethod
    def make_default(cls, key) -> None:
        """
        Makes a pre-registered store as default.

        :param key: the store id.
        """
        cls._default = key

    @classmethod
    def register(cls, key: str, store_factory, default: bool=False):
        """
        Registers the store factory into stores registry, use :meth:`unregister` to remove it.

        :param key: The unique key for store.
        :param store_factory: A callable that returns an instance of :class:`.Store`.
        :param default: If :data:`True` the given store will be marked as default also. in addition you can use
                        :meth:`.make_default` to mark a store as default.
        """
        _factories[key] = store_factory
        if default:
            cls._default = key

    @classmethod
    def unregister(cls, key) -> Store:
        """
        Opposite of :meth:`.register`. :exc:`.KeyError` may raised if key not found in registry.

        :param key: The store key to remove from stores registry.

        """
        if key == cls._default:
            cls._default = None

        if key in _factories:
            return _factories.pop(key)
        else:
            raise KeyError('Cannot find store: %s' % key)

    def get(self, key=None) -> Store:
        """
        Lookup the store in available instance cache, and instantiate a new one using registered factory function,
        if not found.

        If the key is :data:`.None`, the default store will be instantiated(if required) and returned.

        :param key: the store unique id to lookup.
        """
        if key is None:
            if self._default is None:
                raise DefaultStoreError()
            key = self._default

        if key not in self.stores:
            factory = _factories[key]
            self.stores[key] = factory()
        return self.stores[key]

    @property
    def default_store(self) -> Store:
        """
        The same as the :meth:`.get` without parameter.

        """
        return self.get()

    def bind_events(self) -> None:
        """
        Binds the required event on sqlalchemy session. to handle commit & rollback.

        """
        event.listen(self.session, 'after_commit', self.on_commit)
        event.listen(self.session, 'after_soft_rollback', self.on_rollback)
        event.listen(self.session, 'persistent_to_deleted', self.on_delete)

    def unbind_events(self) -> None:
        """
        Opposite of :meth:`bind_events`.

        """
        event.remove(self.session, 'after_commit', self.on_commit)
        event.remove(self.session, 'after_soft_rollback', self.on_rollback)
        event.remove(self.session, 'persistent_to_deleted', self.on_delete)

    def orphaned(self, *attachments) -> None:
        """
        Mark one or more attachment(s) orphaned, So if :attr:`delete_orphan` is :data:`.True`, the attachment(s) will
        be deleted from store after session commit.

        """
        if not self.delete_orphan:
            return

        for attachment in attachments:
            self._files_orphaned.append(attachment)
            self._files_orphaned.extend(attachment.get_orphaned_objects())

    def adopted(self, *attachments) -> None:
        """
        Opposite of :meth:`.orphaned`

        """
        if not self.delete_orphan:
            return

        for f in attachments:
            if f in self._files_orphaned:
                self._files_orphaned.remove(f)

    # noinspection PyUnresolvedReferences
    def register_to_delete_after_commit(self, *attachments: Iterable['Attachment']) -> None:
        """
        Schedules one or more attachment(s) to be deleted from store just after sqlalchemy session commit.

        """
        for attachment in attachments:
            self._files_to_delete_after_commit.extend(attachment.get_objects_to_delete())

    # noinspection PyUnresolvedReferences
    def register_to_delete_after_rollback(self, *files: Iterable['Attachment']) -> None:
        """
        Schedules one or more attachment(s) to be deleted from store just after sqlalchemy session rollback.

        """
        self._files_to_delete_after_rollback.extend(files)

    def reset_files_state(self) -> None:
        """
        Reset the object's state and forget all scheduled tasks for commit and or rollback.

        .. warning:: Calling this method without knowing what you are doing, will be caused bad result !

        """
        self._files_to_delete_after_commit = []
        self._files_to_delete_after_rollback = []
        self._files_orphaned = []

    # noinspection PyUnusedLocal
    def on_commit(self, session) -> None:
        """
        Will be called when session commit occurred.

        """
        for f in self._files_to_delete_after_commit:
            f.delete()

        if self.delete_orphan:
            for f in self._files_orphaned:
                f.delete()

        self.reset_files_state()

    # noinspection PyUnusedLocal
    def on_rollback(self, session, transaction):
        """
        Will be called when session rollback occurred.

        """
        for f in self._files_to_delete_after_rollback:
            f.delete()
        self.reset_files_state()

    # noinspection PyUnusedLocal
    def on_delete(self, session, instance):
        """
        Will be called when an model instance deleted.
        """
        for attribute in _observing_attributes:
            if isinstance(instance, attribute.class_):
                value = getattr(instance, attribute.key)
                if value:
                    self.register_to_delete_after_commit(value.copy())

    @classmethod
    def observe_attribute(cls, attr, collection=False):
        """
        Attach some event handlers on sqlalchemy attribute to handle delete_orphan option.

        """

        if attr not in _observing_attributes:
            _observing_attributes.add(attr)

            # noinspection PyUnusedLocal
            def on_set_attr(target, value, old_value, initiator):
                if old_value is None or old_value in (symbol('NEVER_SET'), symbol('NO_VALUE')):
                    return

                store_manager = StoreManager.get_current_store_manager()
                if store_manager.delete_orphan:
                    if value is not old_value:
                        if collection:
                            if isinstance(old_value, dict):
                                store_manager.orphaned(*(set(old_value.values()) - set(value.values())))
                            else:
                                store_manager.orphaned(*(set(old_value) - set(value)))
                        else:
                            store_manager.orphaned(old_value)

            event.listen(attr, 'set', on_set_attr, propagate=True)
