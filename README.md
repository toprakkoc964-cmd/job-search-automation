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

The collector rotates through the configured searches and writes leads and a run report under `job-search/data/`. Review errors separately from empty results. The sample covers the UK, Germany, Canada, and the US. Replace those examples with your own target markets.

## Search across countries

Each query has a unique `id`, a role `term`, a `location`, and a `country_indeed` value from the [JobSpy country list](https://github.com/speedyapply/JobSpy#indeed-and-glassdoor). Add `"is_remote": true` to look for remote listings in that market. Existing configs can omit this field.

For broader discovery, Codex can also research public employer career pages, regional boards, and international remote boards. Those sources are searched separately from the Indeed collector. Confirm eligible hiring countries, time zones, contract type, and any work authorization or sponsorship requirements on the original listing. A remote listing in one market may accept applicants only from that market.

## Start a Codex chat

Open the cloned folder as a Codex project, start a chat, and enter **Set up my job search**. Codex uses the project's `AGENTS.md` instructions to ask for:

- Target roles, seniority, and adjacent roles
- Location, work arrangement, relocation preferences, and any relevant work authorization limits
- Skills, experience, education, and languages
- Optional CV, public portfolio links, and application email
- Freelance preferences, upfront application budget, and exclusions

A clone contains no candidate profile. Codex writes confirmed answers to the local, git-ignored `profile/candidate.md`. A new chat needs a first message to begin onboarding.

## Try the offline demo

Follow the [fictional candidate walkthrough](examples/demo.md) to see onboarding, a simulated collector run, a sample report, and an application draft. Run `python3 -m unittest discover -s tests -v` to check rotation, deduplication, cooldown, and source failures without a network connection.

## Workflow

1. Collect leads from Indeed and research other public sources relevant to your targets.
2. Verify promising listings on the employer's site. Check eligibility, cost, and duplicate postings.
3. Prepare a role-specific CV, form answers, or a freelance proposal using confirmed experience.
4. Record submissions and replies when you have evidence. A prepared package stays a draft.

Use the [report, tracker, and application templates](examples/templates.md) for local records. The [operations guide](docs/operations.md) covers source rotation, scheduled research, and Gmail reply tracking.

## How subagents are selected

When parallel delegation is available and authorized, Codex can assign two researchers. One covers the candidate's best-supported target roles. The other covers adjacent roles, freelance opportunities, or a different market, depending on the candidate's preferences. For example, a Flutter candidate could get one mobile researcher and one QA or application support researcher.

The coordinator runs JobSpy once, assigns distinct scopes, and merges verified results into one report. If subagents are unavailable, the coordinator can research the same scopes sequentially. See [subagent instructions](AGENTS.md#subagent-selection).

## Privacy

Keep candidate profiles, CVs, job records, generated output, and credentials in the ignored local paths. Review staged files before committing. A public repository makes committed content visible.

## License

MIT. The JobSpy dependency is distributed under its own license.
