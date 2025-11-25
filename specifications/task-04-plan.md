# Task 04 Implementation Plan: MCP Prompt Definitions

**Story**: SCRUM-5 - Cursor MCP Server for ICAET Query Access  
**Task**: 04 - MCP Prompt Definitions

---

## 1. Issue

Create three informative MCP prompts that help users understand ICAET, provide example queries, and guide effective question formatting.

---

## 2. Solution

Implement three prompt constants in `prompts.py` with actual helpful content (not stubs). Each prompt will be a multi-line string with clear, user-friendly guidance. Structure prompts for fastmcp framework consumption using a list of prompt dictionaries with name, description, and content fields.

---

## 3. Implementation Steps

1. Implement `src/icsaet_mcp/prompts.py`:
   - Add module docstring explaining prompt purpose
   - Import `typing.TypedDict` for type hints

2. Create `ICAET_OVERVIEW` prompt content:
   ```
   Name: "icaet_overview"
   Description: "Learn what ICAET is and how to use it"
   Content: 3-5 paragraphs explaining:
   - ICAET is a knowledge base of conference talks, speakers, and topics
   - Contains information from software engineering/architecture conference sessions
   - Query it using natural language questions
   - Get answers about speakers, talk content, themes, and session details
   - Use from Cursor via the query tool
   ```

3. Create `EXAMPLE_QUESTIONS` prompt content:
   ```
   Name: "example_questions"
   Description: "Sample questions to ask ICAET"
   Content: 6-8 diverse example questions:
   - "What did Leslie Miley talk about?"
   - "What sessions covered microservices?"
   - "Who spoke about platform engineering?"
   - "What were the main themes of the conference?"
   - "Which talks discussed AI and machine learning?"
   - "What advice was given about team leadership?"
   - "What stories were shared about scaling systems?"
   ```

4. Create `FORMATTING_GUIDANCE` prompt content:
   ```
   Name: "formatting_guidance"
   Description: "Tips for better ICAET questions"
   Content: 5-7 best practices:
   - Be specific: mention speaker names, topics, or sessions
   - Ask one question at a time for clearer answers
   - Use natural language - no special syntax needed
   - Reference specific talks when you know them
   - Ask about themes, patterns, or comparisons across talks
   - Start broad, then narrow down with follow-up questions
   - Good: "What did X talk about?" vs Bad: "Tell me everything"
   ```

5. Create `PROMPTS` list for fastmcp registration:
   ```python
   PROMPTS = [
       {"name": "icaet_overview", "description": "...", "content": ICAET_OVERVIEW},
       {"name": "example_questions", "description": "...", "content": EXAMPLE_QUESTIONS},
       {"name": "formatting_guidance", "description": "...", "content": FORMATTING_GUIDANCE},
   ]
   ```

6. Run `ruff check src/icsaet_mcp/prompts.py` and `black src/icsaet_mcp/prompts.py`

---

## 4. Verification

- [ ] Three prompts defined with complete, helpful content
- [ ] Each prompt has name, description, and content
- [ ] `PROMPTS` list exports all three for server registration
- [ ] Content is professional, clear, and user-friendly
- [ ] No placeholder text or TODOs in content
- [ ] No technical jargon about MCP protocol
- [ ] `ruff check` passes
- [ ] Manual review confirms content quality and usefulness

