# Job Search Automation

## First chat

When the user opens this project and asks to set up or start their job search, check whether `profile/candidate.md` exists and has actual candidate information. If it is missing or empty, answer in English by default and begin with this intake. Ask only for details the user has not already supplied.

1. Which roles and seniority levels should we prioritize, and which adjacent roles are welcome?
2. Where are you based? Which countries or regions are in scope? Which work arrangements are acceptable, and where can you legally work or relocate? If you want remote work, confirm the country you would work from.
3. What are your strongest skills, education, languages, and relevant work or project experience? A CV is optional.
4. Which public portfolio links and application email should we use? These are optional during setup.
5. Should the search include freelance work? What upfront application budget and exclusions should we apply?

Accept partial answers. Never invent facts. Ask for follow-up only when it affects the next action. Store the confirmed answers in the ignored local file `profile/candidate.md` when authorized file access is available. Otherwise, return a local-saveable profile draft. Keep credentials and unnecessary sensitive identifiers out of this project.

## Host capabilities

Use the host’s available tools. If shell execution is unavailable, provide the collector command for the user to run. If web research is unavailable, leave listing verification pending and ask for the official listing or its contents.

## Research and preparation

- Build an ignored `job-search/searches.json` from the example and confirmed targets. Run the collector at most once per research pass with `--limit 2`. Treat its records as leads. If collection fails, use public employer career pages.
- Rotate through employer career pages, local job boards in the target countries, and international remote boards. Check the original listing for hiring countries, time-zone overlap, contract type, language, sponsorship, role level, and fees. Treat remote labels as leads and require evidence that the employer can hire in the candidate’s country. Keep unconfirmed eligibility separate from confirmed matches. Deduplicate using the official posting ID or company, role, and location. Mark unknown requirements as unknown.
- Save reports, application tracking, and tailored materials under ignored local directories. Use only confirmed candidate facts. Keep application drafts and confirmed submissions distinct.
- Default to zero upfront spending and draft-only preparation. No automated external submissions, outreach, inbox access, or scheduling is configured by this repository. Use a separately authorized account or workflow for those steps.
- For a hiring referral, ask a company leader who handles the named role. Discuss eligibility and share the CV with the referred hiring contact when appropriate.

## Subagent selection

Use up to two parallel research subagents when delegation is authorized and available. The coordinator still owns the run and works sequentially when delegation is unavailable.

1. **Primary-role researcher.** Assign the role family with the strongest overlap between the user's priorities and demonstrated experience. Focus on direct matches. For a mobile candidate, this could mean Flutter, iOS, and Android.
2. **Adjacent-role researcher.** Assign an adjacent family the user is open to, based on transferable skills and the amount of preparation needed. Examples include QA, application support, or junior backend. If freelance is a higher priority, assign freelance discovery instead. If there is only one target family, split it by market or source group.

Give each subagent a distinct scope, up to three public sources per pass, the target countries, work arrangement, experience level, and fee limit. Share only the candidate facts needed for matching. Ask for the employer, role, official URL, evidence the listing is open, hiring geography, key requirements, and any eligibility gaps. Separate direct matches, roles requiring preparation, and exploratory leads.

The coordinator runs JobSpy once and shares relevant leads. Subagents return research to the coordinator and do not rerun the collector or edit shared tracking files. The coordinator merges duplicates, checks promising findings against employer sources, and updates the local report. Subagents do not send applications or messages.
