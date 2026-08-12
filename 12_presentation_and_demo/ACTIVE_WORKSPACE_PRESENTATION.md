# LearnSphere AI Active Workspace Presentation

## Slide 1: Title

LearnSphere AI: Active Workspace and Deployment System

MindForgeAI Internship 2026, Chatake Innoworks Pvt. Ltd.

Team: Vaishnavi Mali, Nagweni Kumbhar, Aishwarya Ekanath

## Slide 2: Problem

- A working internship project needs safe ongoing updates.
- A single unstructured code file makes small UI changes difficult to trace.
- Static hosting and Python API hosting need separate, explicit integration.

## Slide 3: Solution

- Separate Git-based active workspace.
- Dedicated localhost at port 5051.
- Page-level frontend files and a shared style layer.
- Booklet, change map, test checklist, and Git workflow.

## Slide 4: System Architecture

Browser -> Frontend -> Flask API -> SQLite

GitHub Pages -> Runtime configuration -> Render API

GitHub push -> Actions -> Pages

## Slide 5: Page Structure

- Overview
- Planner
- Academic Library
- Practice and Insights
- Team and Internship Credits

## Slide 6: Change Workflow

1. Pull latest work.
2. Create a feature branch.
3. Run localhost:5051.
4. Edit mapped files.
5. Test, commit, push, and review.

## Slide 7: Quality and Safety

- Unit tests before every hand-off.
- No credentials, personal uploads, or databases in Git.
- CORS and runtime API configuration checked before release.
- Learning insights remain supportive and non-diagnostic.

## Slide 8: Demo Screenshot

Insert `12_presentation_and_demo/assets/active-workspace-home.png` after running the local portal.

## Slide 9: Conclusion

The active workspace makes the LearnSphere AI project easier to understand, safer to change, and ready for continuing team collaboration.

