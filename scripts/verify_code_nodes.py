#!/usr/bin/env python3
"""Verify all Code nodes in a Dify workflow YAML file.

Usage: python3 verify_code_nodes.py <workflow.yml>

Checks:
1. All code compiles with compile()
2. All main() functions handle None/empty inputs without crashing
"""

import sys
import re
import yaml


def verify_code_nodes(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    nodes = data['workflow']['graph']['nodes']
    code_nodes = [n for n in nodes if n['data'].get('type') == 'code']

    if not code_nodes:
        print("No Code nodes found.")
        return True

    passed = 0
    failed = 0

    for n in code_nodes:
        nid = n['id']
        title = n['data'].get('title', '?')
        code = n['data'].get('code', '')

        if not code.strip():
            print(f"SKIP: {nid} ({title}) - empty code")
            continue

        # 1. Compile check
        try:
            compile(code, f'<{nid}>', 'exec')
        except SyntaxError as e:
            print(f"COMPILE FAIL: {nid} ({title}): {e}")
            failed += 1
            continue

        # 2. Boundary test with None inputs
        args_match = re.search(r'def main\(([^)]*)\)', code)
        if not args_match:
            print(f"WARN: {nid} ({title}) - no main() function found, skipping runtime test")
            passed += 1
            continue

        arg_str = args_match.group(1).strip()
        arg_count = 0 if arg_str == '' else len(arg_str.split(','))

        try:
            local_ns = {}
            exec(code, local_ns)
            main_fn = local_ns.get('main')
            if main_fn is None:
                print(f"WARN: {nid} ({title}) - main not defined after exec")
                passed += 1
                continue

            test_args = [None] * arg_count
            result = main_fn(*test_args)

            if not isinstance(result, dict):
                print(f"RUNTIME FAIL: {nid} ({title}) - return value must be dict, got {type(result).__name__}")
                failed += 1
                continue

            print(f"OK: {nid} ({title}) - {arg_count} args, returns {list(result.keys())}")
            passed += 1

        except Exception as e:
            print(f"RUNTIME FAIL: {nid} ({title}): {type(e).__name__}: {e}")
            failed += 1

    print(f"\nResults: {passed} passed, {failed} failed, {len(code_nodes)} total")
    return failed == 0


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 verify_code_nodes.py <workflow.yml>")
        sys.exit(1)

    ok = verify_code_nodes(sys.argv[1])
    sys.exit(0 if ok else 1)
