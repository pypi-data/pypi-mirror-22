# -*- coding: utf-8 -*-
# launcher.py
# Copyright (C) 2013-2017 LEAP
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Platform-independent VPN launcher interface.
"""

import getpass
import hashlib
import os
import stat

from twisted.logger import Logger

from abc import ABCMeta, abstractmethod
from functools import partial

from leap.bitmask.vpn.constants import IS_LINUX
from leap.bitmask.vpn.utils import force_eval


log = Logger()


flags_STANDALONE = False


class VPNLauncherException(Exception):
    pass


class OpenVPNNotFoundException(VPNLauncherException):
    pass


def _has_updown_scripts(path, warn=True):
    """
    Checks the existence of the up/down scripts and its
    exec bit if applicable.

    :param path: the path to be checked
    :type path: str

    :param warn: whether we should log the absence
    :type warn: bool

    :rtype: bool
    """
    is_file = os.path.isfile(path)
    if warn and not is_file:
        log.error('Could not find up/down script %s. '
                  'Might produce DNS leaks.' % (path,))

    # XXX check if applies in win
    is_exe = False
    try:
        is_exe = (stat.S_IXUSR & os.stat(path)[stat.ST_MODE] != 0)
    except OSError as e:
        log.warn("%s" % (e,))
    if warn and not is_exe:
        log.error('Up/down script %s is not executable. '
                  'Might produce DNS leaks.' % (path,))
    return is_file and is_exe


def _has_other_files(path, warn=True):
    """
    Check the existence of other important files.

    :param path: the path to be checked
    :type path: str

    :param warn: whether we should log the absence
    :type warn: bool

    :rtype: bool
    """
    is_file = os.path.isfile(path)
    if warn and not is_file:
        log.warn('Could not find file during checks: %s. ' % (
                 path,))
    return is_file


class VPNLauncher(object):
    """
    Abstract launcher class
    """
    __metaclass__ = ABCMeta

    UPDOWN_FILES = None
    OTHER_FILES = None
    UP_SCRIPT = None
    DOWN_SCRIPT = None

    PREFERRED_PORTS = ("443", "80", "53", "1194")

    # FIXME -- dead code?
    @classmethod
    @abstractmethod
    def get_gateways(kls, vpnconfig, providerconfig):
        """
        Return a list with the selected gateways for a given provider, looking
        at the VPN config file.
        Each item of the list is a tuple containing (gateway, port).

        :param vpnconfig: vpn configuration object
        :type vpnconfig: VPNConfig

        :param providerconfig: provider specific configuration
        :type providerconfig: ProviderConfig

        :rtype: list
        """
        gateways = []

        settings = Settings()
        domain = providerconfig.get_domain()
        gateway_conf = settings.get_selected_gateway(domain)
        gateway_selector = VPNGatewaySelector(vpnconfig)

        if gateway_conf == GATEWAY_AUTOMATIC:
            gws = gateway_selector.get_gateways()
        else:
            gws = [gateway_conf]

        if not gws:
            log.error('No gateway was found!')
            raise VPNLauncherException('No gateway was found!')

        for idx, gw in enumerate(gws):
            ports = vpnconfig.get_gateway_ports(idx)

            the_port = "1194"  # default port

            # pick the port preferring this order:
            for port in kls.PREFERRED_PORTS:
                if port in ports:
                    the_port = port
                    break
                else:
                    continue

            gateways.append((gw, the_port))

        log.debug('Using gateways (ip, port): {0!r}'.format(gateways))
        return gateways

    @classmethod
    @abstractmethod
    def get_vpn_command(kls, vpnconfig, providerconfig,
                        socket_host, socket_port, remotes, openvpn_verb=1):
        """
        Return the platform-dependant vpn command for launching openvpn.

        Might raise:
            OpenVPNNotFoundException,
            VPNLauncherException.

        :param vpnconfig: vpn configuration object
        :type vpnconfig: VPNConfig
        :param providerconfig: provider specific configuration
        :type providerconfig: ProviderConfig
        :param socket_host: either socket path (unix) or socket IP
        :type socket_host: str
        :param socket_port: either string "unix" if it's a unix socket,
                            or port otherwise
        :type socket_port: str
        :param openvpn_verb: the openvpn verbosity wanted
        :type openvpn_verb: int

        :return: A VPN command ready to be launched.
        :rtype: list
        """
        # leap_assert_type(vpnconfig, VPNConfig)
        # leap_assert_type(providerconfig, ProviderConfig)

        # XXX this still has to be changed on osx and windows accordingly
        # kwargs = {}
        # openvpn_possibilities = which(kls.OPENVPN_BIN, **kwargs)
        # if not openvpn_possibilities:
        #     raise OpenVPNNotFoundException()
        # openvpn = first(openvpn_possibilities)
        # -----------------------------------------
        openvpn_path = force_eval(kls.OPENVPN_BIN_PATH)

        if not os.path.isfile(openvpn_path):
            log.warn('Could not find openvpn bin in path %s' % (
                     openvpn_path))
            raise OpenVPNNotFoundException()

        args = []

        args += [
            '--setenv', "LEAPOPENVPN", "1",
            '--nobind'
        ]

        if openvpn_verb is not None:
            args += ['--verb', '%d' % (openvpn_verb,)]

        # gateways = kls.get_gateways(vpnconfig, providerconfig)
        gateways = remotes

        for ip, port in gateways:
            args += ['--remote', ip, port, 'udp']

        args += [
            '--client',
            '--dev', ' tun',
            '--persist-key',
            '--tls-client',
            '--remote-cert-tls',
            'server'
        ]

        openvpn_configuration = vpnconfig.get_openvpn_configuration()
        for key, value in openvpn_configuration.items():
            if type(value) is bool:
                if value:
                    args += ['--%s' % (key,)]
            else:
                args += ['--%s' % (key,), value]

        user = getpass.getuser()

        if socket_port == "unix":  # that's always the case for linux
            args += [
                '--management-client-user', user
            ]

        args += [
            '--management-signal',
            '--management', socket_host, socket_port,
            '--script-security', '2'
        ]

        if kls.UP_SCRIPT is not None:
            if _has_updown_scripts(kls.UP_SCRIPT):
                args += [
                    '--up', '\"%s\"' % (kls.UP_SCRIPT,),
                ]

        if kls.DOWN_SCRIPT is not None:
            if _has_updown_scripts(kls.DOWN_SCRIPT):
                args += [
                    '--down', '\"%s\"' % (kls.DOWN_SCRIPT,)
                ]

        args += [
            '--cert', vpnconfig.get_client_cert_path(providerconfig),
            '--key', vpnconfig.get_client_cert_path(providerconfig),
            '--ca', providerconfig.get_ca_cert_path()
        ]

        args += [
            '--ping', '5',
            '--ping-restart', '10']

        args += [
            '--persist-key',
            '--persist-local-ip', '--persist-remote-ip']

        command_and_args = [openvpn_path] + args
        return command_and_args

    @classmethod
    def missing_updown_scripts(kls):
        """
        Return what updown scripts are missing.

        :rtype: list
        """
        # FIXME
        # XXX remove method when we ditch UPDOWN in osx and win too
        if IS_LINUX:
            return []
        else:
            # leap_assert(kls.UPDOWN_FILES is not None,
            #             "Need to define UPDOWN_FILES for this particular "
            #             "launcher before calling this method")
            # TODO assert vs except?
            if kls.UPDOWN_FILES is None:
                raise Exception(
                    "Need to define UPDOWN_FILES for this particular "
                    "launcher before calling this method")
            file_exist = partial(_has_updown_scripts, warn=False)
            zipped = zip(kls.UPDOWN_FILES, map(file_exist, kls.UPDOWN_FILES))
            missing = filter(lambda (path, exists): exists is False, zipped)
            return [path for path, exists in missing]

    @classmethod
    def missing_other_files(kls):
        """
        Return what other important files are missing during startup.
        Same as missing_updown_scripts but does not check for exec bit.

        :rtype: list
        """
        if kls.OTHER_FILES is None:
            raise Exception(
                "Need to define OTHER_FILES for this particular "
                "auncher before calling this method")

        other = force_eval(kls.OTHER_FILES)
        file_exist = partial(_has_other_files, warn=False)

        if flags_STANDALONE:
            try:
                from leap.bitmask import _binaries
            except ImportError:
                raise RuntimeError(
                    "Could not find binary hash info in this bundle!")

            _, bitmask_root_path, openvpn_bin_path = other

            check_hash = _has_expected_binary_hash
            openvpn_hash = _binaries.OPENVPN_BIN
            bitmask_root_hash = _binaries.BITMASK_ROOT

            correct_hash = (
                True,  # we do not check the polkit file
                check_hash(bitmask_root_path, bitmask_root_hash),
                check_hash(openvpn_bin_path, openvpn_hash))

            zipped = zip(other, map(file_exist, other), correct_hash)
            missing = filter(
                lambda (path, exists, hash_ok): (
                    exists is False or hash_ok is False),
                zipped)
            return [path for path, exists, hash_ok in missing]
        else:
            zipped = zip(other, map(file_exist, other))
            missing = filter(lambda (path, exists): exists is False, zipped)
            return [path for path, exists in missing]


def _has_expected_binary_hash(path, expected_hash):
    """
    Check if the passed path matches the expected hash.

    Used from within the bundle, to know if we have to reinstall the shipped
    binaries into the system path.

    This path will be /usr/local/sbin for linux.

    :param path: the path to check.
    :type path: str
    :param expected_hash: the sha256 hash that we expect
    :type expected_hash: str
    :rtype: bool
    """
    try:
        with open(path) as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()
        return expected_hash == file_hash
    except IOError:
        return False
