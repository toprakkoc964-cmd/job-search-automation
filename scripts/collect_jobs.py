"""Bounded JobSpy collection. Records are leads, not verified jobs or applications."""
import argparse
import fcntl
import hashlib
import json
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'job-search' / 'data'


def write_json(path, value):
    temp = path.with_suffix('.tmp')
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')
    temp.replace(path)


def identity(job):
    url = str(job.get('job_url_direct') or job.get('job_url') or '')
    parts = urlsplit(url)
    query = [(k, v) for k, v in parse_qsl(parts.query) if not k.startswith('utm_') and k not in ('trk', 'refId', 'trackingId')]
    normalized = urlunsplit((parts.scheme, parts.netloc.lower(), parts.path.rstrip('/'), urlencode(sorted(query)), ''))
    if not normalized:
        normalized = '|'.join(str(job.get(k) or '').strip().lower() for k in ('company', 'title', 'location'))
    return hashlib.sha256(normalized.encode()).hexdigest()[:20]


def worker(query, output):
    from jobspy import scrape_jobs
    jobs = scrape_jobs(site_name=['indeed'], search_term=query['term'],
                       location=query['location'], country_indeed=query['country_indeed'],
                       results_wanted=10, hours_old=168, verbose=1)
    result = {'jobs': json.loads(jobs.to_json(orient='records', date_format='iso')),
              'errors': jobs.attrs.get('errors', {}),
              'warnings': jobs.attrs.get('warnings', {})}
    write_json(Path(output), result)


def collect(limit):
    DATA.mkdir(parents=True, exist_ok=True)
    # Prevent overlapping scheduled/manual runs from corrupting shared state.
    with (DATA / 'collector.lock').open('a') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            print('Another collection is running; skipped.')
            return
        state_path = DATA / 'state.json'
        state = json.loads(state_path.read_text()) if state_path.exists() else {'cursor': 0, 'runs': {}}
        config = ROOT / 'job-search/searches.json'
        if not config.is_file():
            raise SystemExit('Copy job-search/searches.example.json to job-search/searches.json and edit it first.')
        queries = json.loads(config.read_text())
        if not isinstance(queries, list) or not queries:
            raise SystemExit('Configure at least one search in job-search/searches.json.')
        now = datetime.now(timezone.utc)
        stamp = now.isoformat()
        records_path = DATA / 'leads.json'
        records = json.loads(records_path.read_text()) if records_path.exists() else {}
        reports = []
        for step in range(min(limit, len(queries))):
            query = queries[(state['cursor'] + step) % len(queries)]
            previous = state['runs'].get(query['id'])
            if previous and (now - datetime.fromisoformat(previous)).total_seconds() < 10800:
                reports.append({'query': query, 'status': 'cooldown'})
                continue
            with tempfile.TemporaryDirectory() as temporary:
                target = Path(temporary) / 'result.json'
                try:
                    run = subprocess.run([sys.executable, __file__, '--worker', json.dumps(query), str(target)],
                                         capture_output=True, text=True, timeout=50)
                    if run.returncode != 0:
                        result = {'jobs': [], 'errors': {'worker': run.stderr[-1500:] or f'exit {run.returncode}'}}
                    else:
                        result = json.loads(target.read_text())
                except subprocess.TimeoutExpired:
                    result = {'jobs': [], 'errors': {'worker': '50-second timeout; use web research fallback'}}
                new = 0
                for job in result['jobs']:
                    key = identity(job)
                    old = records.get(key, {})
                    new += not bool(old)
                    records[key] = {**job, 'id': key, 'first_seen': old.get('first_seen', stamp),
                                    'last_seen': stamp, 'verification': old.get('verification', 'unverified'),
                                    'queries': sorted(set(old.get('queries', []) + [query['id']]))}
                reports.append({'query': query, 'status': 'partial_failure' if result.get('errors') else 'completed',
                                'count': len(result['jobs']), 'new': new,
                                'errors': result.get('errors', {}), 'warnings': result.get('warnings', {})})
                state['runs'][query['id']] = stamp
        state['cursor'] = (state['cursor'] + min(limit, len(queries))) % len(queries)
        report = {'checked_at': stamp, 'runs': reports, 'total_leads': len(records)}
        write_json(records_path, records)
        write_json(state_path, state)
        write_json(DATA / 'latest-run.json', report)
        write_json(DATA / (now.strftime('%Y%m%dT%H%M%S%fZ') + '-run.json'), report)
        print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--limit', type=int, choices=range(1, 4), default=2)
    parser.add_argument('--worker', nargs=2, help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.worker:
        worker(json.loads(args.worker[0]), args.worker[1])
    else:
        collect(args.limit)
