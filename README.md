# Job Search Automation

A local starter for researching job openings, verifying them on employer sites, and preparing tailored applications. It includes a rotating Indeed lead collector powered by JobSpy and an English onboarding workflow for Codex.

## Quick start

Requires Python 3.11+ on macOS or Linux. The collector uses POSIX file locking. On Windows, use WSL.

```bash
git clone https://github.com/toprakkoc964-cmd/job-search-automation.git
cd job-search-automation
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
cp job-search/searches.example.json job-search/searches.json
```

Edit the search configuration for your target roles and locations, then run:

```bash
.venv/bin/python scripts/collect_jobs.py --limit 2
```

The collector rotates through the configured searches and writes leads and a run report under `job-search/data/`. Review errors separately from empty results. The examples use the UK to demonstrate the configuration. Set `country_indeed` to the JobSpy country identifier for your own search.

## Start a Codex chat

Open the cloned folder as a Codex project, start a chat, and enter **Set up my job search**. Codex uses the project's `AGENTS.md` instructions to ask for:

- Target roles, seniority, and adjacent roles
- Location, work arrangement, relocation preferences, and any relevant work authorization limits
- Skills, experience, education, and languages
- Optional CV, public portfolio links, and application email
- Freelance preferences, upfront application budget, and exclusions

A clone contains no candidate profile. Codex writes confirmed answers to the local, git-ignored `profile/candidate.md`. A new chat needs a first message to begin onboarding.

## Workflow

1. Collect leads from Indeed and research other public sources relevant to your targets.
2. Verify promising listings on the employer's site. Check eligibility, cost, and duplicate postings.
3. Prepare a role-specific CV, form answers, or a freelance proposal using confirmed experience.
4. Record submissions and replies when you have evidence. A prepared package stays a draft.

For recurring research, configure a scheduled task in your own Codex workspace. Give it this project's folder and ask it to follow `AGENTS.md`. This repo does not provision a scheduler, mailbox integration, or automatic submission workflow.

## Privacy

Keep candidate profiles, CVs, job records, generated output, and credentials in the ignored local paths. Review staged files before committing. A public repository makes committed content visible.

## License

MIT. The JobSpy dependency is distributed under its own license.
