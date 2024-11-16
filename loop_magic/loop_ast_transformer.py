import ast
from typing import Optional
from uuid import uuid4

from more_itertools import one


class LoopAstTransformer(ast.NodeTransformer):
    def generic_visit(self, node: ast.AST) -> ast.AST:
        super().generic_visit(node)

        if not hasattr(node, "body"):
            return node
        if not isinstance(node.body, list):
            return node

        new_body = []
        for stmt in node.body:
            if isinstance(stmt, ast.With):
                if any(
                    self.is_loop_call(expr.context_expr)
                    for expr in stmt.items
                ):
                    if len(stmt.items) != 1:
                        raise Exception(
                            "Loop(...) can only be the single expression within the with-block definitition"
                        )
                    stmt = self.replace_loop(stmt)
            new_body.append(stmt)

        node.body = new_body
        return node

    def is_loop_call(self, node: ast.expr) -> bool:
        return (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "Loop"
        )

    def replace_loop(self, node: ast.With) -> ast.AST:
        item = one(node.items)
        call = item.context_expr
        if not isinstance(call, ast.Call):
            raise AssertionError("not a Call")
        iter = one(call.args)

        vars = item.optional_vars
        if not isinstance(vars, (ast.Tuple, ast.List)):
            raise AssertionError()
        val_var, ctrl_var = vars.elts

        outer_block_name = f"_loop_control_{uuid4().hex}"
        inner_block_name = f"_loop_control_{uuid4().hex}"

        def loop_attr_call(attr: str, args: Optional[list[ast.expr]] = None) -> ast.Call:
            return ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id="Loop", ctx=ast.Load()),
                    attr=attr,
                    ctx=ast.Load(),
                ),
                args=args or [],
                keywords=[],
            )

        def code_block(block_name: str, body: list[ast.stmt]) -> ast.With:
            return ast.With(
                items=[
                    ast.withitem(
                        context_expr=loop_attr_call("code_block"),
                        optional_vars=ast.Name(id=block_name, ctx=ast.Store())
                    )
                ],
                body=body,
            )
        
        loop_control = ast.Assign(
            targets=[ctrl_var],
            value=loop_attr_call(
                "loop_control",
                [
                    ast.Name(id=outer_block_name, ctx=ast.Load()),
                    ast.Name(id=inner_block_name, ctx=ast.Load()),
                ],
            ),
        )

        return code_block(
            outer_block_name,
            [
                ast.For(
                    target=val_var,
                    iter=iter,
                    orelse=[],
                    body=[
                        code_block(
                            inner_block_name,
                            [
                                loop_control,
                                *node.body,
                            ],
                        ),
                    ],
                ),
            ]
        )
