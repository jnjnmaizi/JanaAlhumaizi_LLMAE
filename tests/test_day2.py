"""Day 2 lab and homework checks against attributed instructor fixtures."""
import ast
import contextlib
import io
import json
import os
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class Day2Tests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.previous = Path.cwd()
        os.chdir(self.temp.name)

    def tearDown(self):
        os.chdir(self.previous)
        self.temp.cleanup()

    def execute(self, name, namespace=None):
        namespace = {} if namespace is None else namespace
        nb = json.loads((ROOT / name).read_text(encoding='utf-8'))
        nb['cells'] = [c for c in nb['cells'] if c['cell_type'] == 'code']
        if name == 'notebooks/murshid.ipynb':
            self.assertGreaterEqual(len(nb['cells']), 6)
            nb['cells'] = nb['cells'][:6]
        with contextlib.redirect_stdout(io.StringIO()):
            for cell in nb['cells']:
                exec(compile(''.join(cell['source']), name, 'exec'), namespace)
        return namespace

    def expected(self, name):
        return json.loads((ROOT / 'expected' / name).read_text(encoding='utf-8'))

    def test_five_cases_and_saved_report(self):
        ns = self.execute('notebooks/murshid.ipynb')
        self.assertEqual(ns['day2_results'], self.expected('day2_results.json'))
        self.assertEqual(json.loads(Path('murshid_outputs/day2_results.json').read_text()), ns['day2_results'])
        self.assertEqual(ns['RECORDS'], ns['INITIAL_RECORDS'])

    def test_invalid_schema_never_calls_status_tool(self):
        ns = self.execute('notebooks/murshid.ipynb')
        valid = {'service': 'application_status', 'city': 'Riyadh', 'request_id': 'REF-1001', 'needs_clarification': False}
        self.assertTrue(ns['validate_ticket'](valid))
        bad_values = [[], {}, dict(valid, extra=1), dict(valid, city='Mars'),
                      dict(valid, service=[]), dict(valid, needs_clarification=0),
                      dict(valid, needs_clarification='false'), dict(valid, request_id=42),
                      dict(valid, request_id='REF-10001'), dict(valid, request_id='REF-١٠٠١'),
                      dict(valid, request_id=None), dict(valid, needs_clarification=True)]
        def forbidden(*args, **kwargs):
            self.fail('Status tool called for a rejected request')
        ns['check_status'] = forbidden
        self.assertFalse(ns['validate_ticket'](None))
        for value in bad_values:
            with self.subTest(value=value):
                self.assertFalse(ns['validate_ticket'](value))
                result = ns['route']('REF-1001', ticket_override=value)
                self.assertEqual(result['code'], 'invalid_schema')
                self.assertEqual(result['tool_calls'], 0)
        for question in ('أريد حالة طلبي', 'ألغ طلبي REF-1001'):
            self.assertEqual(ns['route'](question)['tool_calls'], 0)

    def test_ownership_spoofing_and_read_only(self):
        ns = self.execute('notebooks/murshid.ipynb')
        route = ns['route']
        denied = route('REF-1002 demo-user-2', session='demo-user-1')
        self.assertEqual(denied['code'], 'access_denied')
        self.assertNotIn('approved', json.dumps(denied))
        self.assertEqual(denied['answer'], route('REF-9999')['answer'])
        self.assertEqual(route('REF-1002', session='demo-user-2')['code'], 'approved')
        self.assertEqual(route('cancel REF-1001')['tool_calls'], 0)
        self.assertEqual(ns['check_status']('REF-١٠٠١', ns['SESSION'])['status'], 'invalid_reference')
        self.assertEqual(ns['RECORDS'], ns['INITIAL_RECORDS'])

    def test_replay_and_day1_regression(self):
        ns = self.execute('notebooks/murshid.ipynb')
        ns = self.execute('notebooks/murshid.ipynb', ns)
        self.assertEqual(ns['day2_results'], self.expected('day2_results.json'))
        for result, expected in zip(ns['baseline_results'], self.expected('baseline_results.json')):
            self.assertEqual(result['answer'], expected['answer'])
            self.assertEqual(result['model'], expected['model'])
        for question, language in ((ns['FAQ_AR'], 'ar'), (ns['FAQ_EN'], 'en')):
            self.assertEqual(ns['route'](question)['answer'], ns['SERVICE_DIRECTORY'][language])
        calls = ns['client'].calls
        ns['ask']('   ')
        self.assertEqual(ns['client'].calls, calls)

    def test_homework_seven_cases_saved_report_and_replay(self):
        ns = self.execute('homework/day2_tools.ipynb')
        self.assertEqual(ns['result'], self.expected('tools_result.json'))
        self.assertEqual(json.loads(Path('results/tools_result.json').read_text()), ns['result'])
        ns = self.execute('homework/day2_tools.ipynb', ns)
        self.assertEqual(ns['result'], self.expected('tools_result.json'))

    def test_homework_validation_and_authorization_are_distinct(self):
        ns = self.execute('homework/day2_tools.ipynb')
        before = json.dumps(ns['RECORDS'], sort_keys=True)
        call = {'name': 'check_status', 'arguments': {'reference': 'REF-1002'}}
        self.assertEqual(ns['dispatch'](call, 'demo-user-1'), {'code': 'unavailable'})
        self.assertEqual(ns['dispatch'](call, 'demo-user-2'), {'code': 'ok', 'status': 'approved'})
        for reference in ('REF-١٠٠١', 'REF-10001', None):
            self.assertEqual(ns['dispatch']({'name': 'check_status', 'arguments': {'reference': reference}}, 'demo-user-1'), {'code': 'invalid_arguments'})
        self.assertEqual(json.dumps(ns['RECORDS'], sort_keys=True), before)

    def test_scope_and_standard_library(self):
        for path, count in (('notebooks/murshid.ipynb', 6), ('homework/day2_tools.ipynb', 2)):
            nb = json.loads((ROOT / path).read_text())
            nb['cells'] = [c for c in nb['cells'] if c['cell_type'] == 'code']
            if path == 'notebooks/murshid.ipynb':
                self.assertGreaterEqual(len(nb['cells']), count)
                nb['cells'] = nb['cells'][:count]
            self.assertEqual(len(nb['cells']), count)
            for cell in nb['cells']:
                self.assertEqual(cell['cell_type'], 'code')
                for node in ast.walk(ast.parse(''.join(cell['source']))):
                    if isinstance(node, ast.Import):
                        self.assertTrue(all(a.name in {'json', 're', 'sys', 'time', 'uuid'} for a in node.names))
                    elif isinstance(node, ast.ImportFrom):
                        self.assertIn(node.module, {'pathlib', 'copy'})


if __name__ == '__main__':
    unittest.main(verbosity=2)
