"""Deterministically prepare independent books; never generate text from eval answers.
Full originals and notices are retained in source_materials/.
The only test-aware step is the unchanged removal-only reserved-prefix guardrail.
"""
import hashlib
import json
import re
from pathlib import Path
from run_evals import load_suite, reserve_classroom_passages, reject_eval_leakage, word_tokens

ROOT = Path(__file__).resolve().parent


def chunk_text(text, max_tokens=47):
    chunks = []
    for unit in re.split(r'(?<=[.!?])\s+|\n+', text):
        tokens = word_tokens(unit)
        chunks.extend(' '.join(tokens[i:i+max_tokens]) for i in range(0, len(tokens), max_tokens))
    return chunks


def main():
    target = ROOT / 'corpus/source_expanded'
    target.mkdir(parents=True, exist_ok=True)
    sources = json.loads((ROOT / 'source_materials/sources.json').read_text())
    suite = load_suite(ROOT / 'evals/language_evals.json')
    records = []
    for source in sources:
        raw = (ROOT / 'source_materials' / source['original_file']).read_bytes()
        if hashlib.sha256(raw).hexdigest() != source['sha256']:
            raise ValueError('Source hash mismatch: ' + source['original_file'])
        text = raw.decode('utf-8-sig').replace('\r\n', '\n')
        start = re.search(r'^\*\*\* START OF .+?\*\*\*\s*$', text, re.M)
        end = re.search(r'^\*\*\* END OF .+?\*\*\*\s*$', text, re.M)
        if not start or not end:
            raise ValueError('Missing Gutenberg body markers')
        body = text[start.end():end.start()]
        # Underscores encode italics in both editions; plus signs encode bold in the grammar book.
        body = body.replace('_', '')
        if source['gutenberg_id'] == '7010':
            body = body.replace('+', '')
        paragraphs = [' '.join(x.split()) for x in re.split(r'\n\s*\n', body) if x.strip()]
        candidates = chunk_text('\n'.join(paragraphs))
        retained, separation = reserve_classroom_passages(candidates, suite)
        out = target / (source['original_file'].replace('_original', '_body'))
        result = '\n'.join(retained) + '\n'
        reject_eval_leakage(result, suite, str(out.relative_to(ROOT)))
        out.write_text(result, encoding='utf-8')
        records.append({**source, 'corpus_file': str(out.relative_to(ROOT)),
                        'candidate_passages': len(candidates), 'retained_passages': len(retained),
                        'retained_unique_passages': len(set(retained)), 'separation': separation,
                        'corpus_sha256': hashlib.sha256(out.read_bytes()).hexdigest()})
    report = {'selection': 'Complete bodies of two books selected by subject; no test-based entry selection.',
              'processing': 'Remove outer Gutenberg wrappers; remove italic underscores and grammar bold plus signs; reflow paragraphs; original 47-token chunking; removal-only reserved-prefix exclusion.',
              'no_answer_or_eval_output_used_to_generate_text': True, 'sources': records}
    (ROOT / 'source_materials/preparation_manifest.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps([{'file': r['corpus_file'], 'retained': r['retained_passages'], 'excluded': r['separation']['excluded_passages']} for r in records], indent=2))


if __name__ == '__main__':
    main()
