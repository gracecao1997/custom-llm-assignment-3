"""Compare the latest fresh runs created by reproduce.py with submitted evidence."""
import argparse
import json
from pathlib import Path
from run_evals import load_model, model_hash

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path('results/my_fresh_training_comparison.json'))
    args = parser.parse_args()
    reports = []
    for name in ['source_starter', 'source_expanded', 'source_expanded_6000']:
        reference = ROOT / 'llm_runs' / name
        candidates = sorted(p for p in (ROOT / 'llm_runs').glob(name + '_20*') if p.is_dir())
        if not candidates:
            raise SystemExit('No fresh ' + name + ' run. Run python reproduce.py --experiment all first.')
        fresh = candidates[-1]
        identical = {}
        for file in ['corpus.txt', 'split.json', 'tokenization.json', 'history.json', 'inspection.json', 'temperature_comparison.json']:
            identical[file] = (reference / file).read_bytes() == (fresh / file).read_bytes()
        hashes = {}
        for stage, file in [('untrained', 'model_untrained.pt'), ('final', 'model.pt')]:
            a, _, _ = load_model(reference / file)
            b, _, _ = load_model(fresh / file)
            hashes[stage] = {'submitted': model_hash(a), 'fresh': model_hash(b)}
            identical[stage + '_weights'] = hashes[stage]['submitted'] == hashes[stage]['fresh']
            file = 'language_evals/' + stage + '/eval_results.json'
            identical[file] = (reference / file).read_bytes() == (fresh / file).read_bytes()
        reports.append({'experiment': name, 'fresh_run': str(fresh.relative_to(ROOT)),
                        'identical': identical, 'weight_hashes': hashes})
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(reports, indent=2) + '\n')
    if not all(all(r['identical'].values()) for r in reports):
        raise SystemExit('Differences recorded. Check the report and execution environment; do not replace submitted evidence.')
    print('PASS: all three fresh runs reproduce the numerical artifacts, model weights and all six result sets exactly.')


if __name__ == '__main__':
    main()
