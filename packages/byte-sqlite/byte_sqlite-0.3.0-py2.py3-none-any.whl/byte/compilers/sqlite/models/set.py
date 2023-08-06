"""byte-sqlite - compiler set model module."""
from __future__ import absolute_import, division, print_function

from byte.core.models import Set


class SqliteSet(Set):
    """SQlite set class."""

    delimiter = ' '

    prefix = ''
    suffix = ''

    def __init__(self, *nodes, **kwargs):
        """Create SQLite node set.

        :param nodes: Nodes
        :type nodes: Node

        :param kwargs Options (overrides defaults)
        """
        delimiter = kwargs.pop('delimiter', None)

        prefix = kwargs.pop('prefix', None)
        suffix = kwargs.pop('suffix', None)

        super(SqliteSet, self).__init__(*nodes, **kwargs)

        if delimiter is not None:
            self.delimiter = delimiter

        if prefix is not None:
            self.prefix = prefix

        if suffix is not None:
            self.suffix = suffix

    def compile(self):
        """Compile SQLite set.

        :rtype: (str, tuple)
        """
        # Compile children
        statement, parameters = self.compile_children()

        # Build final statement
        return self.prefix + statement + self.suffix, parameters

    def compile_children(self):
        """Compile SQLite set children.

        :rtype: (str, tuple)
        """
        statements = []
        parameters = []

        for node in self.nodes:
            n_statement, n_parameters = node.compile()

            statements.append(n_statement)
            parameters.extend(n_parameters)

        return self.delimiter.join(statements), tuple(parameters)


class SqliteCommaSet(SqliteSet):
    """SQLite comma set class."""

    delimiter = ', '


class SqliteEnclosedSet(SqliteCommaSet):
    """SQLite enclosed set class."""

    prefix = '('
    suffix = ')'
