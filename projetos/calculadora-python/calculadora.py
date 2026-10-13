"""Calculadora desktop com Tkinter.

Recursos: operações básicas, porcentagem, potência, raiz quadrada,
histórico, atalhos de teclado e avaliação segura de expressões.
"""

import ast
import math
import operator
import tkinter as tk
from tkinter import messagebox, ttk


class ExpressionError(ValueError):
    """Erro para expressões matemáticas inválidas."""


def evaluate_expression(expression: str) -> float:
    """Avalia apenas operações matemáticas explicitamente permitidas."""
    operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
        ast.Mod: operator.mod,
    }

    def visit(node):
        if isinstance(node, ast.Expression):
            return visit(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in operators:
            left = visit(node.left)
            right = visit(node.right)
            if isinstance(node.op, ast.Pow) and abs(right) > 100:
                raise ExpressionError("Expoente muito grande.")
            try:
                result = operators[type(node.op)](left, right)
            except ZeroDivisionError as exc:
                raise ExpressionError("Não é possível dividir por zero.") from exc
            except (OverflowError, ValueError) as exc:
                raise ExpressionError("Operação matemática inválida.") from exc
            return result
        if isinstance(node, ast.UnaryOp) and type(node.op) in operators:
            return operators[type(node.op)](visit(node.operand))
        raise ExpressionError("Expressão inválida.")

    if not expression.strip():
        raise ExpressionError("Digite uma expressão primeiro.")
    if len(expression) > 120:
        raise ExpressionError("A expressão é longa demais.")

    try:
        tree = ast.parse(expression, mode="eval")
        result = visit(tree)
    except (SyntaxError, TypeError, RecursionError) as exc:
        raise ExpressionError("Confira os números e operadores.") from exc

    if isinstance(result, complex) or not math.isfinite(result):
        raise ExpressionError("O resultado não é um número real finito.")
    return result


def format_result(value: float) -> str:
    """Evita exibir casas decimais desnecessárias."""
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return f"{value:.10g}"


class CalculatorApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Calculadora Pro")
        self.root.geometry("380x570")
        self.root.minsize(340, 500)
        self.root.configure(bg="#151922")

        self.expression = tk.StringVar()
        self.status = tk.StringVar(value="Pronta")
        self.history: list[tuple[str, str]] = []
        self.just_calculated = False

        self._configure_style()
        self._build_interface()
        self._bind_keyboard()

    def _configure_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "History.Treeview",
            background="#202633",
            foreground="#f3f4f6",
            fieldbackground="#202633",
            rowheight=28,
            borderwidth=0,
        )
        style.configure(
            "History.Treeview.Heading",
            background="#2b3342",
            foreground="#ffffff",
            font=("Segoe UI", 10, "bold"),
        )

    def _build_interface(self):
        header = tk.Frame(self.root, bg="#151922")
        header.pack(fill="x", padx=18, pady=(18, 8))

        tk.Label(
            header, text="CALCULADORA PRO", bg="#151922", fg="#aab4c5",
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w")

        display_frame = tk.Frame(self.root, bg="#202633", padx=14, pady=12)
        display_frame.pack(fill="x", padx=16, pady=(8, 14))

        self.display = tk.Entry(
            display_frame,
            textvariable=self.expression,
            font=("Segoe UI", 25),
            justify="right",
            relief="flat",
            bd=0,
            bg="#202633",
            fg="#ffffff",
            insertbackground="#ffffff",
        )
        self.display.pack(fill="x", ipady=10)
        self.display.focus_set()

        tk.Label(
            self.root, textvariable=self.status, anchor="e",
            bg="#151922", fg="#9aa6ba", font=("Segoe UI", 9)
        ).pack(fill="x", padx=20, pady=(0, 8))

        buttons_frame = tk.Frame(self.root, bg="#151922")
        buttons_frame.pack(fill="both", expand=True, padx=16, pady=(0, 12))

        buttons = [
            [("C", "clear"), ("⌫", "backspace"), ("(", "paren"), (")", "paren"), ("÷", "operator")],
            [("7", "number"), ("8", "number"), ("9", "number"), ("%", "percent"), ("×", "operator")],
            [("4", "number"), ("5", "number"), ("6", "number"), ("x²", "square"), ("−", "operator")],
            [("1", "number"), ("2", "number"), ("3", "number"), ("√", "sqrt"), ("+", "operator")],
            [("±", "sign"), ("0", "number"), (".", "decimal"), ("xʸ", "power"), ("=", "equals")],
        ]

        for row_index, row in enumerate(buttons):
            buttons_frame.rowconfigure(row_index, weight=1)
            for col_index, (label, action) in enumerate(row):
                buttons_frame.columnconfigure(col_index, weight=1)
                color = "#2b3342"
                foreground = "#f3f4f6"
                if action == "operator" or action in {"percent", "square", "sqrt", "power"}:
                    color = "#35445b"
                if action == "equals":
                    color = "#3478f6"
                if action == "clear":
                    color = "#8b3540"
                button = tk.Button(
                    buttons_frame,
                    text=label,
                    command=lambda a=action, v=label: self._handle_button(a, v),
                    bg=color,
                    fg=foreground,
                    activebackground="#52627a",
                    activeforeground="#ffffff",
                    relief="flat",
                    bd=0,
                    font=("Segoe UI", 13, "bold"),
                    cursor="hand2",
                )
                button.grid(
                    row=row_index, column=col_index, sticky="nsew",
                    padx=3, pady=3, ipadx=2, ipady=6
                )

        footer = tk.Frame(self.root, bg="#151922")
        footer.pack(fill="x", padx=18, pady=(0, 12))
        tk.Button(
            footer, text="Ver histórico", command=self.show_history,
            bg="#151922", fg="#8db5ff", activebackground="#202633",
            activeforeground="#ffffff", relief="flat", bd=0,
            font=("Segoe UI", 10, "underline"), cursor="hand2"
        ).pack(side="left")
        tk.Label(
            footer, text="Enter = calcular  •  Esc = limpar",
            bg="#151922", fg="#778297", font=("Segoe UI", 8)
        ).pack(side="right")

    def _bind_keyboard(self):
        self.root.bind("<Return>", lambda _event: self.calculate())
        self.root.bind("<KP_Enter>", lambda _event: self.calculate())
        self.root.bind("<Escape>", lambda _event: self.clear())
        self.root.bind("<BackSpace>", lambda _event: self.backspace())
        self.root.bind("<Key>", self._on_key)

    def _on_key(self, event):
        char = event.char
        if char in "0123456789.()+-%":
            self._append(char)
        elif char in "+-*/^":
            mapped = {"*": "*", "/": "/", "^": "**"}.get(char, char)
            self._append(mapped)

    def _handle_button(self, action: str, value: str):
        if action == "clear":
            self.clear()
        elif action == "backspace":
            self.backspace()
        elif action == "equals":
            self.calculate()
        elif action == "number":
            self._append(value)
        elif action == "decimal":
            self._append(".")
        elif action == "operator":
            self._append({"×": "*", "÷": "/", "−": "-"}.get(value, value))
        elif action == "paren":
            self._append(value)
        elif action == "percent":
            self.apply_percent()
        elif action == "square":
            self.apply_square()
        elif action == "sqrt":
            self.apply_sqrt()
        elif action == "power":
            self._append("**")
        elif action == "sign":
            self.toggle_sign()

    def _append(self, value: str):
        current = self.expression.get()
        if self.just_calculated and (value.isdigit() or value == "."):
            current = ""
        self.just_calculated = False
        self.expression.set(current + value)
        self.status.set("")

    def clear(self):
        self.expression.set("")
        self.status.set("Pronta")
        self.just_calculated = False

    def backspace(self):
        current = self.expression.get()
        self.expression.set(current[:-1])
        self.just_calculated = False

    def _replace_with_transformation(self, transform):
        try:
            value = evaluate_expression(self.expression.get())
            transformed = transform(value)
            if not math.isfinite(transformed):
                raise ExpressionError("O resultado não é finito.")
            self.expression.set(format_result(transformed))
            self.status.set("Resultado atualizado")
            self.just_calculated = True
        except ExpressionError as exc:
            messagebox.showerror("Não foi possível calcular", str(exc), parent=self.root)

    def apply_percent(self):
        self._replace_with_transformation(lambda value: value / 100)

    def apply_square(self):
        self._replace_with_transformation(lambda value: value ** 2)

    def apply_sqrt(self):
        def square_root(value):
            if value < 0:
                raise ExpressionError("Não existe raiz quadrada real de número negativo.")
            return math.sqrt(value)
        self._replace_with_transformation(square_root)

    def toggle_sign(self):
        current = self.expression.get().strip()
        if not current:
            self.expression.set("-")
        elif current.startswith("-(") and current.endswith(")"):
            self.expression.set(current[2:-1])
        else:
            self.expression.set(f"-({current})")
        self.just_calculated = False

    def calculate(self):
        original = self.expression.get().strip()
        try:
            result = evaluate_expression(original)
            formatted = format_result(result)
            self.history.insert(0, (original, formatted))
            self.history = self.history[:100]
            self.expression.set(formatted)
            self.status.set(f"{original} = {formatted}")
            self.just_calculated = True
        except ExpressionError as exc:
            self.status.set("Confira a expressão")
            messagebox.showerror("Erro de cálculo", str(exc), parent=self.root)

    def show_history(self):
        window = tk.Toplevel(self.root)
        window.title("Histórico de cálculos")
        window.geometry("440x340")
        window.configure(bg="#151922")
        window.transient(self.root)

        tk.Label(
            window, text="HISTÓRICO", bg="#151922", fg="#ffffff",
            font=("Segoe UI", 12, "bold")
        ).pack(anchor="w", padx=14, pady=(14, 8))

        columns = ("expression", "result")
        table = ttk.Treeview(
            window, columns=columns, show="headings",
            style="History.Treeview", height=9
        )
        table.heading("expression", text="Expressão")
        table.heading("result", text="Resultado")
        table.column("expression", width=270)
        table.column("result", width=130, anchor="e")
        table.pack(fill="both", expand=True, padx=14, pady=6)

        for expression, result in self.history:
            table.insert("", "end", values=(expression, result))

        controls = tk.Frame(window, bg="#151922")
        controls.pack(fill="x", padx=14, pady=(4, 14))

        def clear_history():
            if messagebox.askyesno("Limpar histórico", "Deseja apagar todo o histórico?", parent=window):
                self.history.clear()
                for item in table.get_children():
                    table.delete(item)

        tk.Button(
            controls, text="Limpar histórico", command=clear_history,
            bg="#8b3540", fg="#ffffff", relief="flat", padx=10, pady=6
        ).pack(side="left")
        tk.Button(
            controls, text="Fechar", command=window.destroy,
            bg="#35445b", fg="#ffffff", relief="flat", padx=14, pady=6
        ).pack(side="right")


def main():
    root = tk.Tk()
    CalculatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
