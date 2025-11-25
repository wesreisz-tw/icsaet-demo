# Task 04: MCP Prompt Definitions

**Story**: SCRUM-5 - Cursor MCP Server for ICAET Query Access  
**Task Sequence**: 4 of 9  
**Dependencies**: None (independent, can run in parallel with Task 03)

---

## Objective

Create three informative MCP prompts that help users understand ICAET, provide example queries, and guide them in formatting questions effectively.

---

## Scope

- Implement prompt definitions in `prompts.py`
- Create "ICAET Overview" prompt explaining what ICAET is
- Create "Example Questions" prompt with sample queries
- Create "Question Formatting" prompt with best practices
- Structure prompts for fastmcp framework consumption
- Add clear, concise, user-friendly content

---

## Acceptance Criteria

1. **ICAET Overview Prompt**
   - [ ] Prompt name: `icaet_overview` or similar
   - [ ] Explains what ICAET is (conference knowledge base)
   - [ ] Describes what knowledge it contains (talks, speakers, topics)
   - [ ] Explains how to use it from Cursor
   - [ ] Mentions it's a query interface to conference content
   - [ ] Length: 3-5 paragraphs, concise and clear

2. **Example Questions Prompt**
   - [ ] Prompt name: `example_questions` or similar
   - [ ] Provides 5-8 diverse example questions
   - [ ] Examples cover different query types:
     - Speaker-focused: "What did [Speaker] talk about?"
     - Topic-focused: "What sessions covered [Topic]?"
     - General: "What were the main themes?"
   - [ ] Each example is realistic and actionable
   - [ ] Shows variety in question complexity

3. **Question Formatting Prompt**
   - [ ] Prompt name: `formatting_guidance` or similar
   - [ ] Provides 5-7 tips for better questions
   - [ ] Tips include:
     - Be specific (mention speakers, topics, or sessions)
     - Ask one thing at a time
     - Use natural language
     - Reference specific talks when possible
   - [ ] Clear do's and don'ts format
   - [ ] Helps users get better results

4. **Prompt Structure**
   - [ ] Each prompt is a constant or function
   - [ ] Compatible with fastmcp prompt registration
   - [ ] Includes metadata (name, description)
   - [ ] Proper type hints

5. **Content Quality**
   - [ ] Professional but friendly tone
   - [ ] No technical jargon about MCP or implementation
   - [ ] Focused on user value
   - [ ] Accurate descriptions
   - [ ] Encouraging and helpful

6. **Code Quality**
   - [ ] Full type hints
   - [ ] Module-level docstring
   - [ ] Follows Python style guide
   - [ ] Passes ruff, black, mypy checks

---

## Required Inputs

**From Task 01**:
- Empty `prompts.py` file ready for implementation
- Knowledge of fastmcp prompt structure

**Domain Knowledge Needed**:
- Understanding of what ICAET conference is
- Types of questions users might ask
- What content/knowledge is available in the API

---

## Expected Outputs

### Implemented prompts.py
```python
# Key components (not full implementation):
- Three prompt definitions (constants or functions)
- Each with name, description, and content
- Structured for fastmcp consumption
- Type hints for all exports
```

### Prompt Content
Each prompt should be:
- Self-contained and understandable
- Helpful to users new to ICAET
- Encouraging exploration
- Clear and concise

### Example Structure
```python
ICAET_OVERVIEW = """
ICAET is a knowledge base containing...
[3-5 paragraphs]
"""

EXAMPLE_QUESTIONS = """
Here are some example questions you can ask:
- What did Leslie Miley talk about?
- [more examples]
"""

FORMATTING_GUIDANCE = """
Tips for better questions:
- Be specific...
- [more tips]
"""
```

---

## Handoff Criteria

**Ready for Task 05 when**:
1. All acceptance criteria met
2. Three prompts fully written with actual content
3. Content is clear, helpful, and user-friendly
4. Prompts structured correctly for fastmcp integration
5. No placeholder text or "TODO" comments
6. Linters report zero errors
7. Manual review confirms content quality

**Artifacts for Next Task**:
- Three complete prompt definitions
- Prompt content ready to display in Cursor
- Structure compatible with fastmcp prompt registration

---

## Task-Specific Constraints

- Content must be actual helpful text (no stubs or placeholders)
- Keep prompts concise (users will read them in Cursor)
- Avoid implementation details (MCP protocol, HTTP, etc.)
- Focus on user value and guidance
- Use markdown formatting for readability if fastmcp supports it
- Prompts are static (no dynamic content or parameters)
- Must work with fastmcp framework's prompt system

---

## Notes

If ICAET domain knowledge is unclear:
- Make reasonable assumptions about conference content
- Focus on general guidance that works for any Q&A system
- Example questions should be realistic and diverse
- Formatting guidance should be universal best practices

