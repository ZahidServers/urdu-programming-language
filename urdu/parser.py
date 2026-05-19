"""Recursive-descent parser for the Urdu Programming Language."""

from __future__ import annotations
from .tokens import TokenType
from .lexer import Token
from .ast_nodes import *


class ParseError(Exception):
    def __init__(self, msg: str, line: int, col: int = 0):
        super().__init__(f"پارسر غلطی [{line}:{col}]: {msg}")
        self.line = line
        self.col = col


_ASSIGN_OPS = {
    TokenType.ASSIGN, TokenType.PLUS_ASSIGN, TokenType.MINUS_ASSIGN,
    TokenType.MULTIPLY_ASSIGN, TokenType.DIVIDE_ASSIGN, TokenType.MODULO_ASSIGN,
    TokenType.POWER_ASSIGN, TokenType.AND_ASSIGN, TokenType.OR_ASSIGN,
    TokenType.NULLISH_ASSIGN, TokenType.BITAND_ASSIGN, TokenType.BITOR_ASSIGN,
}


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = [t for t in tokens if t.type != TokenType.NEWLINE]
        self.pos = 0

    # ── helpers ──────────────────────────────────────────────────────────────

    def _peek(self, offset: int = 0) -> Token:
        idx = self.pos + offset
        if idx < len(self.tokens):
            return self.tokens[idx]
        return self.tokens[-1]  # EOF

    def _advance(self) -> Token:
        t = self.tokens[self.pos]
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
        return t

    def _check(self, *types: TokenType) -> bool:
        return self._peek().type in types

    def _match(self, *types: TokenType) -> Token | None:
        if self._peek().type in types:
            return self._advance()
        return None

    def _expect(self, type: TokenType, msg: str = "") -> Token:
        t = self._peek()
        if t.type != type:
            raise ParseError(
                msg or f"Expected {type.name}, got {t.type.name} ({t.value!r})",
                t.line, t.column
            )
        return self._advance()

    def _eat_semicolon(self):
        self._match(TokenType.SEMICOLON)

    def _line(self) -> int:
        return self._peek().line

    # ── entry point ──────────────────────────────────────────────────────────

    def parse(self) -> Program:
        body: list[ASTNode] = []
        while not self._check(TokenType.EOF):
            body.append(self._parse_statement())
        return Program(body=body, line=1)

    # ── statements ───────────────────────────────────────────────────────────

    def _parse_statement(self) -> ASTNode:
        t = self._peek()

        if t.type == TokenType.AT:
            return self._parse_decorated()
        if t.type in (TokenType.VAR, TokenType.CONST, TokenType.LET):
            return self._parse_var_decl()
        if t.type == TokenType.FUNCTION:
            return self._parse_func_decl(is_async=False)
        if t.type == TokenType.ASYNC and self._peek(1).type == TokenType.FUNCTION:
            self._advance()
            return self._parse_func_decl(is_async=True)
        if t.type == TokenType.CLASS:
            return self._parse_class_decl()
        if t.type == TokenType.IF:
            return self._parse_if()
        if t.type == TokenType.WHILE:
            return self._parse_while()
        if t.type == TokenType.DO:
            return self._parse_do_while()
        if t.type == TokenType.FOR:
            return self._parse_for()
        if t.type == TokenType.SWITCH:
            return self._parse_switch()
        if t.type == TokenType.RETURN:
            return self._parse_return()
        if t.type == TokenType.BREAK:
            self._advance()
            self._eat_semicolon()
            return BreakStatement(line=t.line)
        if t.type == TokenType.CONTINUE:
            self._advance()
            self._eat_semicolon()
            return ContinueStatement(line=t.line)
        if t.type == TokenType.THROW:
            return self._parse_throw()
        if t.type == TokenType.TRY:
            return self._parse_try()
        if t.type == TokenType.IMPORT:
            return self._parse_import()
        if t.type == TokenType.EXPORT:
            return self._parse_export()
        if t.type == TokenType.LEFT_BRACE:
            return self._parse_block()
        if t.type == TokenType.SEMICOLON:
            self._advance()
            return EmptyStatement(line=t.line)

        return self._parse_expression_statement()

    def _parse_decorated(self) -> ASTNode:
        line = self._line()
        decorators = []
        while self._check(TokenType.AT):
            self._advance()
            expr = self._parse_call_expr()
            decorators.append(DecoratorNode(expression=expr, line=line))
        stmt = self._parse_statement()
        if decorators:
            if not hasattr(stmt, "decorators"):
                object.__setattr__(stmt, "decorators", []) if hasattr(stmt, "__dataclass_fields__") else setattr(stmt, "decorators", [])
            stmt.decorators = decorators
        return stmt

    def _parse_block(self) -> Block:
        line = self._line()
        self._expect(TokenType.LEFT_BRACE)
        body: list[ASTNode] = []
        while not self._check(TokenType.RIGHT_BRACE, TokenType.EOF):
            body.append(self._parse_statement())
        self._expect(TokenType.RIGHT_BRACE)
        return Block(body=body, line=line)

    def _parse_block_or_stmt(self) -> Block:
        """Parse either a { block } or a single statement."""
        if self._check(TokenType.LEFT_BRACE):
            return self._parse_block()
        line = self._line()
        stmt = self._parse_statement()
        return Block(body=[stmt], line=line)

    def _parse_var_decl(self) -> VarDeclaration:
        line = self._line()
        kind_tok = self._advance()
        kind = {
            TokenType.VAR: "var",
            TokenType.CONST: "const",
            TokenType.LET: "let",
        }[kind_tok.type]

        decls: list[VarDeclarator] = []
        while True:
            decl_line = self._line()
            id_node = self._parse_binding_pattern()
            init = None
            if self._match(TokenType.ASSIGN):
                init = self._parse_assignment()
            decls.append(VarDeclarator(id=id_node, init=init, line=decl_line))
            if not self._match(TokenType.COMMA):
                break

        self._eat_semicolon()
        return VarDeclaration(kind=kind, declarations=decls, line=line)

    def _parse_binding_pattern(self) -> ASTNode:
        t = self._peek()
        if t.type == TokenType.LEFT_BRACKET:
            return self._parse_array_pattern()
        if t.type == TokenType.LEFT_BRACE:
            return self._parse_object_pattern()
        return Identifier(name=self._advance().value, line=t.line)

    def _parse_array_pattern(self) -> ArrayPattern:
        line = self._line()
        self._expect(TokenType.LEFT_BRACKET)
        elements = []
        while not self._check(TokenType.RIGHT_BRACKET, TokenType.EOF):
            if self._check(TokenType.COMMA):
                elements.append(None)
            elif self._check(TokenType.SPREAD):
                self._advance()
                elements.append(RestElement(argument=self._parse_binding_pattern(), line=self._line()))
            else:
                elem = self._parse_binding_pattern()
                if self._match(TokenType.ASSIGN):
                    elem = AssignPattern(left=elem, right=self._parse_assignment(), line=elem.line)
                elements.append(elem)
            if not self._match(TokenType.COMMA):
                break
        self._expect(TokenType.RIGHT_BRACKET)
        return ArrayPattern(elements=elements, line=line)

    def _parse_object_pattern(self) -> ObjectPattern:
        line = self._line()
        self._expect(TokenType.LEFT_BRACE)
        props = []
        while not self._check(TokenType.RIGHT_BRACE, TokenType.EOF):
            prop_line = self._line()
            if self._check(TokenType.SPREAD):
                self._advance()
                arg = self._parse_binding_pattern()
                props.append(RestElement(argument=arg, line=prop_line))
            else:
                key_tok = self._advance()
                key = key_tok.value
                if self._match(TokenType.COLON):
                    val = self._parse_binding_pattern()
                    default = None
                    if self._match(TokenType.ASSIGN):
                        default = self._parse_assignment()
                    props.append(ObjectPatternProp(key=key, value=val, shorthand=False, default=default, line=prop_line))
                else:
                    id_node = Identifier(name=key, line=prop_line)
                    default = None
                    if self._match(TokenType.ASSIGN):
                        default = self._parse_assignment()
                    props.append(ObjectPatternProp(key=key, value=id_node, shorthand=True, default=default, line=prop_line))
            if not self._match(TokenType.COMMA):
                break
        self._expect(TokenType.RIGHT_BRACE)
        return ObjectPattern(properties=props, line=line)

    def _parse_params(self) -> list[Param]:
        self._expect(TokenType.LEFT_PAREN)
        params: list[Param] = []
        while not self._check(TokenType.RIGHT_PAREN, TokenType.EOF):
            p_line = self._line()
            rest = bool(self._match(TokenType.SPREAD))
            id_node = self._parse_binding_pattern()
            default = None
            if self._match(TokenType.ASSIGN):
                default = self._parse_assignment()
            params.append(Param(name=id_node, default=default, rest=rest, line=p_line))
            if rest:
                break
            if not self._match(TokenType.COMMA):
                break
        self._expect(TokenType.RIGHT_PAREN)
        return params

    def _parse_func_decl(self, is_async: bool = False) -> FunctionDecl:
        line = self._line()
        self._expect(TokenType.FUNCTION)
        is_generator = bool(self._match(TokenType.MULTIPLY))
        name_tok = self._advance()
        params = self._parse_params()
        body = self._parse_block()
        return FunctionDecl(
            name=name_tok.value, params=params, body=body,
            is_async=is_async, is_generator=is_generator, line=line
        )

    def _parse_class_decl(self) -> ClassDecl:
        line = self._line()
        self._expect(TokenType.CLASS)
        name_tok = self._advance()
        superclass = None
        if self._match(TokenType.EXTENDS):
            superclass = self._parse_left_hand_side()
        self._expect(TokenType.LEFT_BRACE)
        members = []
        while not self._check(TokenType.RIGHT_BRACE, TokenType.EOF):
            members.append(self._parse_class_member())
        self._expect(TokenType.RIGHT_BRACE)
        return ClassDecl(name=name_tok.value, superclass=superclass, body=members, line=line)

    def _parse_class_member(self) -> ClassMember:
        line = self._line()
        access = "public"
        is_static = False
        is_async = False

        if self._match(TokenType.PUBLIC): access = "public"
        elif self._match(TokenType.PRIVATE): access = "private"
        elif self._match(TokenType.PROTECTED): access = "protected"

        if self._match(TokenType.STATIC): is_static = True
        if self._check(TokenType.ASYNC) and self._peek(1).type == TokenType.IDENTIFIER:
            self._advance()
            is_async = True

        # getter / setter
        kind = "method"
        if self._check(TokenType.GET) and self._peek(1).type not in (TokenType.LEFT_PAREN, TokenType.SEMICOLON):
            self._advance(); kind = "get"
        elif self._check(TokenType.SET) and self._peek(1).type not in (TokenType.LEFT_PAREN, TokenType.SEMICOLON):
            self._advance(); kind = "set"

        # constructor
        if self._check(TokenType.CONSTRUCTOR):
            self._advance()
            params = self._parse_params()
            body = self._parse_block()
            return ClassMember(key="__init__", value=FunctionDecl(name="__init__", params=params, body=body, line=line),
                               kind="constructor", is_static=is_static, access=access, is_async=False, line=line)

        # computed key [expr]
        computed = False
        if self._check(TokenType.LEFT_BRACKET):
            self._advance()
            key = self._parse_assignment()
            self._expect(TokenType.RIGHT_BRACKET)
            computed = True
        else:
            key_tok = self._advance()
            key = key_tok.value

        # field or method
        if self._check(TokenType.LEFT_PAREN):
            params = self._parse_params()
            body = self._parse_block()
            val = FunctionDecl(name=str(key) if not computed else "_computed_",
                               params=params, body=body, is_async=is_async, line=line)
            return ClassMember(key=key, value=val, kind=kind, is_static=is_static,
                               access=access, computed=computed, is_async=is_async, line=line)
        else:
            init = None
            if self._match(TokenType.ASSIGN):
                init = self._parse_assignment()
            self._eat_semicolon()
            return ClassMember(key=key, value=init, kind="field", is_static=is_static,
                               access=access, computed=computed, line=line)

    def _parse_if(self) -> IfStatement:
        line = self._line()
        self._expect(TokenType.IF)
        self._expect(TokenType.LEFT_PAREN)
        cond = self._parse_expression()
        self._expect(TokenType.RIGHT_PAREN)
        then = self._parse_block_or_stmt()
        alt = None
        if self._match(TokenType.ELIF):
            self._tokens_prepend_if()
            alt = self._parse_if()
        elif self._check(TokenType.ELSE) and self._peek(1).type == TokenType.IF:
            self._advance()
            alt = self._parse_if()
        elif self._match(TokenType.ELSE):
            alt = self._parse_block_or_stmt()
        return IfStatement(condition=cond, consequent=then, alternate=alt, line=line)

    def _tokens_prepend_if(self):
        """ورنہ_اگر already consumed — synthesize IF token at current pos."""
        from .lexer import Token as Tok
        fake = Tok(TokenType.IF, "اگر", self._peek().line, self._peek().column)
        self.tokens.insert(self.pos, fake)

    def _parse_while(self) -> WhileStatement:
        line = self._line()
        self._expect(TokenType.WHILE)
        self._expect(TokenType.LEFT_PAREN)
        cond = self._parse_expression()
        self._expect(TokenType.RIGHT_PAREN)
        body = self._parse_block()
        return WhileStatement(condition=cond, body=body, line=line)

    def _parse_do_while(self) -> DoWhileStatement:
        line = self._line()
        self._expect(TokenType.DO)
        body = self._parse_block()
        self._expect(TokenType.WHILE)
        self._expect(TokenType.LEFT_PAREN)
        cond = self._parse_expression()
        self._expect(TokenType.RIGHT_PAREN)
        self._eat_semicolon()
        return DoWhileStatement(condition=cond, body=body, line=line)

    def _parse_for(self) -> ASTNode:
        line = self._line()
        self._expect(TokenType.FOR)
        self._expect(TokenType.LEFT_PAREN)

        # for...of / for...in
        if self._check(TokenType.VAR, TokenType.CONST, TokenType.LET):
            save_pos = self.pos
            kind_tok = self._advance()
            kind = {TokenType.VAR: "var", TokenType.CONST: "const", TokenType.LET: "let"}[kind_tok.type]
            left_id = self._parse_binding_pattern()
            if self._match(TokenType.IN):
                right = self._parse_expression()
                self._expect(TokenType.RIGHT_PAREN)
                body = self._parse_block()
                return ForInStatement(kind="in", left=VarDeclaration(kind=kind, declarations=[VarDeclarator(id=left_id, init=None, line=line)], line=line), right=right, body=body, line=line)
            if self._match(TokenType.OF):
                right = self._parse_expression()
                self._expect(TokenType.RIGHT_PAREN)
                body = self._parse_block()
                return ForInStatement(kind="of", left=VarDeclaration(kind=kind, declarations=[VarDeclarator(id=left_id, init=None, line=line)], line=line), right=right, body=body, line=line)
            # rewind and parse as C-style for
            self.pos = save_pos

        if self._check(TokenType.IDENTIFIER):
            save_pos = self.pos
            left_id = Identifier(name=self._advance().value, line=self._line())
            if self._match(TokenType.IN):
                right = self._parse_expression()
                self._expect(TokenType.RIGHT_PAREN)
                return ForInStatement(kind="in", left=left_id, right=right, body=self._parse_block(), line=line)
            if self._match(TokenType.OF):
                right = self._parse_expression()
                self._expect(TokenType.RIGHT_PAREN)
                return ForInStatement(kind="of", left=left_id, right=right, body=self._parse_block(), line=line)
            self.pos = save_pos

        # C-style for (init; cond; update)
        init = None
        if not self._check(TokenType.SEMICOLON):
            if self._check(TokenType.VAR, TokenType.CONST, TokenType.LET):
                # _parse_var_decl consumes the semicolon via _eat_semicolon
                init = self._parse_var_decl()
                # If no semicolon was consumed (optional), consume it now
                # (already consumed by _eat_semicolon inside _parse_var_decl)
            else:
                init = ExpressionStatement(expression=self._parse_expression(), line=self._line())
                self._expect(TokenType.SEMICOLON)
        else:
            self._advance()  # eat leading semicolon

        cond = None if self._check(TokenType.SEMICOLON) else self._parse_expression()
        self._expect(TokenType.SEMICOLON)
        update = None if self._check(TokenType.RIGHT_PAREN) else self._parse_expression()
        self._expect(TokenType.RIGHT_PAREN)
        body = self._parse_block()
        return ForStatement(init=init, condition=cond, update=update, body=body, line=line)

    def _parse_switch(self) -> SwitchStatement:
        line = self._line()
        self._expect(TokenType.SWITCH)
        self._expect(TokenType.LEFT_PAREN)
        disc = self._parse_expression()
        self._expect(TokenType.RIGHT_PAREN)
        self._expect(TokenType.LEFT_BRACE)
        cases = []
        while not self._check(TokenType.RIGHT_BRACE, TokenType.EOF):
            case_line = self._line()
            if self._match(TokenType.CASE):
                test = self._parse_expression()
                self._expect(TokenType.COLON)
            elif self._match(TokenType.SWITCH_DEFAULT):
                test = None
                self._expect(TokenType.COLON)
            elif self._match(TokenType.DEFAULT):
                test = None
                self._match(TokenType.COLON)
            else:
                break
            consequent = []
            while not self._check(TokenType.CASE, TokenType.SWITCH_DEFAULT, TokenType.DEFAULT,
                                   TokenType.RIGHT_BRACE, TokenType.EOF):
                consequent.append(self._parse_statement())
            cases.append(SwitchCase(test=test, consequent=consequent, line=case_line))
        self._expect(TokenType.RIGHT_BRACE)
        return SwitchStatement(discriminant=disc, cases=cases, line=line)

    def _parse_return(self) -> ReturnStatement:
        line = self._line()
        self._expect(TokenType.RETURN)
        if self._check(TokenType.SEMICOLON, TokenType.RIGHT_BRACE, TokenType.EOF):
            self._eat_semicolon()
            return ReturnStatement(argument=None, line=line)
        arg = self._parse_expression()
        self._eat_semicolon()
        return ReturnStatement(argument=arg, line=line)

    def _parse_throw(self) -> ThrowStatement:
        line = self._line()
        self._expect(TokenType.THROW)
        arg = self._parse_expression()
        self._eat_semicolon()
        return ThrowStatement(argument=arg, line=line)

    def _parse_try(self) -> TryStatement:
        line = self._line()
        self._expect(TokenType.TRY)
        block = self._parse_block()
        handler = None
        finalizer = None
        if self._match(TokenType.CATCH):
            param = None
            if self._match(TokenType.LEFT_PAREN):
                param = Identifier(name=self._advance().value, line=self._line())
                self._expect(TokenType.RIGHT_PAREN)
            body = self._parse_block()
            handler = CatchClause(param=param, body=body, line=line)
        if self._match(TokenType.FINALLY):
            finalizer = self._parse_block()
        return TryStatement(block=block, handler=handler, finalizer=finalizer, line=line)

    def _parse_import(self) -> ImportDeclaration:
        line = self._line()
        self._expect(TokenType.IMPORT)
        specifiers = []

        if self._check(TokenType.MULTIPLY):
            # import * as name from "..."
            self._advance()
            self._expect(TokenType.AS)
            local = self._advance().value
            specifiers.append(ImportSpecifier(imported="*", local=local, kind="namespace", line=line))
        elif self._check(TokenType.LEFT_BRACE):
            # import { A, B as C } from "..."
            self._advance()
            while not self._check(TokenType.RIGHT_BRACE, TokenType.EOF):
                imp = self._advance().value
                local = imp
                if self._match(TokenType.AS):
                    local = self._advance().value
                specifiers.append(ImportSpecifier(imported=imp, local=local, kind="named", line=line))
                if not self._match(TokenType.COMMA):
                    break
            self._expect(TokenType.RIGHT_BRACE)
        elif self._check(TokenType.IDENTIFIER):
            # import name from "..."
            name = self._advance().value
            specifiers.append(ImportSpecifier(imported="default", local=name, kind="default", line=line))
            if self._match(TokenType.COMMA):
                self._expect(TokenType.LEFT_BRACE)
                while not self._check(TokenType.RIGHT_BRACE, TokenType.EOF):
                    imp = self._advance().value
                    local = imp
                    if self._match(TokenType.AS): local = self._advance().value
                    specifiers.append(ImportSpecifier(imported=imp, local=local, kind="named", line=line))
                    if not self._match(TokenType.COMMA): break
                self._expect(TokenType.RIGHT_BRACE)
        elif self._check(TokenType.STRING):
            src = self._advance().value
            self._eat_semicolon()
            return ImportDeclaration(specifiers=[], source=src, line=line)

        self._expect(TokenType.FROM)
        source = self._expect(TokenType.STRING).value
        self._eat_semicolon()
        return ImportDeclaration(specifiers=specifiers, source=source, line=line)

    def _parse_export(self) -> ExportDeclaration:
        line = self._line()
        self._expect(TokenType.EXPORT)
        is_default = bool(self._match(TokenType.DEFAULT))

        if self._check(TokenType.FUNCTION):
            decl = self._parse_func_decl()
            return ExportDeclaration(declaration=decl, specifiers=[], default=is_default, line=line)
        if self._check(TokenType.CLASS):
            decl = self._parse_class_decl()
            return ExportDeclaration(declaration=decl, specifiers=[], default=is_default, line=line)
        if self._check(TokenType.VAR, TokenType.CONST, TokenType.LET):
            decl = self._parse_var_decl()
            return ExportDeclaration(declaration=decl, specifiers=[], default=is_default, line=line)
        if self._check(TokenType.LEFT_BRACE):
            self._advance()
            specs = []
            while not self._check(TokenType.RIGHT_BRACE, TokenType.EOF):
                local = self._advance().value
                exported = local
                if self._match(TokenType.AS): exported = self._advance().value
                specs.append(ExportSpecifier(local=local, exported=exported, line=line))
                if not self._match(TokenType.COMMA): break
            self._expect(TokenType.RIGHT_BRACE)
            self._eat_semicolon()
            return ExportDeclaration(declaration=None, specifiers=specs, default=False, line=line)

        expr = self._parse_assignment()
        self._eat_semicolon()
        return ExportDeclaration(declaration=ExpressionStatement(expression=expr, line=line),
                                  specifiers=[], default=True, line=line)

    def _parse_expression_statement(self) -> ExpressionStatement:
        line = self._line()
        expr = self._parse_expression()
        self._eat_semicolon()
        return ExpressionStatement(expression=expr, line=line)

    # ── expressions (precedence climbing) ────────────────────────────────────

    def _parse_expression(self) -> ASTNode:
        exprs = [self._parse_assignment()]
        while self._match(TokenType.COMMA):
            exprs.append(self._parse_assignment())
        if len(exprs) == 1:
            return exprs[0]
        return SequenceExpr(expressions=exprs, line=exprs[0].line)

    def _parse_assignment(self) -> ASTNode:
        line = self._line()
        left = self._parse_ternary()

        if self._check(*_ASSIGN_OPS):
            op_tok = self._advance()
            right = self._parse_assignment()
            return AssignExpr(op=op_tok.value, left=left, right=right, line=line)

        return left

    def _parse_ternary(self) -> ASTNode:
        cond = self._parse_nullish()
        if self._match(TokenType.QUESTION):
            then = self._parse_assignment()
            self._expect(TokenType.COLON)
            alt = self._parse_assignment()
            return TernaryExpr(condition=cond, consequent=then, alternate=alt, line=cond.line)
        return cond

    def _parse_nullish(self) -> ASTNode:
        left = self._parse_logical_or()
        while self._match(TokenType.NULLISH):
            right = self._parse_logical_or()
            left = NullishExpr(left=left, right=right, line=left.line)
        return left

    def _parse_logical_or(self) -> ASTNode:
        left = self._parse_logical_and()
        while self._check(TokenType.LOGICAL_OR, TokenType.OR):
            op = self._advance().value
            right = self._parse_logical_and()
            left = LogicalExpr(op="||", left=left, right=right, line=left.line)
        return left

    def _parse_logical_and(self) -> ASTNode:
        left = self._parse_bitwise_or()
        while self._check(TokenType.LOGICAL_AND, TokenType.AND):
            op = self._advance().value
            right = self._parse_bitwise_or()
            left = LogicalExpr(op="&&", left=left, right=right, line=left.line)
        return left

    def _parse_bitwise_or(self) -> ASTNode:
        left = self._parse_bitwise_xor()
        while self._check(TokenType.BITWISE_OR):
            self._advance()
            right = self._parse_bitwise_xor()
            left = BinaryExpr(op="|", left=left, right=right, line=left.line)
        return left

    def _parse_bitwise_xor(self) -> ASTNode:
        left = self._parse_bitwise_and()
        while self._check(TokenType.BITWISE_XOR):
            self._advance()
            right = self._parse_bitwise_and()
            left = BinaryExpr(op="^", left=left, right=right, line=left.line)
        return left

    def _parse_bitwise_and(self) -> ASTNode:
        left = self._parse_equality()
        while self._check(TokenType.BITWISE_AND):
            self._advance()
            right = self._parse_equality()
            left = BinaryExpr(op="&", left=left, right=right, line=left.line)
        return left

    def _parse_equality(self) -> ASTNode:
        left = self._parse_relational()
        while self._check(TokenType.EQUALS, TokenType.NOT_EQUALS,
                          TokenType.STRICT_EQUALS, TokenType.STRICT_NOT_EQUALS):
            op_tok = self._advance()
            right = self._parse_relational()
            # Map === to == for Python (value equality)
            op = "==" if op_tok.type in (TokenType.EQUALS, TokenType.STRICT_EQUALS) else "!="
            left = BinaryExpr(op=op, left=left, right=right, line=left.line)
        return left

    def _parse_relational(self) -> ASTNode:
        left = self._parse_shift()
        while self._check(TokenType.LESS_THAN, TokenType.GREATER_THAN,
                          TokenType.LESS_EQUAL, TokenType.GREATER_EQUAL,
                          TokenType.INSTANCEOF, TokenType.IN_OP):
            op_tok = self._advance()
            right = self._parse_shift()
            if op_tok.type == TokenType.INSTANCEOF:
                left = InstanceofExpr(left=left, right=right, line=left.line)
            elif op_tok.type == TokenType.IN_OP:
                left = InExpr(key=left, obj=right, line=left.line)
            else:
                left = BinaryExpr(op=op_tok.value, left=left, right=right, line=left.line)
        return left

    def _parse_shift(self) -> ASTNode:
        left = self._parse_additive()
        while self._check(TokenType.LEFT_SHIFT, TokenType.RIGHT_SHIFT,
                          TokenType.UNSIGNED_RIGHT_SHIFT):
            op = self._advance().value
            right = self._parse_additive()
            left = BinaryExpr(op=op, left=left, right=right, line=left.line)
        return left

    def _parse_additive(self) -> ASTNode:
        left = self._parse_multiplicative()
        while self._check(TokenType.PLUS, TokenType.MINUS):
            op = self._advance().value
            right = self._parse_multiplicative()
            left = BinaryExpr(op=op, left=left, right=right, line=left.line)
        return left

    def _parse_multiplicative(self) -> ASTNode:
        left = self._parse_exponent()
        while self._check(TokenType.MULTIPLY, TokenType.DIVIDE,
                          TokenType.MODULO, TokenType.FLOOR_DIVIDE):
            op = self._advance().value
            right = self._parse_exponent()
            left = BinaryExpr(op=op, left=left, right=right, line=left.line)
        return left

    def _parse_exponent(self) -> ASTNode:
        left = self._parse_unary()
        if self._check(TokenType.POWER):
            self._advance()
            right = self._parse_exponent()
            return BinaryExpr(op="**", left=left, right=right, line=left.line)
        return left

    def _parse_unary(self) -> ASTNode:
        line = self._line()
        if self._check(TokenType.LOGICAL_NOT, TokenType.NOT):
            self._advance()
            return UnaryExpr(op="not", operand=self._parse_unary(), line=line)
        if self._check(TokenType.MINUS):
            self._advance()
            return UnaryExpr(op="-", operand=self._parse_unary(), line=line)
        if self._check(TokenType.PLUS):
            self._advance()
            return UnaryExpr(op="+", operand=self._parse_unary(), line=line)
        if self._check(TokenType.BITWISE_NOT):
            self._advance()
            return UnaryExpr(op="~", operand=self._parse_unary(), line=line)
        if self._check(TokenType.INCREMENT):
            self._advance()
            return UpdateExpr(op="++", operand=self._parse_unary(), prefix=True, line=line)
        if self._check(TokenType.DECREMENT):
            self._advance()
            return UpdateExpr(op="--", operand=self._parse_unary(), prefix=True, line=line)
        if self._check(TokenType.TYPEOF):
            self._advance()
            return TypeofExpr(argument=self._parse_unary(), line=line)
        if self._check(TokenType.DELETE):
            self._advance()
            return DeleteExpr(argument=self._parse_unary(), line=line)
        if self._check(TokenType.VOID):
            self._advance()
            return VoidExpr(argument=self._parse_unary(), line=line)
        if self._check(TokenType.AWAIT):
            self._advance()
            return AwaitExpr(argument=self._parse_unary(), line=line)
        if self._check(TokenType.YIELD):
            self._advance()
            delegate = bool(self._match(TokenType.MULTIPLY))
            arg = None if self._check(TokenType.SEMICOLON, TokenType.RIGHT_BRACE) else self._parse_assignment()
            return YieldExpr(argument=arg, delegate=delegate, line=line)
        return self._parse_postfix()

    def _parse_postfix(self) -> ASTNode:
        expr = self._parse_call_expr()
        line = self._line()
        if self._check(TokenType.INCREMENT):
            self._advance()
            return UpdateExpr(op="++", operand=expr, prefix=False, line=line)
        if self._check(TokenType.DECREMENT):
            self._advance()
            return UpdateExpr(op="--", operand=expr, prefix=False, line=line)
        return expr

    def _parse_call_expr(self) -> ASTNode:
        expr = self._parse_new_expr()
        while True:
            line = self._line()
            if self._check(TokenType.DOT):
                self._advance()
                prop = self._advance()
                expr = MemberExpr(obj=expr, prop=Identifier(name=prop.value, line=line),
                                  computed=False, line=line)
            elif self._check(TokenType.OPTIONAL_CHAIN):
                self._advance()
                if self._check(TokenType.LEFT_PAREN):
                    args = self._parse_args()
                    expr = CallExpr(callee=expr, args=args, optional=True, line=line)
                else:
                    prop = self._advance()
                    expr = MemberExpr(obj=expr, prop=Identifier(name=prop.value, line=line),
                                      computed=False, optional=True, line=line)
            elif self._check(TokenType.LEFT_BRACKET):
                self._advance()
                idx = self._parse_expression()
                self._expect(TokenType.RIGHT_BRACKET)
                expr = MemberExpr(obj=expr, prop=idx, computed=True, line=line)
            elif self._check(TokenType.LEFT_PAREN):
                args = self._parse_args()
                expr = CallExpr(callee=expr, args=args, line=line)
            elif self._check(TokenType.TEMPLATE_STRING):
                # tagged template literal
                tmpl = self._parse_primary()
                expr = TaggedTemplateExpr(tag=expr, template=tmpl, line=line)
            else:
                break
        return expr

    # Token types that can start a normal primary expression (not kwarg names)
    _PRIMARY_STARTERS = {
        TokenType.IDENTIFIER, TokenType.NUMBER, TokenType.STRING,
        TokenType.TEMPLATE_STRING, TokenType.TRUE, TokenType.FALSE,
        TokenType.NULL, TokenType.UNDEFINED, TokenType.THIS, TokenType.SUPER,
        TokenType.PRINT, TokenType.INPUT_FN,
        TokenType.LEFT_PAREN, TokenType.LEFT_BRACKET, TokenType.LEFT_BRACE,
        TokenType.FUNCTION, TokenType.ASYNC, TokenType.SPREAD,
        TokenType.NOT, TokenType.MINUS, TokenType.PLUS, TokenType.BITWISE_NOT,
        TokenType.TYPEOF, TokenType.DELETE, TokenType.VOID, TokenType.AWAIT,
        TokenType.YIELD, TokenType.NEW, TokenType.INCREMENT, TokenType.DECREMENT,
    }

    def _parse_args(self) -> list[ASTNode]:
        self._expect(TokenType.LEFT_PAREN)
        args = []
        while not self._check(TokenType.RIGHT_PAREN, TokenType.EOF):
            if self._check(TokenType.SPREAD):
                self._advance()
                args.append(SpreadElement(argument=self._parse_assignment(), line=self._line()))
            elif (self._peek().type not in self._PRIMARY_STARTERS
                  and self._peek(1).type == TokenType.ASSIGN):
                # reserved keyword used as keyword-argument name: e.g., کلاس="primary"
                kw_tok = self._advance()
                self._advance()  # consume '='
                val = self._parse_assignment()
                args.append(AssignExpr(
                    op="=",
                    left=Identifier(name=kw_tok.value, line=kw_tok.line),
                    right=val,
                    line=kw_tok.line,
                ))
            else:
                args.append(self._parse_assignment())
            if not self._match(TokenType.COMMA):
                break
        self._expect(TokenType.RIGHT_PAREN)
        return args

    def _parse_new_expr(self) -> ASTNode:
        line = self._line()
        if self._match(TokenType.NEW):
            callee = self._parse_new_expr()
            args = self._parse_args() if self._check(TokenType.LEFT_PAREN) else []
            return NewExpr(callee=callee, args=args, line=line)
        return self._parse_left_hand_side()

    def _parse_left_hand_side(self) -> ASTNode:
        return self._parse_primary()

    # ── primary expressions ───────────────────────────────────────────────────

    def _parse_primary(self) -> ASTNode:
        t = self._peek()
        line = t.line

        # literals
        if t.type == TokenType.NUMBER:
            self._advance()
            return NumberLiteral(value=t.value, line=line)

        if t.type == TokenType.STRING:
            self._advance()
            return StringLiteral(value=t.value, line=line)

        if t.type == TokenType.TEMPLATE_STRING:
            self._advance()
            parsed_parts = []
            for kind, content in t.value:
                if kind == "text":
                    parsed_parts.append(("text", content))
                else:
                    from .lexer import Lexer as L
                    sub_tokens = L(content).tokenize()
                    sub_ast = Parser(sub_tokens).parse()
                    expr_node = sub_ast.body[0].expression if sub_ast.body else StringLiteral(value="", line=line)
                    parsed_parts.append(("expr", expr_node))
            return TemplateLiteral(parts=parsed_parts, line=line)

        if t.type == TokenType.TRUE:
            self._advance(); return BooleanLiteral(value=True, line=line)
        if t.type == TokenType.FALSE:
            self._advance(); return BooleanLiteral(value=False, line=line)
        if t.type == TokenType.NULL:
            self._advance(); return NullLiteral(line=line)
        if t.type == TokenType.UNDEFINED:
            self._advance(); return UndefinedLiteral(line=line)
        if t.type == TokenType.THIS:
            self._advance(); return ThisExpression(line=line)
        if t.type == TokenType.SUPER:
            self._advance(); return SuperExpression(line=line)

        # print / input as identifiers
        if t.type == TokenType.PRINT:
            self._advance(); return Identifier(name="لکھو", line=line)
        if t.type == TokenType.INPUT_FN:
            self._advance(); return Identifier(name="پڑھو", line=line)

        # grouping or arrow function
        if t.type == TokenType.LEFT_PAREN:
            return self._parse_paren_or_arrow()

        # array literal
        if t.type == TokenType.LEFT_BRACKET:
            return self._parse_array_literal()

        # object literal
        if t.type == TokenType.LEFT_BRACE:
            return self._parse_object_literal()

        # function expression
        if t.type == TokenType.FUNCTION:
            return self._parse_func_expr(is_async=False)
        if t.type == TokenType.ASYNC:
            if self._peek(1).type == TokenType.FUNCTION:
                self._advance()
                return self._parse_func_expr(is_async=True)
            if self._peek(1).type == TokenType.LEFT_PAREN:
                self._advance()
                return self._parse_arrow(is_async=True)
            if self._peek(1).type == TokenType.IDENTIFIER:
                self._advance()
                return self._parse_single_param_arrow(is_async=True)

        # spread in expression context
        if t.type == TokenType.SPREAD:
            self._advance()
            return SpreadElement(argument=self._parse_assignment(), line=line)

        # identifier
        if t.type == TokenType.IDENTIFIER:
            self._advance()
            # single-param arrow: name =>
            if self._check(TokenType.ARROW):
                self._advance()
                return self._parse_arrow_body(
                    params=[Param(name=Identifier(name=t.value, line=line), line=line)],
                    is_async=False, line=line
                )
            return Identifier(name=t.value, line=line)

        raise ParseError(f"Unexpected token {t.type.name} ({t.value!r})", line, t.column)

    def _parse_paren_or_arrow(self) -> ASTNode:
        line = self._line()
        # Peek ahead to detect arrow function
        save = self.pos
        try:
            params = self._parse_params()
            if self._check(TokenType.ARROW):
                self._advance()
                return self._parse_arrow_body(params=params, is_async=False, line=line)
        except Exception:
            pass
        self.pos = save

        # Regular grouping
        self._expect(TokenType.LEFT_PAREN)
        expr = self._parse_expression()
        self._expect(TokenType.RIGHT_PAREN)
        return expr

    def _parse_arrow(self, is_async: bool = False) -> ASTNode:
        line = self._line()
        params = self._parse_params()
        self._expect(TokenType.ARROW)
        return self._parse_arrow_body(params=params, is_async=is_async, line=line)

    def _parse_single_param_arrow(self, is_async: bool = False) -> ASTNode:
        line = self._line()
        name_tok = self._advance()
        self._expect(TokenType.ARROW)
        param = Param(name=Identifier(name=name_tok.value, line=line), line=line)
        return self._parse_arrow_body(params=[param], is_async=is_async, line=line)

    def _parse_arrow_body(self, params: list[Param], is_async: bool, line: int) -> ArrowFunction:
        if self._check(TokenType.LEFT_BRACE):
            body = self._parse_block()
            return ArrowFunction(params=params, body=body, is_async=is_async, is_expression=False, line=line)
        else:
            expr = self._parse_assignment()
            return ArrowFunction(params=params, body=expr, is_async=is_async, is_expression=True, line=line)

    def _parse_func_expr(self, is_async: bool = False) -> FunctionExpr:
        line = self._line()
        self._expect(TokenType.FUNCTION)
        is_gen = bool(self._match(TokenType.MULTIPLY))
        name = None
        if self._check(TokenType.IDENTIFIER):
            name = self._advance().value
        params = self._parse_params()
        body = self._parse_block()
        return FunctionExpr(name=name, params=params, body=body, is_async=is_async,
                            is_generator=is_gen, line=line)

    def _parse_array_literal(self) -> ArrayLiteral:
        line = self._line()
        self._expect(TokenType.LEFT_BRACKET)
        elements = []
        while not self._check(TokenType.RIGHT_BRACKET, TokenType.EOF):
            if self._check(TokenType.COMMA):
                elements.append(None)
            elif self._check(TokenType.SPREAD):
                self._advance()
                elements.append(SpreadElement(argument=self._parse_assignment(), line=self._line()))
            else:
                elements.append(self._parse_assignment())
            if not self._match(TokenType.COMMA):
                break
        self._expect(TokenType.RIGHT_BRACKET)
        return ArrayLiteral(elements=elements, line=line)

    def _parse_object_literal(self) -> ObjectLiteral:
        line = self._line()
        self._expect(TokenType.LEFT_BRACE)
        props = []
        while not self._check(TokenType.RIGHT_BRACE, TokenType.EOF):
            prop_line = self._line()
            if self._check(TokenType.SPREAD):
                self._advance()
                arg = self._parse_assignment()
                props.append(ObjectProperty(key="...", value=SpreadElement(argument=arg, line=prop_line),
                                             computed=False, line=prop_line))
            elif self._check(TokenType.LEFT_BRACKET):
                # computed key
                self._advance()
                key = self._parse_assignment()
                self._expect(TokenType.RIGHT_BRACKET)
                self._expect(TokenType.COLON)
                val = self._parse_assignment()
                props.append(ObjectProperty(key=key, value=val, computed=True, line=prop_line))
            else:
                key_tok = self._advance()
                key = key_tok.value
                if self._check(TokenType.LEFT_PAREN):
                    # method shorthand
                    params = self._parse_params()
                    body = self._parse_block()
                    val = FunctionExpr(name=key, params=params, body=body, line=prop_line)
                    props.append(ObjectProperty(key=key, value=val, method=True, line=prop_line))
                elif self._match(TokenType.COLON):
                    val = self._parse_assignment()
                    props.append(ObjectProperty(key=key, value=val, line=prop_line))
                else:
                    # shorthand { x }
                    props.append(ObjectProperty(
                        key=key,
                        value=Identifier(name=key, line=prop_line),
                        shorthand=True, line=prop_line
                    ))
            if not self._match(TokenType.COMMA):
                break
        self._expect(TokenType.RIGHT_BRACE)
        return ObjectLiteral(properties=props, line=line)
