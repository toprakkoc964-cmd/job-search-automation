# Offline walkthrough

All people, companies, listings, and evidence in this example are fictional. The `example.com` URLs are placeholders. Keep real answers and outputs in ignored directories.

## First chat

In Codex, enter **Set up my job search**. Example answers:

- Target junior frontend roles, with QA as an adjacent option.
- Based in the UK. Open to hybrid in Manchester or remote from the UK. No relocation.
- Built and published a small TypeScript project. Comfortable with HTML, CSS, and Git. English for work.
- Portfolio: https://example.com/avery-portfolio. Leave the application email unset during the demo.
- No freelance work in this example. Upfront budget is zero.

The coordinator saves confirmed answers to `profile/candidate.md` and chooses frontend and QA research scopes. It can run those scopes sequentially or delegate them when authorized.

## Run the offline collector demo

From the repository root, run:

```bash
python3 -m unittest discover -s tests -v
```

The tests simulate two search queries returning the same official posting URL with different tracking parameters. The first query adds a lead, the second merges it, and the next pass respects the cooldown. Another test simulates a timed-out source and a successful empty response. Tests use temporary files and make no network calls.

## Review the sample report

| ID | Employer and role | Source evidence | Eligibility | Status |
|---|---|---|---|---|
| DEMO-001 | Example Studio, Junior Frontend Developer | Fixture only. In this scenario the employer lists an open role at https://example.com/careers/junior-frontend. | UK remote in the fixture. Start date and language level should be confirmed in a real listing. | Draft prepared |

The coordinator records one lead for the two copies. In a live run, it needs real employer evidence before calling a listing active or eligible.

## Prepare the sample application

> I built a TypeScript project and published it so reviewers could try it without an account. I used Git to track changes and worked on the HTML and CSS for the interface. I would be glad to walk through the project and explain how I would approach a small frontend feature on your team.

Add verified contact details and a public portfolio link in a real draft. In this example, no application was submitted and no reply or follow-up date was recorded. Use the [templates](templates.md) to continue with a real lead.
