"""byte-sqlite - compiler expression models module."""
from __future__ import absolute_import, division, print_function

from byte.compilers.sqlite.models.clause import SqliteClause
from byte.compilers.sqlite.models.entity import SqliteEntity
from byte.compilers.sqlite.models.set import SqliteSet
from byte.core.models import BaseProperty, Expressions, Node
from byte.core.models.expressions.base import (
    And,
    Between,
    Equal,
    Expression,
    GreaterThan,
    GreaterThanOrEqual,
    In,
    Is,
    IsNot,
    LessThan,
    LessThanOrEqual,
    Like,
    NotEqual,
    NotIn,
    Or,
    RegularExpression
)
from byte.core.models.expressions.proxy import BaseProxyExpression

import inspect


# TODO Implement sqlite expressions
# __add__ = _e(OP.ADD)
# __sub__ = _e(OP.SUB)
# __mul__ = _e(OP.MUL)
# __div__ = __truediv__ = _e(OP.DIV)
# __xor__ = _e(OP.XOR)
# __radd__ = _e(OP.ADD, inv=True)
# __rsub__ = _e(OP.SUB, inv=True)
# __rmul__ = _e(OP.MUL, inv=True)
# __rdiv__ = __rtruediv__ = _e(OP.DIV, inv=True)
# __rand__ = _e(OP.AND, inv=True)
# __ror__ = _e(OP.OR, inv=True)
# __rxor__ = _e(OP.XOR, inv=True)
# __lshift__ = _e(OP.IN)
# __rshift__ = _e(OP.IS)
# __mod__ = _e(OP.LIKE)
# __pow__ = _e(OP.ILIKE)
# bin_and = _e(OP.BIN_AND)
# bin_or = _e(OP.BIN_OR)
# __invert__
class SqliteExpressions(Expressions):
    """SQLite expressions class."""

    @property
    def compiler(self):
        """Retrieve compiler.

        :rtype: byte.compilers.core.base.Compiler
        """
        raise NotImplementedError

    @classmethod
    def match(cls, source):
        """Find an expression matching the provided `source` expression.

        :param source: Source Expression
        :type source: byte.core.models.expressions.base.Expression

        :return: SQLite Expression Class
        """
        if hasattr(source, '__class__'):
            source = source.__class__

        # Find base class
        source_base = None

        for base in inspect.getmro(source):
            if base.__module__.startswith('byte.core.models.expressions.base'):
                source_base = base
                break

        if source_base is None:
            return None, None

        # Find matching expression
        for expression_cls in EXPRESSIONS:
            if issubclass(expression_cls, source_base):
                return source_base, expression_cls

        return source_base, None

    @classmethod
    def parse(cls, compiler, source):
        """Parse `source` expression into SQLite expression.

        :param compiler: Compiler
        :type compiler: byte.compilers.core.base.Compiler

        :param source: Source Expression
        :type source: byte.core.models.expressions.base.Expression

        :return: SQLite Expression
        :rtype: SqliteExpression
        """
        if not isinstance(source, BaseProxyExpression):
            return source

        # Find matching sqlite expression
        base_cls, expression_cls = cls.match(source)

        if not expression_cls:
            if base_cls:
                raise NotImplementedError('Unsupported expression: %s' % (base_cls.__name__,))

            raise NotImplementedError('Unsupported expression: %s' % (source.__class__.__name__,))

        # Transform `source` expression into `target_cls`
        if issubclass(expression_cls, SqliteManyExpression):
            return expression_cls(compiler, *[
                cls.parse(compiler, value)
                for value in source.values
            ])

        if issubclass(expression_cls, SqliteExpression):
            return expression_cls(compiler, source.lhs, source.rhs)

        raise NotImplementedError('Unsupported expression: %s' % (base_cls.__name__,))

    def and_(self, *values):
        """Create SQLite AND expression."""
        return SqliteAnd(self.compiler, self, *values)

    def between(self, low, high):
        """Create SQLite BETWEEN expression."""
        return SqliteBetween(self.compiler, self, SqliteSet(low, SqliteClause('AND'), high))

    def concat(self, rhs):
        """Create SQLite CONCAT expression."""
        return SqliteStringExpression(self.compiler, self, rhs)

    def contains(self, rhs):
        """Create SQLite LIKE contains expression."""
        return SqliteLike(self.compiler, self, '%%%s%%' % rhs)

    def endswith(self, rhs):
        """Create SQLite LIKE ends-with expression."""
        return SqliteLike(self.compiler, self, '%%%s' % rhs)

    def in_(self, rhs):
        """Create SQLite IN expression."""
        return SqliteIn(self.compiler, self, rhs)

    def is_null(self, is_null=True):
        """Create SQLite IS NULL expression."""
        if is_null:
            return SqliteIs(self.compiler, self, None)

        return SqliteIsNot(self.compiler, self, None)

    def not_in(self, rhs):
        """Create SQLite NOT IN expression."""
        return SqliteNotIn(self.compiler, self, rhs)

    def or_(self, *values):
        """Create SQLite OR expression."""
        return SqliteOr(self.compiler, self, *values)

    def regexp(self, expression):
        """Create SQLite REGEXP expression."""
        return SqliteRegularExpression(self.compiler, self, expression)

    def startswith(self, rhs):
        """Create SQLite LIKE starts-with expression."""
        return SqliteLike(self.compiler, self, '%s%%' % rhs)

    def __and__(self, rhs):
        return And(self.compiler, self, rhs)

    def __eq__(self, rhs):
        if rhs is None:
            return SqliteIs(self.compiler, self, rhs)

        return SqliteEqual(self.compiler, self, rhs)

    def __ge__(self, rhs):
        return SqliteGreaterThanOrEqual(self.compiler, self, rhs)

    def __gt__(self, rhs):
        return SqliteGreaterThan(self.compiler, self, rhs)

    def __le__(self, rhs):
        return SqliteLessThanOrEqual(self.compiler, self, rhs)

    def __lt__(self, rhs):
        return SqliteLessThan(self.compiler, self, rhs)

    def __ne__(self, rhs):
        if rhs is None:
            return SqliteIsNot(self.compiler, self, rhs)

        return SqliteNotEqual(self.compiler, self, rhs)

    def __neg__(self):
        return self.desc()

    def __or__(self, rhs):
        return SqliteOr(self.compiler, self, rhs)

    def __pos__(self):
        return self.asc()


class SqliteExpression(Expression, SqliteExpressions):
    """SQLite expression class."""

    operator = None

    def compile(self):
        """Compile SQLite expression.

        :rtype: SqliteClause
        """
        if not self.operator:
            raise NotImplementedError('%s.operator hasn\'t been defined' % (self.__class__.__name__,))

        parameters = []

        # Parse values
        lhs = self._compile_value(parameters, self.lhs)
        rhs = self._compile_value(parameters, self.rhs)

        # Compile clause
        return SqliteClause('%s %s %s' % (lhs, self.operator, rhs), *parameters).compile()

    def _compile_value(self, parameters, value):
        if isinstance(value, BaseProperty):
            statement, _ = SqliteEntity(self.compiler.table, value.name).compile()
            return statement

        parameters.append(value)
        return '?'


class SqliteManyExpression(Node, SqliteExpressions):
    """SQLite many expression class."""

    operator = None

    def __init__(self, *values):
        """Create SQLite many expression."""
        self.values = values

    def compile(self):
        """Compile SQLite many expression.

        :rtype: SqliteSet
        """
        if not self.operator:
            raise NotImplementedError('%s.operator hasn\'t been defined' % (self.__class__.__name__,))

        return SqliteSet(*self.values, delimiter=' %s ' % (self.operator,)).compile()


class SqliteStringExpression(SqliteExpression):
    """SQLite string expression class."""

    def __add__(self, other):
        return self.concat(other)

    def __radd__(self, other):
        return other.concat(self)


class SqliteAnd(And, SqliteManyExpression):
    """SQLite AND expression class."""

    operator = 'AND'


class SqliteBetween(Between, SqliteExpression):
    """SQLite BETWEEN expression class."""

    operator = 'BETWEEN'


class SqliteEqual(Equal, SqliteExpression):
    """SQLite Equal expression class."""

    operator = '=='


class SqliteGreaterThan(GreaterThan, SqliteExpression):
    """SQLite Greater-than expression class."""

    operator = '>'


class SqliteGreaterThanOrEqual(GreaterThanOrEqual, SqliteExpression):
    """SQLite Greater-than-or-equal expression class."""

    operator = '>='


class SqliteIn(In, SqliteExpression):
    """SQLite IN expression class."""

    operator = 'IN'


class SqliteIs(Is, SqliteExpression):
    """SQLite IS expression class."""

    operator = 'IS'


class SqliteIsNot(IsNot, SqliteExpression):
    """SQLite IS NOT expression class."""

    operator = 'IS NOT'


class SqliteLessThan(LessThan, SqliteExpression):
    """SQLite Less-than expression class."""

    operator = '<'


class SqliteLessThanOrEqual(LessThanOrEqual, SqliteExpression):
    """SQLite Less-than-or-equal expression class."""

    operator = '<='


class SqliteLike(Like, SqliteExpression):
    """SQLite LIKE expression class."""

    operator = 'LIKE'


class SqliteNotEqual(NotEqual, SqliteExpression):
    """SQLite Not-equal expression class."""

    operator = '!='


class SqliteNotIn(NotIn, SqliteExpression):
    """SQLite NOT IN expression class."""

    operator = 'NOT IN'


class SqliteOr(Or, SqliteManyExpression):
    """SQLite OR expression class."""

    operator = 'OR'


class SqliteRegularExpression(RegularExpression, SqliteExpression):
    """SQLite REGEXP expression class."""

    operator = 'REGEXP'


EXPRESSIONS = [
    SqliteAnd,
    SqliteBetween,
    SqliteEqual,
    SqliteGreaterThan,
    SqliteGreaterThanOrEqual,
    SqliteIn,
    SqliteIs,
    SqliteIsNot,
    SqliteLessThan,
    SqliteLessThanOrEqual,
    SqliteLike,
    SqliteNotEqual,
    SqliteNotIn,
    SqliteOr,
    SqliteRegularExpression
]
