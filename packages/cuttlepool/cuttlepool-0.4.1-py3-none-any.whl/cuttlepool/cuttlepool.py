# -*- coding: utf-8 -*-
"""
Cuttle Pool class.

:license: MIT, see LICENSE for details.
"""
try:
    import queue
except ImportError:
    import Queue as queue
import sys
import threading
import warnings


class CuttlePool(object):
    """
    A connection pool for SQL databases.

    :param func connect: The ``connect`` function of the chosen sql driver.
    :param int capacity: Max number of connections in pool. Defaults to ``5``.
    :param int timeout: Time in seconds to wait for connection. Defaults to
                        ``None``.
    :param int overflow: The number of extra connections that can be made if
                         the pool is exhausted. Defaults to ``1``.
    :param \**kwargs: Connection arguments for the underlying database
                      connector.

    :raises ValueError: If capacity <= 0 or overflow < 0.
    :raises Empty: If ``pool`` does not return a connection within ``timeout``
                   seconds.
    """

    def __init__(self, connect, capacity=5,
                 overflow=1, timeout=None, **kwargs):
        if capacity <= 0:
            raise ValueError('connection pool requires a capacity of 1+ '
                             'connections')
        if overflow < 0:
            raise ValueError('pool overflow must be non negative')

        self._connect = connect
        self._connection_arguments = kwargs

        self._capacity = capacity
        self._overflow = overflow
        self._timeout = timeout

        self._pool = queue.Queue(self._capacity)
        self._reference_pool = []
        self._Connection = None

    def __del__(self):
        try:
            self._close_connections()
        except:
            pass

    @property
    def _maxsize(self):
        return self._capacity + self._overflow

    @property
    def _size(self):
        return len(self._reference_pool)

    @property
    def connection_arguments(self):
        return {k: v for k, v in self._connection_arguments.items()}

    def _make_connection(self):
        """
        Returns a connection object.
        """
        connection = self._connect(**self._connection_arguments)

        if self._Connection is None:
            self._Connection = type(connection)

        self._reference_pool.append(connection)

        return connection

    def _harvest_lost_connections(self):
        """
        Returns lost connections to pool.
        """
        # A connection should be referenced by 3 things at any given time, the
        # _reference_pool, a PoolConnection or the _pool, and sys.getrefcount
        # (it's referenced by sys.getrefcount when sys.getrefcount is called).
        # If the refcount is less than 3 this means it's only referenced by
        # _reference_pool and sys.getrefcount and should be returned to the
        # pool.
        with threading.RLock():
            for idx in range(self._size):
                if sys.getrefcount(self._reference_pool[idx]) < 3:
                    self.put_connection(self._reference_pool[idx])

    def _close_connections(self):
        """
        Closes all connections associated with the pool.
        """
        with threading.RLock():
            for con in self._reference_pool:
                try:
                    con.close()
                except:
                    pass

            while not self._pool.empty():
                try:
                    self._pool.get_nowait()
                except queue.Empty:
                    break

            self._reference_pool = []

    def empty_pool(self):
        """
        Removes all connections associated with the pool.
        """
        self._close_connections()

    def get_connection(self):
        """
        Returns a ``PoolConnection`` object.

        :return: A ``PoolConnection`` object.

        :raises AttributeError: If attempt to get connection times out.
        """
        with threading.RLock():

            if self._pool.empty():
                self._harvest_lost_connections()

            try:
                connection = self._pool.get_nowait()

            except:

                if self._size < self._maxsize:
                    connection = self._make_connection()

                else:
                    try:
                        connection = self._pool.get(timeout=self._timeout)
                    except queue.Empty:
                        raise AttributeError('could not get connection, the '
                                             'pool is depleted')

            if not self.ping(connection):
                self._reference_pool.remove(connection)
                connection = self._make_connection()

            self.normalize_connection(connection)

            return PoolConnection(connection, self)

    def normalize_connection(self, connection):
        """
        A user implemented function that resets the properties of the
        ``Connection`` object. This prevents unwanted behavior from a
        connection retrieved from the pool as it could have been changed when
        previously used.

        :param obj connection: A ``Connection`` object.
        """
        warnings.warn('Failing to implement `normalize_connection()` can '
                      'result in unwanted behavior.')

    def ping(self, connection):
        """
        A user implemented function that ensures the ``Connection`` object is
        open.

        :param obj connection: A ``Connection`` object.

        :return: A bool indicating if the connection is open (``True``) or
                 closed (``False``).
        """
        warnings.warn('Failing to implement `ping()` can result in unwanted '
                      'behavior.')
        return True

    def put_connection(self, connection):
        """
        Adds a connection back to the pool.

        :param connection: A connection object.

        :raises ValueError: If improper connection object.
        """
        with threading.RLock():
            if not isinstance(connection, self._Connection):
                raise ValueError('improper connection object')

            if connection not in self._reference_pool:
                raise ValueError('connection returned to pool was not created '
                                 'by pool')

            try:
                self._pool.put_nowait(connection)

            except queue.Full:
                self._reference_pool.remove(connection)

                try:
                    connection.close()
                except Exception:
                    pass


class PoolConnection(object):
    """
    A wrapper around a connection object.

    :param connection: A connection object.
    :param pool: A connection pool.

    :raises AttributeError: If improper connection object or improper pool
                            object.
    """

    def __init__(self, connection, pool):
        if not isinstance(pool, CuttlePool):
            raise AttributeError('improper pool object')
        if not isinstance(connection, pool._Connection):
            raise AttributeError('improper connection object')

        self._connection = connection
        self._pool = pool

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def __getattr__(self, attr):
        """
        Gets attributes of connection object.
        """
        if attr != 'close':
            return getattr(self._connection, attr)

    def __setattr__(self, attr, value):
        """Sets attributes of connection object."""
        if attr not in ['close', '_connection', '_pool']:
            return setattr(self._connection, attr, value)

        if attr != 'close':
            self.__dict__[attr] = value

    def close(self):
        """
        Returns the connection to the connection pool.
        """
        if isinstance(self._connection, self._pool._Connection):
            self._pool.put_connection(self._connection)
            self._connection = None
            self._pool = None
