# Week 4: Foundations Review and Cloud Computing

Week 4 is a flex and recovery lesson. Students revisit the Week 3 foundations before the course moves forward: variables, data types, input and conversion, conditionals, lists, loops, functions, parameters, return values, decomposition, and tracing.

The class uses a browser notebook so local setup does not consume the lesson. The notebook also creates a concrete introduction to cloud computing: student code runs on a remote computer, while the browser displays and controls the session. A Raspberry Pi gives students a physical example of the same basic computer resources that a cloud provider manages at much larger scale.

## Learning objectives

By the end of class, students can:

- Trace values through a short Python program and predict its output.
- Correct code that misuses types, conditionals, loops, or return values.
- Build a working program from variables, a list, a loop, a conditional, and functions.
- Explain the difference between code running locally and code running on a cloud computer.
- Identify compute, storage, and networking in the classroom notebook workflow.
- Describe a hyperscaler as a company that operates very large fleets of computing infrastructure.

## Before class

1. Open the [Week 4 review notebook in Google Colab](https://colab.research.google.com/github/lhernandez-sudo/project-syncere-cs-2027/blob/main/week-04-foundations-cloud/exercises/foundations-review.ipynb).
2. Run every cell from a student account on the classroom network.
3. Share the Colab link as a short URL or QR code.
4. Ask students to sign in to a Google account before 9:00 AM when possible.
5. Keep the notebook file available for upload at <https://colab.research.google.com/> if the GitHub link is temporarily unavailable.
6. If using the Raspberry Pi demonstration, connect it to a separate hotspot or known network before class. Do not make student access to the Pi a requirement.

Colab resources are temporary and availability can vary. Students should use **File > Save a copy in Drive** before editing and **File > Download > Download .ipynb** at the end of class.

## Saturday agenda

| Time | Block |
| --- | --- |
| 9:00-9:13 | Direct Week 3 review: values, decisions, and loops |
| 9:13-9:22 | Raspberry Pi, cloud computing, and the Colab runtime |
| 9:22-9:35 | Functions review, objectives, and Colab launch |
| 9:35-10:25 | Colab work block 1: values through loops |
| 10:25-10:35 | Break |
| 10:35-11:20 | Colab work block 2: functions and debugging |
| 11:20-11:30 | Break |
| 11:30-12:25 | Colab project: Engineering Output Tracker |
| 12:25-12:45 | Peer testing, tracing, and repair |
| 12:45-1:00 | Exit ticket and notebook download |

## Opening review: Week 3 concepts

Students answer the review questions displayed on slides 2 through 4. They only need paper or a notes app. They should not use Google, ChatGPT, or run the code during the first attempt. The purpose is to reveal what they remember and what still needs instruction.

Use the twenty minutes in three parts:

1. **9:00-9:08 — Individual attempt:** Display each review slide for about two minutes. Students answer every question they can and mark uncertain answers.
2. **9:08-9:13 — Partner comparison:** Partners compare answers and explain where they disagree. They may revise in a different color.
3. **9:13-9:20 — Class trace:** Return to slides 2 through 4, trace each code sample together, and record the correct answers. Ask students to explain why before confirming each answer. The answer key is in the speaker notes.

Do not grade the first attempt. Use the results to decide which concepts need the most time during the relay and guided lab.

## Key vocabulary

- **Trace:** Follow values and control flow one step at a time.
- **Variable:** A name that refers to a stored value.
- **Data type:** The kind of value, such as `str`, `int`, `float`, or `bool`.
- **Conditional:** Code that selects a path using a Boolean condition.
- **List:** An ordered collection of values.
- **Loop:** Code that repeats.
- **Function:** A named, reusable block of code.
- **Parameter:** A name that receives a value when a function runs.
- **Return value:** A result that a function sends back to its caller.
- **Local computing:** Code runs on the computer in front of the user.
- **Cloud computing:** Computing resources are reached through a network and provided on demand.
- **Compute:** CPU and memory used to run programs.
- **Storage:** A place that keeps notebooks, programs, or data.
- **Networking:** Connections that move requests and results between computers.
- **Data center:** A facility that contains and supports many computer systems.
- **Hyperscaler:** A company that operates computing infrastructure at very large scale. AWS, Microsoft Azure, and Google Cloud are common examples.

## Instructor-led relay

Open [`examples/concept_relay.py`](examples/concept_relay.py) or the matching section of the notebook. Repeat the Week 3 routine for every example:

1. **Read:** Name the inputs and stored values.
2. **Predict:** Write the output before running.
3. **Run:** Execute the example.
4. **Change:** Modify one value or condition.
5. **Explain:** Describe why the output changed.

Do not reveal an answer immediately after a wrong prediction. Trace the code with the class, update a small value table, and let students revise the prediction.

## Guided foundations repair lab

Students work through [`exercises/foundations-review.ipynb`](exercises/foundations-review.ipynb). The expanded notebook includes explanations, prediction prompts, trace tables, nine guided practices, checkpoints, debugging challenges, self-check tests, cloud-runtime exploration, and a staged final project. Its core repairs cover conversion, conditional boundaries, lists, loop accumulators, `while` loop stopping conditions, and return values.

Pairs stop after every checkpoint and compare traces. A student who finishes early explains one repair to another student without taking control of their keyboard.

## Cloud computing and Raspberry Pi demonstration

Hold up the Raspberry Pi and identify its processor, memory, storage, power, and network connection. Then map the classroom notebook:

| Classroom item | Cloud concept |
| --- | --- |
| Student browser | Client interface |
| Internet or school network | Networking |
| Colab runtime | Remote compute |
| Notebook copied to Drive | Persistent storage |
| Temporary files inside the runtime | Temporary storage |
| Google | Cloud service provider |

Ask: **Where did the code actually run? What would disappear if the runtime stopped? What did we save somewhere else?**

Optional Pi demonstration:

1. Run `python -m http.server 8000` in a folder containing a simple `index.html`.
2. Open the page from a second device on the same trusted network.
3. Explain that the Pi served a response to a client request.
4. Compare one small Pi with a provider that manages large groups of servers, storage systems, networks, facilities, and automation.

Use a separate hotspot if the school network blocks device-to-device traffic. The conceptual demonstration still works if only the instructor connects.

## Project: Engineering Output Tracker rebuild

Students complete the final section of the notebook, then transfer or compare their solution with [`assignment/output_tracker_rebuild.py`](assignment/output_tracker_rebuild.py).

The minimum artifact must:

- Ask for a name.
- Store at least three scores in a list.
- Use a loop to calculate the total.
- Calculate and return an average from a function.
- Use a conditional to choose useful feedback.
- Print a result that includes the student's name and average.

Students may use Google or ChatGPT for explanations. They must cite one source or record one AI prompt, describe what they changed, and trace every line they keep.

## Peer testing and code tracing

Partners use [`exercises/peer-check.md`](exercises/peer-check.md). Each reviewer runs a normal case and a boundary case, then traces one function call from argument to parameter to return value. The developer repairs one issue and reruns the same test.

## Exit ticket

1. What value does `input()` return before conversion?
2. When would you choose a `for` loop instead of a `while` loop?
3. What is the difference between `print()` and `return`?
4. Where did your notebook code run today?
5. Name one example of compute, storage, and networking from class.
6. Which Week 3 concept needs one more practice session?

## Optional extensions

- Reject scores outside 0 through 10.
- Keep asking after invalid input instead of ending the program.
- Add a function that returns the highest score without using `max()`.
- Compare a local run with the Colab run and list what stays the same.
- Research one hyperscaler service and classify it primarily as compute, storage, or networking.

## Instructor evidence of readiness

Move forward after most students can independently:

- Predict which conditional branch will run.
- Trace an accumulator through at least three loop iterations.
- Explain how an argument becomes a parameter.
- Use a returned value outside the function.
- Complete the minimum tracker without copying an unexplained solution.

