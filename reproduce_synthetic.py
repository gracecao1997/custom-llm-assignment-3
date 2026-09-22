"""Execute a submitted notebook without overwriting the submitted run or outputs.
Usage: python reproduce.py --experiment starter
"""
import argparse
from datetime import datetime, timezone
from pathlib import Path
import nbformat
from nbclient import NotebookClient


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--experiment', choices=['starter', 'expanded', 'expanded_6000', 'all'], default='all')
    parser.add_argument('--kernel', default='python3', help='Installed Jupyter kernel name')
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S_%fZ')
    experiments = ['starter', 'expanded', 'expanded_6000'] if args.experiment == 'all' else [args.experiment]
    for name in experiments:
        notebook = nbformat.read(root / (name + '_custom_llm.ipynb'), as_version=4)
        for cell in notebook.cells:
            if cell.cell_type == 'code':
                cell.outputs = []
                cell.execution_count = None
        client = NotebookClient(notebook, timeout=3600, kernel_name=args.kernel,
                                resources={'metadata': {'path': str(root)}})
        print('Executing', name, flush=True)
        try:
            client.execute()
        finally:
            target = root / ('reproduced_' + name + '_' + stamp + '.ipynb')
            nbformat.write(notebook, target)
            print('Saved executed notebook:', target, flush=True)
    print('New result folders appear under llm_runs/. Submitted runs were preserved.')


if __name__ == '__main__':
    main()
