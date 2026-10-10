# Week 2: Input, AI-Assisted Development, and Feedback

This lesson resumes after Week 1 setup. Students practice the weekly `git pull` routine, use Git Graph to see how the course repository changes, build a small Python adventure, use ChatGPT as a coding partner, and improve the program from peer feedback. This is still a Python foundations lesson: students must run, test, and explain every change.

## Learning objectives

By the end of class, students can:

- Update the course repository with `git pull`.
- Open repository history with the Git Graph VS Code extension.
- Explain the difference between writing, saving, and running Python code.
- Use `input()`, variables, and conditional logic in a small program.
- Ask ChatGPT for a bounded code change and verify the result.
- Collect peer feedback and implement one improvement.
- Identify early questions about scale, reliability, and cybersecurity.

## Saturday agenda

| Time | Block |
| --- | --- |
| 9:00-9:15 | Build-a-Bot Introductions icebreaker |
| 9:15-9:30 | Weekly `git pull` routine and Git Graph setup |
| 9:30-9:45 | Run the starter project and review objectives |
| 9:45-10:25 | Write, save, run, observe, and fix |
| 10:25-10:35 | Break |
| 10:35-10:50 | Install or open ChatGPT |
| 10:50-11:20 | Prompting and verification workshop |
| 11:20-11:30 | Break |
| 11:30-12:25 | Build any Python app and make it easy to launch |
| 12:25-12:40 | Peer testing and written feedback |
| 12:40-12:50 | Implement one peer-requested improvement |
| 12:50-1:00 | Scale, security, and engineering reflection |

## Key vocabulary

- **Source code:** Human-readable instructions saved in a program file.
- **Run:** Ask Python to execute the saved instructions.
- **Input:** Information a user gives a program.
- **Variable:** A name that stores a value.
- **Conditional:** Code that chooses an action based on a condition.
- **Prompt:** An instruction or question given to an AI system.
- **Verification:** Evidence that a result works as intended.
- **Scale:** The ability to continue working as usage grows.
- **Cybersecurity:** Protecting systems, accounts, and data from harm.

## Icebreaker: Build-a-Bot Introductions

Use these four steps:

1. Find a partner you did not work with last week.
2. Take two minutes to invent a robot. Give it a name, a useful job, and one funny bug.
3. Take turns explaining your robots. Ask your partner one question.
4. Introduce your partner's robot to the class.

Example: **SnackBot brings snacks, but it only delivers broccoli.**

Partners then introduce each other's robots to the class or a nearby pair. After sharing, ask: **Which bug would you fix first, and why?** The activity creates an early connection between creativity, user needs, bugs, and prioritization.

## Instructor-led sequence

1. Model `git status`, `git pull`, and `code .` from the repository root.
2. Install Git Graph with `code --install-extension mhutchie.git-graph` and open **Git Graph: View Git Graph** from the Command Palette.
3. Run [`examples/adventure_demo.py`](examples/adventure_demo.py).
4. Change one message, save, run again, and intentionally create a small syntax error.
5. Explain the cycle: write, save, run, observe, fix, and run again.
6. Explain that Python automatically prepares code for execution. Students do not use a separate compile command in this lesson.

## Guided ChatGPT exercise

Students may create any beginner Python app they can finish, explain, and test. The supplied [`assignment/adventure.py`](assignment/adventure.py) is an optional starting point. They may use ChatGPT, but each prompt must:

1. State the desired behavior.
2. Include only the relevant code and error message.
3. Preserve the parts that already work.
4. Ask for a way to verify the change.

Use [`exercises/chatgpt-prompt-guide.md`](exercises/chatgpt-prompt-guide.md) for the prompt pattern. Treat every response as a draft. Read the proposed code, predict what it will do, run it, test multiple inputs, and revise it when needed.

Never paste passwords, private student information, API keys, or access tokens into ChatGPT.

## Project challenge

Create a Python app based on your own idea. It might be a game, quiz, calculator, interactive story, useful tool, or something else you want to build.

The finished app must:

- Have at least one clear action the user can take.
- Respond helpfully to an unexpected or blank input when the app accepts input.
- Include one feature developed with ChatGPT assistance.
- Include a working `start.bat` file that launches the program when double-clicked.
- Work when another student opens and tests it.

Students may also ask ChatGPT to add a restart option. Example prompt:

> When my app finishes, ask the user if they want to restart. Keep everything else working and explain the changes.

Students must be able to explain every submitted line, including AI-generated code.

## Peer testing and revision

Exchange projects with a partner and complete [`exercises/peer-feedback.md`](exercises/peer-feedback.md). The partner tests the launcher, tries expected and unexpected inputs, and requests one specific improvement.

The developer must implement one piece of peer feedback, run the project again, and write what changed. No Git commit is required this week.

## Engineering reflection

Discuss these questions after the revised programs work:

- What would fail first if one million people used this program overnight?
- How would the team protect accounts and user data from cyberattacks?
- What logs, tests, or alerts would help the team find problems?
- Which improvement would you add after learning more Python?
- If you revisited this project at the end of the course, what would you rebuild differently?

Engineering skill grows through repeated cycles of building, receiving feedback, studying failures, and improving the system.

## Exit ticket

1. What feature did you add today?
2. What did your peer ask you to improve?
3. What change did ChatGPT suggest, and how did you verify it?
4. What might break if the program suddenly had one million users?
5. What skill do you want your future engineering self to bring back to this project?

## Optional extensions

- Add a score or inventory variable.
- Let the player restart without closing the program.
- Reject blank names and unsupported choices.
- Ask ChatGPT for test cases rather than code, then implement the fixes yourself.

