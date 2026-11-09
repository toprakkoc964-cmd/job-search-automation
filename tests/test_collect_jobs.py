import io
import json
import subprocess
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from scripts import collect_jobs


class CollectorDemo(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        root = Path(directory.name)
        self.data = root / "job-search" / "data"
        self.data.parent.mkdir()
        config = [
            {"id": "frontend", "term": "junior frontend", "location": "UK", "country_indeed": "UK"},
            {"id": "qa", "term": "junior QA", "location": "UK", "country_indeed": "UK"},
        ]
        (self.data.parent / "searches.json").write_text(json.dumps(config))
        settings = patch.multiple(collect_jobs, ROOT=root, DATA=self.data)
        settings.start()
        self.addCleanup(settings.stop)
        stdout = redirect_stdout(io.StringIO())
        stdout.__enter__()
        self.addCleanup(stdout.__exit__, None, None, None)

    def read(self, name):
        return json.loads((self.data / name).read_text())

    def test_rotation_merges_tracking_url_variants_and_respects_cooldown(self):
        def worker(args, **kwargs):
            query = json.loads(args[-2])
            url = f"https://example.com/careers/frontend?utm_source={query['id']}"
            collect_jobs.write_json(Path(args[-1]), {"jobs": [{"job_url_direct": url}]})
            return subprocess.CompletedProcess(args, 0)

        with patch.object(collect_jobs.subprocess, "run", side_effect=worker) as run:
            collect_jobs.collect(1)
            first = self.read("latest-run.json")["runs"][0]
            self.assertEqual((first["query"]["id"], first["new"]), ("frontend", 1))

            collect_jobs.collect(1)
            second = self.read("latest-run.json")["runs"][0]
            self.assertEqual((second["query"]["id"], second["new"]), ("qa", 0))
            leads = list(self.read("leads.json").values())
            self.assertEqual(len(leads), 1)
            self.assertEqual(leads[0]["queries"], ["frontend", "qa"])

            collect_jobs.collect(1)
            self.assertEqual(self.read("latest-run.json")["runs"][0]["status"], "cooldown")
            self.assertEqual(run.call_count, 2)

    def test_timeout_is_distinct_from_successful_empty_results(self):
        def worker(args, **kwargs):
            if json.loads(args[-2])["id"] == "frontend":
                raise subprocess.TimeoutExpired(args, kwargs["timeout"])
            collect_jobs.write_json(Path(args[-1]), {"jobs": []})
            return subprocess.CompletedProcess(args, 0)

        with patch.object(collect_jobs.subprocess, "run", side_effect=worker):
            collect_jobs.collect(2)
        failed, empty = self.read("latest-run.json")["runs"]
        self.assertEqual(failed["status"], "partial_failure")
        self.assertIn("timeout", failed["errors"]["worker"])
        self.assertEqual(empty["status"], "completed")
        self.assertEqual(empty["count"], 0)
        self.assertEqual(empty["errors"], {})
