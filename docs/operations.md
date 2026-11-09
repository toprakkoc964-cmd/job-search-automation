# Operating the workflow

## Rotate sources

| Pass | Sources | Check |
|---|---|---|
| Market discovery | Indeed via JobSpy and one local board in a target country | Role, language, region and recent postings |
| Remote discovery | Public remote boards such as We Work Remotely or Remotive | Eligible hiring countries, time zone and contract |
| Employer verification | Employer career pages and employer-linked job portals | Open status, original posting ID and application channel |

Treat board results as leads. Verify promising matches on employer pages, merge duplicates, and record access failures separately. Other boards are researched by the agent, outside the Indeed collector.

## Schedule local research

1. Finish onboarding and run a normal research pass in your project.
2. In the ChatGPT desktop app, create a recurring task for the project. Use the local checkout if the task needs your ignored candidate profile or tracker. Keep the app running and the computer on for local tasks.
3. Use a prompt such as this one.

   > Follow AGENTS.md. Run the configured collector once with limit 2. Rotate to the next source group, verify promising leads on employer pages, and update the local tracker. Prepare drafts for verified matches and report meaningful changes. Keep source failures separate from empty results.

4. Check the first scheduled run for the source group, duplicate handling, and saved local output. Confirm that an idle run avoids repeated notifications.

See [OpenAI Docs on scheduled tasks](https://learn.chatgpt.com/docs/automations).

## Track Gmail replies

1. Choose the application mailbox and connect it to ChatGPT through Gmail if your plan and workspace allow it. Verify the connected account before reading mail.
2. Search narrowly for known employer domains, subjects or application IDs. Match each message to a single application, then classify it as a receipt, interview, rejection, or general correspondence. Leave ambiguous matches for review.
3. Verify with a message explicitly labeled as a test. Record it separately from real applications and check that any test notification arrives once.
4. On eligible plans, a supported Gmail event can trigger a task in ChatGPT on web or mobile. A web task cannot directly update your local tracker. Confirm that your chosen environment can access both the mailbox and the tracker before relying on automatic updates. Otherwise, transfer the verified result into the local tracker during a project session.

The repository includes the workflow and templates. Mailbox authorization, scheduling, and external application submission are configured separately.
