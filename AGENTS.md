# Project Syncere Course Authoring Guide

These instructions apply to the entire repository.

## Audience and course constraints

- Write for 18-year-old students with little or no prior programming experience.
- Use Python 3.12 or newer on Windows computers.
- Classes meet every Saturday from 9:00 AM to 1:00 PM.
- Preserve two ten-minute breaks in every four-hour lesson.
- Plan only about 75% of available Saturdays. Keep flex time for setup, review, cancellations, and project recovery.
- Build toward three major projects: the December Python capstone, the team data application, and the final AI capstone.

## Weekly folder pattern

Create each new week as `week-NN-short-topic/` with this structure:

```text
week-NN-short-topic/
├── README.md
├── examples/
├── exercises/
├── assignment/
└── slides/
```

Omit a subfolder only when the lesson genuinely does not need it. Do not create empty placeholder files.

## Weekly README pattern

Every weekly `README.md` must include:

1. Lesson title and where it fits in the curriculum
2. Learning objectives written as observable student actions
3. Four-hour Saturday agenda with exact times
4. Key vocabulary and concepts
5. Instructor-led example or live-coding sequence
6. Guided exercise instructions
7. Project or challenge with a concrete artifact
8. Peer testing, sharing, or code-review instructions
9. Exit ticket or reflection questions
10. Optional extensions for students who finish early

Use the standard Saturday rhythm unless a project, showcase, field trip, or administrative requirement calls for an explicit variation:

| Time | Block |
| --- | --- |
| 9:00-9:20 | Do-now or computer science challenge |
| 9:20-9:40 | Community, review, and objectives |
| 9:40-10:25 | Focused lesson and live coding |
| 10:25-10:35 | Break |
| 10:35-11:20 | Guided Python lab |
| 11:20-11:30 | Break |
| 11:30-12:25 | Project or challenge |
| 12:25-12:45 | Share, debug, and peer review |
| 12:45-1:00 | Exit ticket and reflection |

Week 1 is an approved exception: reserve 9:00-9:30 for administrative tasks and begin technical instruction at 9:30.

## Slide deck pattern

- Add an editable PowerPoint deck to `week-NN-short-topic/slides/`.
- Follow the weekly agenda in presentation order so the instructor can advance through the day without rearranging slides.
- Include a title slide, agenda, objectives, concise concept slides, live-coding prompts, both break slides, guided-lab instructions, project instructions, peer-review prompts, and an exit ticket.
- Put detailed instructor guidance in speaker notes rather than crowding slides.
- Keep code large enough to read from the back of a classroom.
- Use the Project Syncere visual direction: deep navy, muted blue, teal, green, coral accents, white backgrounds, and Arial when available.
- Keep slide titles direct and student-facing. Avoid slogans and unnecessary jargon.

## Python materials

- Prefer the standard library before adding third-party packages.
- Keep starter code runnable even when student tasks remain marked with `TODO` comments.
- Use small functions, descriptive names, docstrings, and type hints when they improve clarity.
- Never place API keys, passwords, tokens, or student data in the repository.
- Use parameterized SQL for every database query containing values.
- Include a simple way to run each example from the repository root.
- Add or update tests in proportion to the lesson's difficulty.

## Project and AI guidance

- Scope projects so students can produce a working minimum version during the scheduled class time.
- Require a defined user, problem, inputs, processing, and outputs.
- Treat debugging, Git commits, documentation, and reflection as recurring practices rather than isolated topics.
- Introduce AI as one component of a solution, not as a substitute for programming fundamentals.
- Require AI projects to document evaluation cases, limitations, privacy concerns, safeguards, and meaningful AI assistance.

## Quality checks

- Run every Python example before committing it.
- Confirm local Markdown links resolve.
- Check that dates and times agree with the pacing workbook and curriculum roadmap.
- Render and visually inspect every PowerPoint deck before delivery.
- Do not commit generated caches, local databases, virtual environments, secrets, or temporary build files.
