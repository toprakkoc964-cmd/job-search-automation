# Portfolio project coach

Use this workflow when the candidate selects a job listing or when verified listings reveal a useful skill gap. The coordinator gives the coach the relevant requirements, their source URLs, and only the confirmed candidate skills needed for comparison. Use a dedicated subagent when authorized and available. Otherwise, the coordinator follows these instructions directly.

1. Separate required skills, preferred skills, and unknowns. Explain which requirements the project will demonstrate and which remain outside its scope.
2. Reuse an existing brief if it covers the same gap. Otherwise, choose one realistic problem and two or three core skills. Write at most one brief per pass.
3. Include a user story, stack, milestones, concrete acceptance criteria, a first task, and a README checklist. Use synthetic data and keep credentials and private information out of public artifacts.
4. Let the candidate build the project. Offer hints, debugging help, and code review on request. Ask the candidate to explain one design decision and one failure case.
5. Save the brief under the ignored `output/portfolio/` directory, or return it as Markdown when file access is unavailable. Track brief ready, in progress, and complete. Record skills as personal project evidence only after reviewing the working result.

## Example brief using a fictional listing

A full-stack posting asks for Spring Boot, PostgreSQL, and React with TypeScript. Build a help desk where staff open requests and support agents move them from Open to In Progress to Resolved.

| Milestone | Acceptance criteria |
|---|---|
| API | A valid request returns 201. An empty title returns 400. An invalid status change is rejected. |
| Persistence | PostgreSQL stores requests and status history. Changing status and recording history succeed or roll back together. |
| UI | Staff can create and filter requests and inspect their history. Loading, empty, and error states are visible. |
| Public demo | The README includes setup and test commands, synthetic sample data, and two design decisions. |

**First task:** Implement `POST /tickets` with in-memory storage. Demonstrate the 201 and 400 responses, then explain where input validation happens.
