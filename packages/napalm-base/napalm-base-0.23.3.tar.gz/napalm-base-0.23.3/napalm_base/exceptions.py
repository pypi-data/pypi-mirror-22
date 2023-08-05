# Copyright 2015 Spotify AB. All rights reserved.
#
# The contents of this file are licensed under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with the
# License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

# Python3 support
from __future__ import print_function
from __future__ import unicode_literals


class ModuleImportError(Exception):
    pass


class ConnectionException(Exception):
    pass


class ReplaceConfigException(Exception):
    pass


class MergeConfigException(Exception):
    pass


class SessionLockedException(Exception):
    pass


class CommandTimeoutException(Exception):
    pass


class CommandErrorException(Exception):
    pass


class DriverTemplateNotImplemented(Exception):
    pass


class TemplateNotImplemented(Exception):
    pass


class TemplateRenderException(Exception):
    pass


class ValidationException(Exception):
    pass
