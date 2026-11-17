"""Day 1 checks derived from the instructor's guide and supplied lab assertions."""
import ast
import contextlib
import io
import json
import os
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class Day1Tests(unittest.TestCase):
    def setUp(self):
        self.notebook = json.loads((ROOT / 'notebooks/murshid.ipynb').read_text(encoding='utf-8'))
        self.notebook['cells'] = [c for c in self.notebook['cells'] if c['cell_type'] == 'code']
        # Isolate the original milestone as later days extend the cumulative notebook.
        self.assertGreaterEqual(len(self.notebook['cells']), 3)
        self.notebook['cells'] = self.notebook['cells'][:3]
        self.expected = json.loads((ROOT / 'expected/baseline_results.json').read_text(encoding='utf-8'))
        self.previous = Path.cwd()
        self.temp = tempfile.TemporaryDirectory()
        os.chdir(self.temp.name)
        self.ns = {}

    def tearDown(self):
        os.chdir(self.previous)
        self.temp.cleanup()

    def execute(self):
        with contextlib.redirect_stdout(io.StringIO()):
            for cell in self.notebook['cells']:
                exec(compile(''.join(cell['source']), '<day1>', 'exec'), self.ns)

    def assert_baseline(self, rows):
        self.assertEqual(len(rows), 3)
        for actual, expected in zip(rows, self.expected):
            self.assertEqual(set(actual), {'trace_id', 'answer', 'model', 'latency_ms'})
            self.assertEqual(actual['answer'], expected['answer'])
            self.assertEqual(actual['model'], expected['model'])
            self.assertIsInstance(actual['trace_id'], str)
            self.assertTrue(actual['trace_id'])
            self.assertGreaterEqual(actual['latency_ms'], 0)

    def test_fresh_execution_baseline_and_saved_output(self):
        self.execute()
        self.assert_baseline(self.ns['baseline_results'])
        saved = json.loads(Path('murshid_outputs/baseline_results.json').read_text(encoding='utf-8'))
        self.assertEqual(saved, self.ns['baseline_results'])
        self.assertEqual(self.ns['client'].calls, 3)

    def test_repeat_execution(self):
        self.execute()
        self.execute()
        self.assert_baseline(self.ns['baseline_results'])
        self.assertEqual(self.ns['client'].calls, 3)

    def test_invalid_input_never_calls_client(self):
        self.execute()
        before = self.ns['client'].calls
        for value in ('', '  ', None, 12, []):
            with self.subTest(value=value):
                self.assertEqual(self.ns['ask'](value)['answer'], 'Please enter a valid question.')
                self.assertEqual(self.ns['client'].calls, before)

    def test_whitespace_and_unknown_question(self):
        self.execute()
        self.assertEqual(self.ns['ask']('  ' + self.ns['FAQ_EN'] + '  ')['answer'], self.expected[1]['answer'])
        self.assertEqual(self.ns['ask']('An unknown service question')['answer'], 'Please clarify the service you need.')
        self.assertEqual(self.ns['client'].calls, 5)

    def test_three_code_cells_standard_library_only(self):
        self.assertEqual(len(self.notebook['cells']), 3)
        allowed = {'json', 're', 'sys', 'time', 'uuid', 'pathlib', 'copy'}
        for index, cell in enumerate(self.notebook['cells'], 1):
            self.assertEqual(cell['cell_type'], 'code')
            source = ''.join(cell['source'])
            self.assertTrue(source.startswith(f'# DAY 1 - Cell {index}:'))
            for node in ast.walk(ast.parse(source)):
                if isinstance(node, ast.Import):
                    self.assertTrue(all(alias.name.split('.')[0] in allowed for alias in node.names))
                elif isinstance(node, ast.ImportFrom):
                    self.assertIn(node.module.split('.')[0], allowed)
                elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                    self.assertNotIn(node.func.id, {'eval', 'exec', '__import__'})


if __name__ == '__main__':
    unittest.main(verbosity=2)
