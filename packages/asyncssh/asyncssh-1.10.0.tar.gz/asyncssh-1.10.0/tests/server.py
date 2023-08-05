# Copyright (c) 2016-2017 by Ron Frederick <ronf@timeheart.net>.
# All rights reserved.
#
# This program and the accompanying materials are made available under
# the terms of the Eclipse Public License v1.0 which accompanies this
# distribution and is available at:
#
#     http://www.eclipse.org/legal/epl-v10.html
#
# Contributors:
#     Ron Frederick - initial implementation, API, and documentation

"""SSH server used for unit tests"""

import asyncio
import os
import shutil
import signal
import socket
import subprocess

import asyncssh
from asyncssh.misc import async_context_manager

from .util import run, AsyncTestCase


class Server(asyncssh.SSHServer):
    """Unit test SSH server"""

    def __init__(self):
        self._conn = None

    def connection_made(self, conn):
        """Record connection object for later use"""

        self._conn = conn

    def begin_auth(self, username):
        """Handle client authentication request"""

        return username != 'guest'


class ServerTestCase(AsyncTestCase):
    """Unit test class which starts an SSH server and agent"""

    # Pylint doesn't like mixed case method names, but this was chosen to
    # match the convention used in the unittest module.

    # pylint: disable=invalid-name

    _server = None
    _server_addr = None
    _server_port = None
    _agent_pid = None

    @classmethod
    @asyncio.coroutine
    def create_server(cls, server_factory=(), *, loop=(),
                      server_host_keys=(), **kwargs):
        """Create an SSH server for the tests to use"""

        if loop is ():
            loop = cls.loop

        if server_factory is ():
            server_factory = Server

        if server_host_keys is ():
            server_host_keys = ['skey']

        return (yield from asyncssh.create_server(
            server_factory, port=0, family=socket.AF_INET, loop=loop,
            server_host_keys=server_host_keys, **kwargs))

    @classmethod
    @asyncio.coroutine
    def start_server(cls):
        """Start an SSH server for the tests to use"""

        return (yield from cls.create_server())

    @classmethod
    @asyncio.coroutine
    def asyncSetUpClass(cls):
        """Set up keys, an SSH server, and an SSH agent for the tests to use"""

        ckey_dsa = asyncssh.generate_private_key('ssh-dss')
        ckey_dsa.write_private_key('ckey_dsa')
        ckey_dsa.write_public_key('ckey_dsa.pub')

        ckey = asyncssh.generate_private_key('ssh-rsa')
        ckey.write_private_key('ckey')
        ckey.write_public_key('ckey.pub')

        ckey_cert = ckey.generate_user_certificate(ckey, 'name')
        ckey_cert.write_certificate('ckey-cert.pub')

        skey = asyncssh.generate_private_key('ssh-rsa')
        skey.write_private_key('skey')
        skey.write_public_key('skey.pub')

        skey_cert = skey.generate_host_certificate(skey, 'name')
        skey_cert.write_certificate('skey-cert.pub')

        exp_cert = skey.generate_host_certificate(skey, 'name',
                                                  valid_after='-2d',
                                                  valid_before='-1d')
        skey.write_private_key('exp_skey')
        exp_cert.write_certificate('exp_skey-cert.pub')

        for f in ('ckey_dsa', 'ckey', 'skey', 'exp_skey'):
            os.chmod(f, 0o600)

        os.mkdir('.ssh', 0o700)

        shutil.copy('ckey_dsa', os.path.join('.ssh', 'id_dsa'))
        shutil.copy('ckey_dsa.pub', os.path.join('.ssh', 'id_dsa.pub'))
        shutil.copy('ckey', os.path.join('.ssh', 'id_rsa'))
        shutil.copy('ckey.pub', os.path.join('.ssh', 'id_rsa.pub'))

        with open('authorized_keys', 'w') as auth_keys:
            auth_keys.write('cert-authority,principals="ckey" ')

            with open('ckey.pub') as ckey_pub:
                shutil.copyfileobj(ckey_pub, auth_keys)

            auth_keys.write('permitopen=":*" ')

            with open('ckey.pub') as ckey_pub:
                shutil.copyfileobj(ckey_pub, auth_keys)

            with open('ckey_dsa.pub') as ckey_dsa_pub:
                shutil.copyfileobj(ckey_dsa_pub, auth_keys)

        cls._server = yield from cls.start_server()

        sock = cls._server.sockets[0]
        cls._server_addr = '127.0.0.1'
        cls._server_port = sock.getsockname()[1]

        with open(os.path.join('.ssh', 'known_hosts'), 'w') as known_hosts:
            known_hosts.write('[%s]:%s ' % (cls._server_addr,
                                            cls._server_port))

            with open('skey.pub') as skey_pub:
                shutil.copyfileobj(skey_pub, known_hosts)

        os.environ['LOGNAME'] = 'guest'
        os.environ['HOME'] = '.'

        if 'DISPLAY' in os.environ: # pragma: no cover
            del os.environ['DISPLAY']
        if 'SSH_ASKPASS' in os.environ: # pragma: no cover
            del os.environ['SSH_ASKPASS']
        if 'SSH_AUTH_SOCK' in os.environ: # pragma: no cover
            del os.environ['SSH_AUTH_SOCK']
        if 'XAUTHORITY' in os.environ: # pragma: no cover
            del os.environ['XAUTHORITY']

        try:
            output = run('ssh-agent -a agent 2>/dev/null')
        except subprocess.CalledProcessError: # pragma: no cover
            cls._agent_pid = None
        else:
            cls._agent_pid = int(output.splitlines()[2].split()[3][:-1])

            os.environ['SSH_AUTH_SOCK'] = 'agent'

            agent = yield from asyncssh.connect_agent()
            yield from agent.add_keys([ckey_dsa, (ckey, ckey_cert)])
            agent.close()

    @classmethod
    @asyncio.coroutine
    def asyncTearDownClass(cls):
        """Shut down test server and agent"""

        # Wait a bit for existing tasks to exit
        yield from asyncio.sleep(1)

        cls._server.close()
        yield from cls._server.wait_closed()

        if cls._agent_pid: # pragma: no branch
            os.kill(cls._agent_pid, signal.SIGTERM)

    # pylint: enable=invalid-name

    def agent_available(self):
        """Return whether SSH agent is available"""

        return bool(self._agent_pid)

    @asyncio.coroutine
    def create_connection(self, client_factory, loop=(), **kwargs):
        """Create a connection to the test server"""

        if loop is ():
            loop = self.loop

        return (yield from asyncssh.create_connection(client_factory,
                                                      self._server_addr,
                                                      self._server_port,
                                                      loop=loop, **kwargs))

    @async_context_manager
    def connect(self, **kwargs):
        """Open a connection to the test server"""

        conn, _ = yield from self.create_connection(None, **kwargs)

        return conn
