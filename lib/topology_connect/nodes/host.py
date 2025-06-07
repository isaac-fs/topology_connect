# -*- coding: utf-8 -*-
#
# Copyright (C) 2015-2016 Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""
topology_connect base node module.
"""

from __future__ import unicode_literals, absolute_import
from __future__ import print_function, division

from logging import getLogger

from ..node import CommonConnectNode
from ..shell import SshBashShell


log = getLogger(__name__)


class HostNode(CommonConnectNode):
    """
    FIXME: Document.
    """

    def __init__(
        self,
        identifier,
        identity_file="id_rsa",
        options=None,
        user=None,
        password=None,
        port=22,
        **kwargs,
    ):
        if identity_file and password:
            raise Exception("Cannot use both identity_file and password options")

        if options is None:
            options = ()

        if password:
            options = options + ("BatchMode=no",)
        else:
            options = options + ("BatchMode=yes",)

        super(HostNode, self).__init__(identifier, **kwargs)
        self._register_shell(
            "bash",
            SshBashShell(
                initial_prompt=[r"\w+@.+:.+[#$] ", r"bash-.+[#$] ", r"\w+:.*[#$] "],
                hostname=self._fqdn,
                identity_file=identity_file,
                options=options,
                user=user,
                password=password,
                port=port,
            ),
        )


class UncheckedHostNode(CommonConnectNode):
    """
    FIXME: Document.
    """

    def __init__(
        self,
        identifier,
        identity_file=None,
        options=None,
        port=22,
        user=None,
        password=None,
        **kwargs,
    ):
        if identity_file and password:
            raise Exception("Cannot use both identity_file and password options")

        if options is None:
            options = ("StrictHostKeyChecking=no", "UserKnownHostsFile=/dev/null")
        else:
            options = options + ("StrictHostKeyChecking=no", "UserKnownHostsFile=none")

        if password:
            options = options + ("BatchMode=no",)
        else:
            options = options + ("BatchMode=yes",)

        super(UncheckedHostNode, self).__init__(identifier, **kwargs)
        self._register_shell(
            "bash",
            SshBashShell(
                initial_prompt=[r"\w+@.+:.+[#$] ", r"bash-.+[#$] ", r"\w+:.*[#$] "],
                hostname=self._fqdn,
                identity_file=identity_file,
                options=options,
                user=user,
                password=password,
                port=port,
            ),
        )


__all__ = ["HostNode", "UncheckedHostNode"]
