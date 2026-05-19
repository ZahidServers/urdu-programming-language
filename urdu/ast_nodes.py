"""AST node definitions for the Urdu Programming Language."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Optional


# ─── Base (not a dataclass — avoids default-arg ordering issues) ──────────────

class ASTNode:
    line: int = 0

    def accept(self, visitor):
        method = getattr(visitor, f"visit_{type(self).__name__}", None)
        if method:
            return method(self)
        raise NotImplementedError(f"No visitor for {type(self).__name__}")


# helper: each node stores line at end with default 0
def _node(*fields, line=0):
    pass


# ─── Program ─────────────────────────────────────────────────────────────────

@dataclass
class Program(ASTNode):
    body: list
    line: int = 0


# ─── Literals ────────────────────────────────────────────────────────────────

@dataclass
class NumberLiteral(ASTNode):
    value: Any
    line: int = 0

@dataclass
class StringLiteral(ASTNode):
    value: str
    line: int = 0

@dataclass
class TemplateLiteral(ASTNode):
    parts: list
    line: int = 0

@dataclass
class BooleanLiteral(ASTNode):
    value: bool
    line: int = 0

@dataclass
class NullLiteral(ASTNode):
    line: int = 0

@dataclass
class UndefinedLiteral(ASTNode):
    line: int = 0

@dataclass
class ArrayLiteral(ASTNode):
    elements: list
    line: int = 0

@dataclass
class ObjectProperty(ASTNode):
    key: Any
    value: Any
    computed: bool = False
    shorthand: bool = False
    method: bool = False
    line: int = 0

@dataclass
class ObjectLiteral(ASTNode):
    properties: list
    line: int = 0

@dataclass
class RegexLiteral(ASTNode):
    pattern: str
    flags: str
    line: int = 0


# ─── Identifiers ─────────────────────────────────────────────────────────────

@dataclass
class Identifier(ASTNode):
    name: str
    line: int = 0

@dataclass
class ThisExpression(ASTNode):
    line: int = 0

@dataclass
class SuperExpression(ASTNode):
    line: int = 0


# ─── Expressions ─────────────────────────────────────────────────────────────

@dataclass
class BinaryExpr(ASTNode):
    op: str
    left: Any
    right: Any
    line: int = 0

@dataclass
class LogicalExpr(ASTNode):
    op: str
    left: Any
    right: Any
    line: int = 0

@dataclass
class UnaryExpr(ASTNode):
    op: str
    operand: Any
    prefix: bool = True
    line: int = 0

@dataclass
class UpdateExpr(ASTNode):
    op: str
    operand: Any
    prefix: bool = True
    line: int = 0

@dataclass
class AssignExpr(ASTNode):
    op: str
    left: Any
    right: Any
    line: int = 0

@dataclass
class TernaryExpr(ASTNode):
    condition: Any
    consequent: Any
    alternate: Any
    line: int = 0

@dataclass
class NullishExpr(ASTNode):
    left: Any
    right: Any
    line: int = 0

@dataclass
class MemberExpr(ASTNode):
    obj: Any
    prop: Any
    computed: bool = False
    optional: bool = False
    line: int = 0

@dataclass
class CallExpr(ASTNode):
    callee: Any
    args: list
    optional: bool = False
    line: int = 0

@dataclass
class NewExpr(ASTNode):
    callee: Any
    args: list
    line: int = 0

@dataclass
class ArrowFunction(ASTNode):
    params: list
    body: Any
    is_async: bool = False
    is_expression: bool = False
    line: int = 0

@dataclass
class FunctionExpr(ASTNode):
    name: Optional[str]
    params: list
    body: Any
    is_async: bool = False
    is_generator: bool = False
    line: int = 0

@dataclass
class SpreadElement(ASTNode):
    argument: Any
    line: int = 0

@dataclass
class SequenceExpr(ASTNode):
    expressions: list
    line: int = 0

@dataclass
class AwaitExpr(ASTNode):
    argument: Any
    line: int = 0

@dataclass
class YieldExpr(ASTNode):
    argument: Any
    delegate: bool = False
    line: int = 0

@dataclass
class TypeofExpr(ASTNode):
    argument: Any
    line: int = 0

@dataclass
class DeleteExpr(ASTNode):
    argument: Any
    line: int = 0

@dataclass
class VoidExpr(ASTNode):
    argument: Any
    line: int = 0

@dataclass
class InstanceofExpr(ASTNode):
    left: Any
    right: Any
    line: int = 0

@dataclass
class InExpr(ASTNode):
    key: Any
    obj: Any
    line: int = 0

@dataclass
class TaggedTemplateExpr(ASTNode):
    tag: Any
    template: Any
    line: int = 0


# ─── Destructuring ───────────────────────────────────────────────────────────

@dataclass
class ArrayPattern(ASTNode):
    elements: list
    line: int = 0

@dataclass
class ObjectPatternProp(ASTNode):
    key: str
    value: Any
    shorthand: bool = True
    default: Any = None
    line: int = 0

@dataclass
class ObjectPattern(ASTNode):
    properties: list
    line: int = 0

@dataclass
class RestElement(ASTNode):
    argument: Any
    line: int = 0

@dataclass
class AssignPattern(ASTNode):
    left: Any
    right: Any
    line: int = 0


# ─── Parameters ──────────────────────────────────────────────────────────────

@dataclass
class Param(ASTNode):
    name: Any
    default: Any = None
    rest: bool = False
    line: int = 0


# ─── Statements ──────────────────────────────────────────────────────────────

@dataclass
class Block(ASTNode):
    body: list
    line: int = 0

@dataclass
class ExpressionStatement(ASTNode):
    expression: Any
    line: int = 0

@dataclass
class VarDeclarator(ASTNode):
    id: Any
    init: Any = None
    line: int = 0

@dataclass
class VarDeclaration(ASTNode):
    kind: str
    declarations: list
    line: int = 0

@dataclass
class FunctionDecl(ASTNode):
    name: str
    params: list
    body: Any
    is_async: bool = False
    is_generator: bool = False
    line: int = 0
    decorators: list = field(default_factory=list)

@dataclass
class ClassMember(ASTNode):
    key: Any
    value: Any
    kind: str = "method"
    is_static: bool = False
    access: str = "public"
    computed: bool = False
    is_async: bool = False
    line: int = 0

@dataclass
class ClassDecl(ASTNode):
    name: str
    superclass: Any
    body: list
    line: int = 0

@dataclass
class IfStatement(ASTNode):
    condition: Any
    consequent: Any
    alternate: Any = None
    line: int = 0

@dataclass
class WhileStatement(ASTNode):
    condition: Any
    body: Any
    line: int = 0

@dataclass
class DoWhileStatement(ASTNode):
    condition: Any
    body: Any
    line: int = 0

@dataclass
class ForStatement(ASTNode):
    init: Any
    condition: Any
    update: Any
    body: Any
    line: int = 0

@dataclass
class ForInStatement(ASTNode):
    kind: str
    left: Any
    right: Any
    body: Any
    line: int = 0

@dataclass
class SwitchCase(ASTNode):
    test: Any
    consequent: list
    line: int = 0

@dataclass
class SwitchStatement(ASTNode):
    discriminant: Any
    cases: list
    line: int = 0

@dataclass
class ReturnStatement(ASTNode):
    argument: Any = None
    line: int = 0

@dataclass
class BreakStatement(ASTNode):
    label: Any = None
    line: int = 0

@dataclass
class ContinueStatement(ASTNode):
    label: Any = None
    line: int = 0

@dataclass
class ThrowStatement(ASTNode):
    argument: Any
    line: int = 0

@dataclass
class CatchClause(ASTNode):
    param: Any
    body: Any
    line: int = 0

@dataclass
class TryStatement(ASTNode):
    block: Any
    handler: Any
    finalizer: Any
    line: int = 0

@dataclass
class ImportSpecifier(ASTNode):
    imported: str
    local: str
    kind: str = "named"
    line: int = 0

@dataclass
class ImportDeclaration(ASTNode):
    specifiers: list
    source: str
    line: int = 0

@dataclass
class ExportSpecifier(ASTNode):
    local: str
    exported: str
    line: int = 0

@dataclass
class ExportDeclaration(ASTNode):
    declaration: Any
    specifiers: list
    default: bool = False
    line: int = 0

@dataclass
class LabeledStatement(ASTNode):
    label: str
    body: Any
    line: int = 0

@dataclass
class EmptyStatement(ASTNode):
    line: int = 0

@dataclass
class DecoratorNode(ASTNode):
    expression: Any
    line: int = 0
