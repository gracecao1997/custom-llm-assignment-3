"""Check submitted evidence against the actual notebooks, sources and saved weights.
Run from any directory: python verify_submission.py
"""
import argparse
import hashlib
import json
import re
from pathlib import Path
from zipfile import ZipFile
import torch
from run_evals import load_model, load_suite, model_hash, reject_eval_leakage

ROOT = Path(__file__).resolve().parent
RUNS = ('source_starter', 'source_expanded', 'source_expanded_6000')
PINNED = {
    'run_evals.py': 'da87f28d128344807512e2bac1cfc662b37ac2c7e4a32b84c09f1950e92d67a0',
    'chat.py': '6152c8b7780f3b46fef5de38461adfc4b1a55df70ed106ca73ec5e9aded86d25',
    'evals/language_evals.json': 'e8affcd72841e3ed7da5c0b6b116327fe9f69c9abd66a1180d1d88ceaa3e17f7',
    'nanogpt_model.py': '7c01703240dbec5d554527dc666e35b3df8391d0b117fddc07afcf325a21d11c',
}


def read(path):
    return json.loads(path.read_text())


def check(condition, description):
    if not condition:
        raise AssertionError(description)


def audit(output_path=None):
    for file, expected in PINNED.items():
        check(hashlib.sha256((ROOT / file).read_bytes()).hexdigest() == expected, 'Source changed: ' + file)
    provenance = read(ROOT / 'source_materials/preparation_manifest.json')
    for item in provenance['sources']:
        check(hashlib.sha256((ROOT / 'source_materials' / item['original_file']).read_bytes()).hexdigest() == item['sha256'], 'Original textbook hash mismatch')
        check(hashlib.sha256((ROOT / item['corpus_file']).read_bytes()).hexdigest() == item['corpus_sha256'], 'Prepared textbook corpus changed')
    suite = load_suite(ROOT / 'evals/language_evals.json')
    expected_ids = {case['id'] for case in suite['cases']}
    reports = []
    for run in RUNS:
        folder = ROOT / 'llm_runs' / run
        config = read(folder / 'config.json')
        split = read(folder / 'split.json')
        corpus = (folder / 'corpus.txt').read_text()
        reject_eval_leakage(corpus, suite, run)
        check(not set(split['train']) & set(split['validation']), run + ' overlapping split')
        check(set(split['train']) | set(split['validation']) == set(corpus.splitlines()), run + ' corpus/split mismatch')
        check(set(split['evaluation_train']) <= set(split['train']), run + ' train panel')
        check(set(split['evaluation_validation']) <= set(split['validation']), run + ' validation panel')
        check(len(split['evaluation_train']) == len(split['evaluation_validation']) == 20, run + ' panel size')
        notebook = read(ROOT / (run + '_custom_llm.ipynb'))
        cells = [cell for cell in notebook['cells'] if cell['cell_type'] == 'code']
        check(all(c['execution_count'] is not None for c in cells), run + ' unexecuted cell')
        check(not any(o['output_type'] == 'error' for c in cells for o in c['outputs']), run + ' error output')
        check(any('image/svg+xml' in o.get('data', {}) for c in cells for o in c['outputs']), run + ' missing plot')
        stage_checks = []
        for stage, filename in [('untrained', 'model_untrained.pt'), ('final', 'model.pt')]:
            model, vocabulary, saved = load_model(folder / filename)
            identity = model_hash(model)
            result_dir = folder / 'language_evals' / stage
            rows = read(result_dir / 'eval_results.json')
            summary = read(result_dir / 'eval_summary.json')
            check(len(rows) == 48 and {r['id'] for r in rows} == expected_ids, run + '/' + stage + ' cases')
            check(read(result_dir / 'eval_cases.json') == suite, run + '/' + stage + ' suite changed')
            check(summary['model_sha256'] == identity, run + '/' + stage + ' model identity')
            check(sum(row['score'] for row in rows) == summary['overall']['correct'], run + '/' + stage + ' total')
            check(vocabulary == read(folder / 'tokenization.json')['vocabulary'], run + ' vocabulary mismatch')
            prior = ROOT / 'source_evidence' / ('rerun_' + run + '_' + stage) / 'eval_results.json'
            check(read(prior) == rows, run + '/' + stage + ' saved rerun mismatch')
            stage_checks.append({'stage': stage, 'cases': len(rows), 'model_sha256': identity,
                                 'scores_and_saved_rerun_consistent': True})
        inspection = read(folder / 'inspection.json')
        embedding = model.transformer.wte.weight.detach().cpu()[inspection['token_id']].tolist()
        check(embedding == inspection['embedding_after'], run + ' final inspection mismatch')
        checkpoint = read(folder / 'checkpoint.json')
        check(checkpoint['initial_embeddings'][inspection['token_id']] == inspection['embedding_before'], run + ' initial inspection mismatch')
        check(read(folder / 'training_summary.json')['completed_steps'] == config['training_steps'], run + ' incomplete training')
        with ZipFile(ROOT / 'llm_runs' / (run + '.zip')) as archive:
            for file in folder.rglob('*'):
                if file.is_file():
                    relative = file.relative_to(folder).as_posix()
                    check(archive.read(relative) == file.read_bytes(), run + ' archive mismatch: ' + relative)
        reports.append({'run': run, 'stages': stage_checks, 'notebook_complete': True,
                        'panels_and_split_valid': True, 'prefix_separation_passed': True,
                        'inspection_matches_weights': True, 'archive_byte_identical': True})
    for file in ['corpus.txt', 'split.json', 'tokenization.json']:
        check((ROOT / 'llm_runs/source_expanded' / file).read_bytes() == (ROOT / 'llm_runs/source_expanded_6000' / file).read_bytes(), 'follow-up changed ' + file)
    check(reports[1]['stages'][0]['model_sha256'] == reports[2]['stages'][0]['model_sha256'], 'follow-up changed initialization')
    chat = read(ROOT / 'source_evidence/chat_transcript.json')
    check(len(chat['turns']) >= 3, 'Insufficient chat turns')
    check(chat['model_sha256'] == reports[1]['stages'][1]['model_sha256'], 'chat uses different model')
    for target in re.findall(r'\]\(([^)]+)\)', (ROOT / 'README.md').read_text()):
        if '://' not in target and not target.startswith('#'):
            linked = (ROOT / target.split('#')[0]).resolve()
            check(linked.exists() or (output_path is not None and linked == output_path.resolve()), 'Broken README link: ' + target)
    return {'runs': reports, 'official_sources_unchanged': True,
            'followup_corpus_split_vocabulary_initial_weights_identical': True,
            'chat_matches_expanded_checkpoint': True, 'readme_file_links_valid': True,
            'limitation': 'Exact prefix rejection does not detect all semantic contamination; review teaching sources too.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, help='Optional JSON report path; default is read-only')
    args = parser.parse_args()
    report = audit(args.output)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2) + '\n')
    print('PASS: all notebooks, 288 stage/case records, weights, inspections, archives, separation, chat identity and README links.')


if __name__ == '__main__':
    main()
