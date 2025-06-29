import ast
import argparse
from pathlib import Path
from stdlib_list import stdlib_list

def find_imports(source_dir: Path) -> set[str]:
    imported_modules = set()

    for py_file in source_dir.rglob("*.py"):
        with py_file.open("r", encoding="utf-8") as f:
            try:
                node = ast.parse(f.read(), filename=str(py_file))
                for stmt in ast.walk(node):
                    if isinstance(stmt, ast.Import):
                        for alias in stmt.names:
                            imported_modules.add(alias.name.split(".")[0])
                    elif isinstance(stmt, ast.ImportFrom):
                        if stmt.module:
                            imported_modules.add(stmt.module.split(".")[0])
            except SyntaxError:
                print(f"⚠️ Syntax error in {py_file}")
    return imported_modules

def main():
    parser = argparse.ArgumentParser(description="Used third-party libraries finder")
    parser.add_argument("path", type=str, help="Path to Python source directory (e.g., ./src)")
    parser.add_argument("--python-version", type=str, default="3.11", help="Python version (e.g., 3.11)")
    args = parser.parse_args()

    source_dir = Path(args.path).resolve()
    std_libs = set(stdlib_list(args.python_version))
    used_imports = find_imports(source_dir)

    third_party = sorted([lib for lib in used_imports if lib not in std_libs])

    print("✅ 外部ライブラリ（標準ライブラリを除く）:")
    for name in third_party:
        print("-", name)

if __name__ == "__main__":
    main()
