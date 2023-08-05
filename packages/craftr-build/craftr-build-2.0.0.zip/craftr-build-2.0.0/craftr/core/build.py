# The Craftr build system
# Copyright (C) 2016  Niklas Rosenstein
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
:mod:`craftr.core.build`
========================

This module provides all the API to generate a Ninja build manifest.
"""

from craftr import platform
from craftr.utils import argspec
from craftr.utils import path
from craftr.utils import pyutils
from craftr.utils import shell
from craftr.utils.singleton import Default
from ninja_syntax import Writer as NinjaWriter

import abc
import base64
import lzma
import ninja_syntax
import os
import pickle
import re
import stat
import sys


class DuplicateOutputError(Exception):
  """
  This exception is raised if the same output file would be built by
  multiple targets.
  """

  def __init__(self, filename, new_target, target):
    self.filename = filename
    self.new_target = new_target
    self.target = target

  def __str__(self):
    return '"{}" produced by {} and {}'.format(self.filename,
        self.new_target.name, self.target.name)


class Graph(object):
  """
  This class represents the whole build graph which is generated from
  targets reference input and output files. After a :class:`Target` is
  created, it must be added to a Graph with the :meth:`add_target` method.

  Note that all filenames in the Graph are absolute and normalized with
  the :func:`path.norm` function.

  .. attribute:: tasks

    Read-only. A dictionary of all :class:`Tasks<Task>` that have been
    added to the Graph.

  .. attribute:: target

    Read-only. A dictionary of all the :class:`Targets<Target>` that have
    been added to the Graph.

  .. attribute:: infiles

    Read-only. A dictionary that maps normalized filenames of input files
    to a list of :class:`Targets<Target>`.

  .. attribute:: outfiles

    Read-only. A dictionary that maps normalized filenames of output files
    to the :class:`Target` that creates it.

  .. attributes:: vars

    A dictionary of variables that will be exported to the Ninja manifest.
  """

  def __init__(self):
    self.tasks = {}
    self.targets = {}
    self.infiles = {}
    self.outfiles = {}
    self.vars = {}
    self.tools = {}

  def add_tool(self, tool):
    """
    Add a :class:`Tool` to the Graph.

    :raise ValueError: If the :attr:`Tool.name` is already used.
    """

    if tool.name in self.tools:
      raise ValueError('a tool with the name {!r} already exists'
          .format(tool.name))
    self.tools[tool.name] = tool

  def add_target(self, target):
    """
    Add a :class:`Target` to the Graph.

    .. note:: For performance reasons, this method assumes that all paths
              in the *target* are already normalized with :meth:`path.norm`.

    :raise ValueError: If the :attr:`Target.name` is already used.
    :raise DuplicateOutputError: If the *target* lists an output file that
      is already created by another target.
    """

    argspec.validate('target', target, {'type': Target})
    if target.name in self.targets:
      raise ValueError('a target with the name {!r} already exists'
        .format(target.name))
    self.targets[target.name] = target
    for infile in target.inputs:
      self.infiles.setdefault(infile, []).append(target)
    for outfile in target.outputs:
      other = self.outfiles.setdefault(outfile, target)
      if other is not target:
        raise DuplicateOutputError(outfile, target, other)

  def add_task(self, task, **kwargs):
    """
    Add a :class:`Task` to the Graph. Creates a :class:`Target` for the task
    and returns it.

    :param task: The :class:`Task` to add to the Graph.
    :param kwargs: Additional parameters for the :class:`Target` constructor.
    """

    argspec.validate('task', task, {'type': Task})
    if task.name in self.tasks:
      raise ValueError('a task with the name {!r} already exists'
        .format(task.name))

    target = Target(task.name, [task.get_command()], task = task, **kwargs)
    assert target.task is task
    self.add_target(target)
    self.tasks[task.name] = task
    return target


  def export(self, writer, context, platform):
    """
    Export the build graph to a Ninja manifest.

    :param writer: A :class:`ninja_syntax.Writer` object.
    :param context: A :class:`ExportContext` object.
    :param platform: A :class:`PlatformHelper` instance.
    """

    argspec.validate('writer', writer, {"type": ninja_syntax.Writer})
    writer.comment('This file was automatically generated with Craftr.')
    writer.comment('It is not recommended to edit this file manually.')
    writer.newline()

    if self.vars:
      for key, value in self.vars.items():
        writer.variable(key, value)
      writer.newline()

    if self.tools:
      writer.comment('Tools')
      writer.comment('-----')
      for tool in self.tools.values():
        tool.export(writer, context, platform)
      writer.newline()

    defaults = []
    for target in self.targets.values():
      if not target.explicit and target.generates_build_instruction:
        defaults.append(target.name)
      target.export(writer, context, platform)

    if defaults:
      writer.default(defaults)

class Target(object):
  """
  A higher level abstraction of a Target that can be added to a :class:`Graph`
  and then exported into a Ninja build manifest. A target should be treated
  as read-only always.
  """

  def __init__(self, name, commands, inputs, outputs, implicit_deps=(),
               order_only_deps=(), pool=None, deps=None, depfile=None,
               msvc_deps_prefix=None, explicit=False, foreach=False,
               description=None, metadata=None, cwd=None, environ=None,
               frameworks=(), task=None, runprefix=None):
    argspec.validate('name', name, {'type': str})
    argspec.validate('commands', commands,
      {'type': list, 'allowEmpty': False, 'items':
        {'type': list, 'allowEmpty': False, 'items': {'type': [Tool, Target, str]}}})
    argspec.validate('inputs', inputs, {'type': [list, tuple], 'items': {'type': [Target, str]}})
    argspec.validate('outputs', outputs, {'type': [list, tuple], 'items': {'type': str}})
    argspec.validate('implicit_deps', implicit_deps, {'type': [list, tuple], 'items': {'type': [Target, str]}})
    argspec.validate('order_only_deps', order_only_deps, {'type': [list, tuple], 'items': {'type': [Target, str]}})
    argspec.validate('pool', pool, {'type': [None, str]})
    argspec.validate('deps', deps, {'type': [None, str], 'enum': ['msvc', 'gcc']})
    argspec.validate('depfile', depfile, {'type': [None, str]})
    argspec.validate('msvc_deps_prefix', msvc_deps_prefix, {'type': [None, str]})
    argspec.validate('explicit', explicit, {'type': bool})
    argspec.validate('foreach', foreach, {'type': bool})
    argspec.validate('description', description, {'type': [None, str]})
    argspec.validate('metadata', metadata, {'type': [None, dict]})
    argspec.validate('cwd', cwd, {'type': [None, str]})
    argspec.validate('environ', environ, {'type': [None, dict]})
    argspec.validate('frameworks', frameworks, {'type': [list, tuple], 'items': {'type': dict}})
    argspec.validate('task', task, {'type': [None, Task]})
    argspec.validate('runprefix', runprefix, {'type': [None, list, str], 'items': {'type': str}})

    if isinstance(runprefix, str):
      runprefix = shell.split(runprefix)
    elif runprefix is None:
      runprefix = []

    def expand_mixed_list(mixed, implicit_deps, mode):
      result = []
      for item in mixed:
        if isinstance(item, Target):
          if mode == 'implicit':
            names = [item.name]
          elif mode == 'inputs':
            names = item.outputs
          elif mode == 'cmd':
            names = [path.abs(x) for x in item.outputs]
          else:
            raise RuntimeError(mode)

          if implicit_deps is not None:
            implicit_deps += names
          result += names

        elif isinstance(item, Tool):
          result.append(str(item))

        elif isinstance(item, str):
          if mode != 'cmd':
            item = path.abs(item)
          result.append(item)

        else:
          raise RuntimeError

      return result

    self.implicit_deps = []
    self.inputs = expand_mixed_list(inputs, None, 'inputs')
    self.outputs = [path.abs(x) for x in outputs]
    self.commands = [expand_mixed_list(cmd, self.implicit_deps, 'cmd') for cmd in commands]
    self.implicit_deps += expand_mixed_list(implicit_deps, None, 'implicit')
    self.order_only_deps = expand_mixed_list(order_only_deps, None, 'implicit')

    self.name = name
    self.pool = pool
    self.deps = deps
    self.depfile = depfile
    self.msvc_deps_prefix = msvc_deps_prefix
    self.explicit = explicit
    self.foreach = foreach
    self.description = description
    self.metadata = metadata or {}
    self.cwd = cwd
    self.environ = environ or {}
    self.frameworks = frameworks
    self.task = task
    self.runprefix = runprefix

    if self.foreach and len(self.inputs) != len(self.outputs):
      raise ValueError('foreach target must have the same number of output '
        'files ({}) as input files ({})'.format(len(self.outputs),
        len(self.inputs)))

    if self.deps == 'gcc' and not self.depfile:
      raise ValueError('require depfile with deps="gcc"')

  def __str__(self):
    return '<{}.Target "{}">'.format(__name__, self.name)

  def __lshift__(self, other):
    """
    Adds *other* as an implicit dependency to the target.

    :param other: A :class:`Target` or :class:`str`.
    :return: ``self``
    """

    if isinstance(other, Target):
      self.implicit_deps += other.outputs
    elif isinstance(other, str):
      self.implicit_deps.append(path.norm(other))
    else:
      raise TypeError("Target.__lshift__() expected Target or str")
    return self

  def export(self, writer, context, platform):
    """
    Export the target to a Ninja manifest.
    """

    writer.comment("target: {}".format(self.name))
    writer.comment("--------" + "-" * len(self.name))
    commands = platform.prepare_commands(self.commands)

    # Check if we need to export a command file or can export the command
    # directly.
    if not self.environ and len(commands) == 1:
      commands = [platform.prepare_single_command(commands[0], self.cwd)]
    else:
      filename = path.join('.commands', self.name)
      command, __ = platform.write_command_file(filename, commands,
        self.inputs, self.outputs, cwd=self.cwd, environ=self.environ,
        foreach=self.foreach)
      commands = [command]

    assert len(commands) == 1
    command = shell.join(commands[0], for_ninja=True)

    writer.rule(self.name, command, pool=self.pool, deps=self.deps,
      depfile=self.depfile, description=self.description)

    if self.msvc_deps_prefix:
      # We can not write msvc_deps_prefix on the rule level with Ninja
      # versions older than 1.7.1. Write it global instead, but that *could*
      # lead to issues...
      indent = 1 if context.ninja_version > '1.7.1' else 0
      writer.variable('msvc_deps_prefix', self.msvc_deps_prefix, indent)

    writer.newline()
    if self.foreach:
      assert len(self.inputs) == len(self.outputs)
      for infile, outfile in zip(self.inputs, self.outputs):
        writer.build(
          [outfile],
          self.name,
          [infile],
          implicit=self.implicit_deps,
          order_only=self.order_only_deps)
    else:
      writer.build(
        self.outputs or [self.name],
        self.name,
        self.inputs,
        implicit=self.implicit_deps,
        order_only=self.order_only_deps)

    if self.outputs and self.name not in self.outputs:
      writer.build(self.name, 'phony', self.outputs)

  @property
  def generates_build_instruction(self):
    """
    Reading this property tells you whether the target produces at least one
    build in the Ninja manifest. This is used to determine whether a target is
    included in the list of default targets or not.
    """

    return not (self.foreach and not self.inputs)


class Tool(object):
  """
  This class represents a program that can be called by by the command in
  build rules. Usually this is only necessary if the tool requires a special
  environment.

  Depending on whether its necessary on the current platform, tools might be
  exported into shell scripts. The actual command to be called in the command
  can then be retrieved by converting the :class:`Tool` object to a string.

  .. attribute:: name

    The name of the tool. In a build :class:`Graph`, there may only be one tool
    associated with the same name.

  .. attribute:: command

    The command that is to be executed and to which the additional command-line
    arguments are forwarded to. Must be a list of strings.

  .. attribute:: preamble

    A list of commands/files that are to be sourced before the :attr:`command`
    can be executed.

  .. attribute:: environ

    A dictionary of environment variables that will be exported before the
    command or premable is executed.

  .. attribute:: exported_command

    After :meth:`exported_command` has been called, this member contains the
    command that was exported for the Tool. This is a single string.
  """

  def __init__(self, name, command, preamble=None, environ=None):
    argspec.validate('name', name, {'type': str})
    argspec.validate('command', command,
        {'type': [list, tuple], 'allowEmpty': False, 'items': {'type': str}})
    argspec.validate('preamble', preamble,
        {'type': [None, list, tuple], 'items':
          {'type': [list, tuple], 'allowEmpty': False, 'items': {'type': str}}})
    argspec.validate('environ', environ, {'type': [None, dict]})

    self.name = name
    self.command = list(command)
    self.preamble = preamble or []
    self.environ = environ or {}
    self.exported_command = None

  def __str__(self):
    """
    Returns the name of the command to execute the tool in Ninja. This is
    always a variable reference.
    """

    return '$CraftrTool_{}'.format(self.name.replace('.', '_'))

  def export(self, writer, context, platform):
    name = str(self)[1:]
    if not self.preamble and not self.environ:
      self.exported_command = shell.join(self.command)
    else:
      filename = path.join('.tools', name)
      command, filename = platform.write_command_file(
          filename, list(self.preamble) + [self.command], environ=self.environ,
          accept_additional_args=True)
      self.exported_command = shell.join(command)
    writer.variable(name, self.exported_command)


class Task(object):
  """
  Represents a task that can be executed via ``craftr run <task> <args...>``.
  A task is a Python function that accepts arguments from the command-line.
  """

  def __init__(self, name, func, args):
    self.name = name
    self.func = func
    self.args = args

  def __repr__(self):
    return '<Task {!r}>'.format(self.name)

  def get_command(self):
    return ['$Craftr_run_command', self.name] + self.pickle_args(self.args)

  def invoke(self, args):
    args = self.unpickle_args(args)
    return self.func(*args)

  @staticmethod
  def pickle_args(args):
    """
    Converts a list of arguments that may contain Python objects to a list of
    plain strings containing only printable characters. Python objects are
    pickled, compressed and then encoded in base64.
    """

    result = []
    for item in args:
      if isinstance(item, str):
        result.append(item)
      else:
        dump = pickle.dumps(item)
        result.append('pickle://' + base64.b64encode(lzma.compress(dump)).decode('ascii'))
    return result

  @staticmethod
  def unpickle_args(args):
    """
    Reverts :meth:`pickle_args`.
    """

    result = []
    for item in args:
      assert isinstance(item, str)
      if item.startswith('pickle://'):
        dump = lzma.decompress(base64.b64decode(item[9:]))
        result.append(pickle.loads(dump))
      else:
        result.append(item)
    return result


class ExportContext(object):
  """
  An instance of this class is required for :meth:`Graph.export` and
  :meth:`Target.export`. It provides additional information that can influence
  the exported manifest.

  .. attribute:: ninja_version
  """

  def __init__(self, ninja_version):
    self.ninja_version = ninja_version


class PlatformHelper(object, metaclass=abc.ABCMeta):
  """
  Interface to abstract platfrom dependent operations during the export
  process.
  """

  @abc.abstractmethod
  def prepare_commands(self, commands):
    """
    Passed a list of list of strings that represents the commands for
    a target. Return the same value or a modified value.
    """

  @abc.abstractmethod
  def prepare_single_command(self, command, cwd):
    """
    Given a single command as a list of strings and an optional working
    directory path, return an updated list of strings that serves as the
    new command including the current working directory switch.
    """

  @abc.abstractmethod
  def write_command_file(self, filename, commands, inputs=None, outputs=None,
      cwd=None, environ=None, foreach=False, suffix=Default, dry=False,
      accept_additional_args=False):
    """
    Writes a file that can be run by the native shell to execute the *commands*.
    If *suffix* is omitted, the default script suffix for the shell will be
    appended (which is especially important on Windows).

    References to ``$in`` and ``$out`` will be replaced by the values of
    *inputs* and *outputs* if they are specified. Note that in a concatenated
    context (eg. ``$out.d``) the number input or output files (respectively)
    must be exactly one, otherwise an error is raised.

    If *foreach* is specified, the generated command file accepts two
    command-line arguments for the input and output file. Note that references
    to ``$in`` and ``$out`` will then be replaced by the respective placeholder
    in the shells scripting language and the *inputs* and *outputs* parmaeters
    are ignored.

    If *accept_additional_args* is True, the last command in *commands* must
    accept forward arguments passed to the shell script.

    Returns 1) a list of strings that represents the command to execute the
    script. If *foreach* is specified, the two last items of the returned list
    will be ``['$in', '$out']``. 2) The actual filename that has been created.
    """

  @abc.abstractmethod
  def format_env_ref(self, envvar):
    """
    Given the name of an environment variable, return a new string that
    references that environment variable in the syntax of this platform's
    shell.
    """

  @staticmethod
  def replace_argument_inout_vars(arg, inputs, outputs):
    """
    Helper function for :meth:`write_command_file` to replace the ``$in``
    and ``$out`` variables in a command argument *arg* with the specified
    *inputs* and *outputs*.
    """

    def replace_var(var, value, files):
      files = files or ()
      match = re.match('.*(\\$' + var + ')\\b.*', value)
      if not match:
        return [value]
      if match.group(0) == '$' + var:
        return files
      #if len(files) != 1:
      #  raise RuntimeError('embedded in an argument, `$' + var +
      #    '` can only expand with one filename')
      return [value[:match.start(1)] + files[0] + value[match.end(1):]]

    result = replace_var('in', arg, inputs)
    if len(result) == 1:
      result = replace_var('out', result[0], outputs)
    return result

  @staticmethod
  def replace_commands_inout_vars(commands, inputs, outputs):
    """
    Applies :meth:`replace_argument_inout_vars` to all *commands*.
    """

    new_commands = []
    for command in commands:
      new_commands.append(pyutils.flatten(
        [PlatformHelper.replace_argument_inout_vars(x, inputs, outputs)
        for x in command]))
    return new_commands
    commands = new_commands


class WindowsPlatformHelper(PlatformHelper):

  def prepare_commands(self, commands):
    # ISSUE craftr-build/craftr#67
    # On Windows, commands that are not executables need to be invoked via CMD.
    new_commands = []
    for args in commands:
      try:
        prog = shell.find_program(args[0])
        is_executable = prog.endswith('.exe')
      except FileNotFoundError:
        is_executable = args[0].endswith('.exe')
      if not is_executable:
        args = ['cmd', '/c'] + args
      new_commands.append(args)
    return new_commands

  def prepare_single_command(self, command, cwd):
    if cwd is not None:
      command = ['cmd', '/c', 'cd', cwd, shell.safe('&&')] + command
    return command

  def write_command_file(self, filename, commands, inputs=None, outputs=None,
      cwd=None, environ=None, foreach=False, suffix='.cmd', dry=False,
      accept_additional_args=False):

    if suffix is not None:
      filename = path.addsuffix(filename, suffix)
    result = ['cmd', '/Q', '/c', filename]
    if foreach:
      result += ['$in', '$out']
      inputs, outputs = ['%1'], ['%2']

    commands = self.replace_commands_inout_vars(commands, inputs, outputs)
    if dry:
      return result, filename

    path.makedirs(path.dirname(path.abs(filename)))
    with open(filename, 'w') as fp:
      fp.write('REM This file is automatically generated with Craftr. It is \n')
      fp.write('REM not recommended to modify it manually.\n\n')
      if cwd is not None:
        fp.write('cd ' + shell.quote(cwd) + '\n\n')
      for key, value in environ.items():
        fp.write('set ' + shell.quote('{}={}'.format(key, value), for_ninja=True) + '\n')
      fp.write('\n')
      for index, command in enumerate(commands):
        if accept_additional_args and index == len(commands)-1:
          command.append(shell.safe('%*'))
        fp.write(shell.join(command) + '\n')
        fp.write('if %errorlevel% neq 0 exit %errorlevel%\n\n')

    return result, filename

  def format_env_ref(self, envvar):
    return '%' + envvar + '%'


class UnixPlatformHelper(PlatformHelper):

  def prepare_commands(self, commands):
    return commands

  def prepare_single_command(self, command, cwd):
    if cwd is not None:
      command = [shell.safe('('), 'cd', cwd, shell.safe('&&')] + command + [shell.safe(')')]
    return command

  def write_command_file(self, filename, commands, inputs=None, outputs=None,
      cwd=None, environ=None, foreach=False, suffix='.sh', dry=False,
      accept_additional_args=False):

    if suffix is not None:
      filename = path.addsuffix(filename, suffix)
    result = [filename]
    if foreach:
      result += ['$in', '$out']
      inputs, outputs = ['%1'], ['%2']

    commands = self.replace_commands_inout_vars(commands, inputs, outputs)
    if dry:
      return result, filename

    path.makedirs(path.dirname(filename))
    with open(filename, 'w') as fp:
      # TODO: Make sure this also works for shells other than bash.
      fp.write('#!' + shell.find_program(environ.get('SHELL', 'bash')) + '\n')
      fp.write('set -e\n')
      if cwd:
        fp.write('cd ' + shell.quote(cwd) + '\n')
      fp.write('\n')
      for key, value in environ.items():
        fp.write('export {}={}\n'.format(key, shell.quote(value)))
      fp.write('\n')
      for index, command in enumerate(commands):
        if accept_additional_args and index == len(commands)-1:
          command.append(shell.safe('$*'))
        fp.write(shell.join(command))
        fp.write('\n')

    os.chmod(filename, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR |
      stat.S_IRGRP | stat.S_IWGRP | stat.S_IROTH)  # rwxrw-r--

    return result, filename

  def format_env_ref(self, envvar):
    # We need to use double quotes since otherwise the variable would be
    # expanded by Ninja instead of bash.
    return '$$' + envvar


def get_platform_helper():
  if platform.name == 'win':
    return WindowsPlatformHelper()
  elif platform.name in ('cygwin', 'msys', 'linux', 'mac'):
    return UnixPlatformHelper()
  raise EnvironmentError('unsupported platform: {}'.format(platform.name))
