This story [STORY_ID] needs to be broken down into sequential, independent tasks for implementation. 

INTENTION: We're creating atomic tasks to reduce complexity, enable focused implementation 
cycles, and provide clear progress milestones. Each task should build incrementally 
toward the complete story implementation.

Analyze the story specification and create task requirement files (task-01.md, task-02.md, etc.) 
where each task:
1. Is independently implementable and testable
2. Builds incrementally toward story completion
3. Has clear dependencies on previous tasks
4. Includes specific acceptance criteria
5. Can be completed in a single research-plan-execute cycle
6. Has explicit handoff criteria to the next task
7. Specifies required inputs from previous tasks
8. Defines expected outputs for subsequent tasks

Consider natural boundaries such as: data layer → business logic → API layer → UI layer,
or foundational setup → core implementation → integration → validation.

For each task, create a task-[N].md file that includes:
- Task objective and scope
- Acceptance criteria
- Dependencies on previous tasks
- Required inputs from previous task handoffs
- Expected outputs and handoff criteria
- Task-specific constraints

Provide the breakdown as a numbered sequence of task requirement files.

FILE ORGANIZATION:
- Create all task files in the same directory as the story being decomposed
- Use naming convention: task-01.md, task-02.md, etc. (zero-padded numbers)
- This co-location ensures easy reference and maintains story-task relationships
