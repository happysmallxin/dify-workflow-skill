#!/usr/bin/env python3
"""Extract and display all SQL nodes from a Dify workflow YAML file.

Usage: python3 verify_sql_nodes.py <workflow.yml> [--test-date YYYY-MM-DD]

Outputs each SQL query with template variables replaced by test dates,
ready for MCP MySQL verification.
"""

import sys
import re
import yaml
from datetime import datetime, timedelta


def extract_sql_nodes(filepath, test_date=None):
    if test_date is None:
        today = datetime.now()
        test_date = today.strftime('%Y-%m-%d')

    # Calculate end date (next day)
    end_date = (datetime.strptime(test_date, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')

    with open(filepath, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    nodes = data['workflow']['graph']['nodes']
    sql_nodes = []

    for n in nodes:
        d = n.get('data', {})
        if d.get('type') != 'tool':
            continue

        sql = d.get('tool_parameters', {}).get('query_sql', {}).get('value', '')
        if not sql.strip():
            continue

        # Replace template variables with test dates
        sql_test = re.sub(r"'{{#[^}]+\.start_time#}}'", f"'{test_date}'", sql)
        sql_test = re.sub(r"'{{#[^}]+\.end_time#}}'", f"'{end_date}'", sql_test)
        # Replace gid_list with a sample value
        sql_test = re.sub(
            r"{{#[^}]+\.gid_list#}}",
            "'8a818232958df2ae01958e8415d0016e','8a818232958df2ae01958e84edc20171'",
            sql_test
        )

        sql_nodes.append({
            'id': n['id'],
            'title': d.get('title', '?'),
            'original_sql': sql,
            'test_sql': sql_test
        })

    return sql_nodes, test_date, end_date


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 verify_sql_nodes.py <workflow.yml> [--test-date YYYY-MM-DD]")
        sys.exit(1)

    filepath = sys.argv[1]
    test_date = None

    for i, arg in enumerate(sys.argv):
        if arg == '--test-date' and i + 1 < len(sys.argv):
            test_date = sys.argv[i + 1]

    sql_nodes, start, end = extract_sql_nodes(filepath, test_date)

    print(f"Found {len(sql_nodes)} SQL nodes (test range: {start} ~ {end})\n")

    for i, sn in enumerate(sql_nodes):
        print(f"[{i+1}] {sn['title']} (id={sn['id']})")
        print(f"    Original: {sn['original_sql'][:100].strip()}...")
        print(f"    Test SQL: {sn['test_sql'][:150].strip()}...")
        print()

    print("Run each test SQL through MCP MySQL (mcp__mysql__sql_query) to verify.")
