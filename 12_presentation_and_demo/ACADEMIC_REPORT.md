# Academic Project Report — LearnSphere AI

## Abstract

LearnSphere AI is an AIML-enabled study operating system that consolidates students’ academic planning, personal learning resources, practice, reflection and progress signals. The project responds to fragmented study workflows in which schedules, notes, PDFs, recordings and assessment preparation are separated across tools. The local MVP provides authenticated, persistent student workspaces with subject management, task planning, resource upload, notes, quizzes, focus logging, diary entries and clearly bounded learning insights.

## Problem statement

Students often know what material they possess but not what action to take next. Traditional learning-management systems distribute content but rarely help an individual plan, practise retrieval, reflect on barriers, or turn observed behaviour into a manageable intervention.

## Objectives

1. Create a unified, student-owned study workspace.
2. Support daily planning, materials capture, recall practice and reflection.
3. Use AIML responsibly for contextual coaching, practice generation and indicative performance scenarios.
4. Provide a maintainable full-stack architecture suitable for iterative evaluation.

## Methodology

The work follows an iterative product-engineering cycle: user/job analysis, architecture design, MVP implementation, API testing, local deployment, and staged expansion. Flask provides a lightweight REST API; SQLite persists local demonstration data; JWT restricts personal workspace endpoints; a responsive browser client presents the experience. AI is designed behind a provider adapter and is not represented as a source of certain academic truth.

## Implemented modules

| Module | Evidence |
| --- | --- |
| Identity and workspace access | Registration, sign-in, JWT-protected endpoints |
| Learning organization | Subjects, tasks, notes, files and audio upload metadata |
| Study execution | Focus logging and daily diary |
| Practice | On-demand three-question active-recall quiz and score history |
| Learning analysis | Consistency signal, indicative mark scenario, adaptive suggestions |

## Results and evaluation plan

Automated API smoke tests verify account creation, protected access, planning, notes, and insight response. A future user study should recruit consenting students, measure time-to-plan, weekly retention, planned-versus-logged focus, quiz use, perceived clarity, and accessibility success. Claims about academic improvement require controlled evaluation and must not be inferred from engagement alone.

## Limitations and future work

The current quiz engine is a deterministic local starter, not a subject-grounded generative model. Uploaded files are stored locally and not parsed. Production delivery needs document extraction, retrieval evaluation, citations, PostgreSQL/object storage, scheduler/notifications, real voice transcription, data controls, model monitoring, and bias/privacy review.

## Conclusion

LearnSphere AI demonstrates a technically credible base for a human-centred academic companion. Its value lies in connecting planning and execution while retaining student agency, privacy and transparent limitations.
