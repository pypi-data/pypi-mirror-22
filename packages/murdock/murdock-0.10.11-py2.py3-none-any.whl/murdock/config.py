# -*- coding: utf-8 -*-
#
#   This file is part of the Murdock project.
#
#   Copyright 2016 Malte Lichtner
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

"""
Module `murdock.config`
-----------------------

Registration of runtime configuration options. In the spirit of the modularity
and extensibility of Murdock, all configuration options needed by a certain
part of the software are registered directly in the corresponding module which
needs them. Options needed to set up a docking, for example, are defined in the
`~murdock.runner.docking` module, whereas parameters for the `Particle Swarm`
search algorithm are declared in the `murdock.search.ps` module. To that end,
these modules all contain a configuration class named `ConfigDeclaration` (e.g.
`murdock.runner.docking.ConfigDeclaration` or
`murdock.search.ps.ConfigDeclaration`). For each configuration item which is a
dictionary or a list, there is a method with the same name. The expected
configuration options for the top-level item ``"docking"``, for example, are
defined in the method `murdock.runner.docking.ConfigDeclaration.docking`.  That
method returns a list of `.ConfigOption` instances, one for each item in the
dictionary ``"docking"``.

Each `.ConfigOption` has a `~.ConfigOption.name`, a
`~.ConfigOption.dtype`, a short `~.ConfigOption.description` and, optionally, a
`~.ConfigOption.default` value (used if the option is not present in the
configuration file) and a `~.ConfigOption.required` switch, which can be set to
``False`` (default is ``True``) to supress an error during the configuration
validation if the item is not present in the file and has no
`~.ConfigOption.default` value.

If an option is a dictionary or a list, its own items are returned by another
method with the corresponding name. For the item ``"receptor"`` in
``"docking"``, for example, the options are returned by the method
`~murdock.runner.docking.ConfigDeclaration.receptor` (also defined in the
`murdock.runner.docking` because the option is needed by the
`~murdock.runner.docking.Docking` class). The method used to find the module
corresponding to a certain configuration item is described in
`~murdock.runner.runner.Configuration`.

.. seealso:: `~murdock.runner.runner.Configuration`

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from past.builtins import basestring

import murdock.misc


class ConfigOption(object):
    """A class to store information on a configuration option.
    """

    def __init__(
            self, name, dtype, description=None, default=None, required=True,
            validate=True, check_filepath=False, choices=None, length=None):
        #: name (tag)
        self.name = name
        #: data type
        self.dtype = dtype
        #: short description (for parsing error output)
        self.description = description
        #: default value
        self.default = default
        #: the required number of items (checked for lists and dictionaries)
        self.length = length
        #: whether the option is required (only checked if default is None)
        self.required = required
        #: whether the content of this option should be validated
        self.validate = validate
        #: whether to check if this option is the path to an existing file
        self.check_filepath = check_filepath
        #: a tuple of allowed values (or None if all values are allowed)
        self.choices = choices
        if self.dtype not in (dict, list) and self.length is not None:
            raise AttributeError(
                'The attribute `length` can only be set if `dtype` is either '
                '`list` or `dict`.')

    def __str__(self):
        s = (
            'Configuration option:\n   Name: `%s`\n   Type: %s\n'
            '   Description: %s\n   Default: %s\n   Required: %s\n'
            '   Validate: %s\n' % (
                self.name, self.dtype, self.description, self.default,
                self.required, self.validate))
        if self.check_filepath:
            s = '%s   Check filepath: %s\n' % (s, self.check_filepath)
        if self.choices is not None:
            s = '%s   Choices: %s\n' % (s, ', '.join(self.choices))
        return s

    @staticmethod
    def float_ge_zero(val):
        f = murdock.misc.finitefloat(val)
        if f < 0:
            raise ValueError
        return f

    @staticmethod
    def float_gt_zero(val):
        f = ConfigOption.float_ge_zero(val)
        if f == 0:
            raise ValueError
        return f

    @staticmethod
    def float_le_zero(val):
        f = murdock.misc.finitefloat(val)
        if f > 0:
            raise ValueError
        return f

    @staticmethod
    def float_lt_zero(val):
        f = ConfigOption.float_le_zero(val)
        if f == 0:
            raise ValueError
        return f

    @staticmethod
    def int_ge_zero(val):
        i = int(val)
        if i < 0 or float(val) != i:
            raise ValueError
        return i

    @staticmethod
    def int_gt_zero(val):
        i = ConfigOption.int_ge_zero(val)
        if i == 0:
            raise ValueError
        return i

    @staticmethod
    def int_le_zero(val):
        i = int(val)
        if i > 0 or float(val) != i:
            raise ValueError
        return i

    @staticmethod
    def int_lt_zero(val):
        i = ConfigOption.int_le_zero(val)
        if i == 0:
            raise ValueError
        return i

    @staticmethod
    def string(val):
        if not isinstance(val, basestring):
            raise ValueError
        return val


class ConfigDeclaration(object):
    """Parent class for all configuration option declarations.

    This class is used in other modules to register their own configuration
    options.

    """

    def get_default_options(self):
        """Default configuration options:

        - "notes":
            a list of notes which may be added to any part of the
            configuration file; it is not validated and may have an arbitrary
            (also nested) structure `(dtype=list, required=False,
            validate=False)`

        """
        opt = []
        opt.append(ConfigOption(
            name='notes', dtype=list, description='list of notes',
            required=False, validate=False))
        return opt
