"""
Восстанавливает в hw1.ipynb исходные cell IDs и metadata.
    python restore_notebook.py                   # ID и metadata
    python restore_notebook.py --clear-outputs   # и ещё убрать выводы ячеек, если нужно перепрогнать
Порядок ячеек сверяется с cell_ids.json.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
NOTEBOOK = HERE / 'hw1.ipynb'
CELL_KEYS = {'hw1', 'tags'}
NOTEBOOK_KEYS = {'hw1', 'kernelspec', 'language_info'}

reference = json.loads((HERE / 'cell_ids.json').read_text(encoding='utf-8'))
notebook = json.loads(NOTEBOOK.read_text(encoding='utf-8'))
cells = notebook['cells']

if len(cells) != len(reference):
    raise SystemExit(f'{len(cells)} cells in the notebook, {len(reference)} in cell_ids.json: nothing changed')

for index, (cell, expected) in enumerate(zip(cells, reference)):
    hw1 = cell['metadata'].get('hw1', {})
    actual = (cell['cell_type'], hw1.get('task_id'), hw1.get('role'))
    if actual != (expected['cell_type'], expected['task_id'], expected['role']):
        raise SystemExit(f'cell {index} differs from cell_ids.json: {actual}: nothing changed')

changed = 0
for cell, expected in zip(cells, reference):
    changed += cell['id'] != expected['id']
    cell['id'] = expected['id']
    cell['metadata'] = {key: value for key, value in cell['metadata'].items() if key in CELL_KEYS}
    if '--clear-outputs' in sys.argv and cell['cell_type'] == 'code':
        cell['outputs'] = []
        cell['execution_count'] = None
notebook['metadata'] = {key: value for key, value in notebook['metadata'].items() if key in NOTEBOOK_KEYS}

NOTEBOOK.write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
size = NOTEBOOK.stat().st_size / 2**20
print(f'restored {changed} cell IDs, metadata cleaned, notebook {size:.2f} MB')
