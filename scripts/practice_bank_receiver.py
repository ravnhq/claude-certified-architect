#!/usr/bin/env python3
"""Receive browser-rendered practice-bank questions on loopback and checkpoint them."""
import hashlib
import html
import json
import re
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs

ROOT = Path(__file__).resolve().parents[1] / '.corpus' / 'practice-bank'
ORIGIN = 'http://127.0.0.1:8768'
EXAMS = {'CCAR-F': 480, 'CCAR-P': 456, 'CCDV-F': 524}
FORM = b'''<!doctype html><title>Practice-bank local collector</title>
<h1>Practice-bank local collector</h1>
<form method="post" action="/capture">
<label>Question batch <textarea name="payload" rows="12" cols="90"></textarea></label>
<button>Save batch</button></form>'''


def validate_record(record):
    if not isinstance(record, dict) or not isinstance(record.get('exam'), str) or record['exam'] not in EXAMS:
        raise ValueError('Unknown exam')
    for key in ('question', 'snapshot'):
        if not isinstance(record.get(key), str) or not record[key].strip():
            raise ValueError(f'Missing {key}')
    options = record.get('options')
    if not isinstance(options, list) or len(options) < 2:
        raise ValueError('Missing options')
    if any(not isinstance(option, str) or not option.strip() for option in options):
        raise ValueError('Invalid option')
    explanations = record.get('explanations')
    if not isinstance(explanations, list) or len(explanations) != len(options):
        raise ValueError('Missing explanations')
    if any(not isinstance(item, str) or not item.strip() for item in record['explanations']):
        raise ValueError('Empty explanation')
    correct = record.get('correct_answers')
    if not isinstance(correct, list) or not correct or any(item not in options for item in correct):
        raise ValueError('Missing or invalid correct answer')
    # Answer letters shuffle between sessions; the text defines deduplication.
    choices = sorted(re.sub(r'^[A-Z]\)\s*', '', item).strip() for item in options)
    content = json.dumps([record['question'].strip(), choices], ensure_ascii=False)
    record['fingerprint'] = hashlib.sha256(content.encode()).hexdigest()
    return record


def save_batch(batch):
    if not isinstance(batch, list) or not 1 <= len(batch) <= 60:
        raise ValueError('Expected 1 to 60 questions')
    records = [validate_record(record) for record in batch]
    for record in records:
        folder = ROOT / record['exam']
        folder.mkdir(parents=True, exist_ok=True)
        target = folder / f"{record['fingerprint']}.json"
        temporary = target.with_suffix('.tmp')
        temporary.write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n')
        temporary.replace(target)
    summary = {exam: {'collected': len(list((ROOT / exam).glob('*.json'))),
                      'published_total': total} for exam, total in EXAMS.items()}
    target = ROOT / 'status.json'
    temporary = target.with_suffix('.tmp')
    temporary.write_text(json.dumps(summary, indent=2) + '\n')
    temporary.replace(target)
    return summary


def export_banks():
    for exam, total in EXAMS.items():
        records = [json.loads(path.read_text()) for path in sorted((ROOT / exam).glob('*.json'))]
        (ROOT / f'{exam}.json').write_text(json.dumps(records, ensure_ascii=False, indent=2) + '\n')
        lines = [f'# {exam} — collected practice-bank questions', '',
                 f'{len(records)} unique questions collected; published bank: {total}.', '',
                 'Source content is preserved as supplied by the practice bank; answers are not independently verified.', '']
        for index, record in enumerate(records, 1):
            lines.extend([f'## {index}. {record["question"]}', ''])
            for option, explanation in zip(record['options'], record['explanations']):
                marker = ' **(correct)**' if option in record.get('correct_answers', []) else ''
                lines.extend([f'### {option}{marker}', '', explanation, ''])
        (ROOT / f'{exam}.md').write_text('\n'.join(lines))
        print(f'{exam}: {len(records)}/{total}', flush=True)


class Receiver(BaseHTTPRequestHandler):
    def reply(self, status, content, content_type='text/html; charset=utf-8'):
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Content-Security-Policy', "default-src 'none'; form-action 'self'")
        self.end_headers()
        self.wfile.write(content)

    def do_GET(self):
        if self.headers.get('Host') != '127.0.0.1:8768':
            self.reply(404, b'Not found')
            return
        if self.path == '/':
            self.reply(200, FORM)
        elif self.path == '/known':
            records = [json.loads(path.read_text()) for exam in EXAMS for path in (ROOT / exam).glob('*.json')]
            payload = [{key: record[key] for key in ('exam', 'question', 'options', 'correct_answers')}
                       for record in records]
            self.reply(200, ('<title>Collected questions</title><pre>' + html.escape(json.dumps(payload)) + '</pre>').encode())
        else:
            self.reply(404, b'Not found')

    def do_POST(self):
        if (self.path != '/capture' or self.headers.get('Origin') != ORIGIN
                or self.headers.get('Host') != '127.0.0.1:8768'):
            self.reply(403, b'Only the local collector form may submit')
            return
        try:
            length = int(self.headers.get('Content-Length', '0'))
            if not 0 < length <= 4_000_000:
                raise ValueError('Invalid batch size')
            fields = parse_qs(self.rfile.read(length).decode())
            summary = save_batch(json.loads(fields['payload'][0]))
        except (ValueError, KeyError, UnicodeError) as error:
            self.reply(400, str(error).encode(), 'text/plain; charset=utf-8')
            return
        self.reply(200, ('<!doctype html><title>Saved</title><h1>Saved</h1><pre>'
                        + json.dumps(summary, indent=2) + '</pre><a href="/">Next batch</a>').encode())

    def log_message(self, format, *args):
        pass


if __name__ == '__main__':
    if sys.argv[1:] == ['--export']:
        export_banks()
    elif sys.argv[1:]:
        raise SystemExit('Usage: practice_bank_receiver.py [--export]')
    else:
        print(f'Collector at {ORIGIN}; output: {ROOT}', flush=True)
        HTTPServer(('127.0.0.1', 8768), Receiver).serve_forever()
