# Task 04 Implementation Plan: MCP Prompt Definitions

**Story**: SCRUM-5  
**Task ID**: Task 04  
**Created**: 2025-11-25

---

## 1. Issue

Need to create three informative MCP prompts in `prompts.py` that help users understand ICAET, provide example queries, and guide them in formatting questions effectively for the knowledge base.

---

## 2. Solution

Implement three prompt definitions as string constants in `prompts.py` with descriptive content that will be registered with the fastmcp framework. Each prompt will be self-contained and provide actionable guidance to users within Cursor.

**Technical Rationale**:
- Use simple string constants for static prompts (no dynamic content needed)
- Follow fastmcp prompt structure for easy registration
- Keep content concise (users read prompts in Cursor UI)
- Focus on user value, not technical implementation details
- Use markdown formatting for better readability

---

## 3. Implementation Steps

### Step 1: Create ICAET Overview Prompt
**File**: `/Users/wesleyreisz/work/mcp/icsaet-demo/src/icsaet_mcp/prompts.py`
- Replace entire file content with:
  ```python
  """MCP prompt definitions for ICAET context."""

  ICAET_OVERVIEW = """# ICAET Knowledge Base

  ICAET (International Conference on Advanced Engineering and Technology) is a comprehensive conference knowledge base containing information about:

  - **Talks and Sessions**: Detailed content from conference presentations
  - **Speakers**: Information about presenters and their expertise
  - **Topics**: Technical themes and subject areas covered
  - **Key Insights**: Main takeaways and important points from sessions

  ## Using ICAET from Cursor

  You can query this knowledge base by asking natural language questions about any aspect of the conference. The system will search through all conference content and provide relevant answers based on the actual talks, speakers, and topics.

  This is a query interface to conference content - ask about specific speakers, topics, sessions, or general themes to explore what was covered at ICAET.
  """
  ```

### Step 2: Add Example Questions Prompt
**File**: `/Users/wesleyreisz/work/mcp/icsaet-demo/src/icsaet_mcp/prompts.py`
- After `ICAET_OVERVIEW`, add:
  ```python

  EXAMPLE_QUESTIONS = """# Example Questions for ICAET

  Here are diverse examples of questions you can ask:

  ## Speaker-Focused Questions
  - "What did Leslie Miley talk about?"
  - "What topics did [Speaker Name] cover in their session?"
  - "Who presented on software architecture?"

  ## Topic-Focused Questions
  - "What sessions covered machine learning?"
  - "What was discussed about cloud computing?"
  - "Tell me about DevOps practices presented at the conference"

  ## General Conference Questions
  - "What were the main themes of the conference?"
  - "What emerging technologies were discussed?"
  - "What sessions focused on leadership and management?"

  ## Specific Session Questions
  - "What were the key takeaways from the keynote?"
  - "What examples were given in the microservices talk?"
  - "What best practices were recommended for API design?"

  Feel free to ask follow-up questions to dive deeper into any topic!
  """
  ```

### Step 3: Add Question Formatting Prompt
**File**: `/Users/wesleyreisz/work/mcp/icsaet-demo/src/icsaet_mcp/prompts.py`
- After `EXAMPLE_QUESTIONS`, add:
  ```python

  FORMATTING_GUIDANCE = """# Tips for Better ICAET Questions

  ## Do's ✓
  - **Be specific**: Mention speaker names, topics, or session types when you know them
  - **Ask one thing at a time**: Focus on a single question for clearer answers
  - **Use natural language**: Write questions as you would ask a colleague
  - **Reference context**: If asking follow-ups, mention what you're building on
  - **Ask for details**: Request examples, best practices, or specific insights

  ## Don'ts ✗
  - Avoid overly broad questions like "Tell me everything"
  - Don't combine multiple unrelated questions in one query
  - Skip technical jargon about the query system itself

  ## Examples of Well-Formed Questions
  - ✓ "What did Leslie Miley say about inclusive engineering practices?"
  - ✓ "What examples were given for microservices patterns?"
  - ✓ "Who spoke about API security best practices?"

  ## Getting Better Results
  The more specific your question, the more targeted the answer. If you get a broad response, try narrowing your question to a specific speaker, topic, or aspect you're interested in.
  """
  ```

### Step 4: Add Module-Level Exports
**File**: `/Users/wesleyreisz/work/mcp/icsaet-demo/src/icsaet_mcp/prompts.py`
- At the end of file, add:
  ```python

  __all__ = ["ICAET_OVERVIEW", "EXAMPLE_QUESTIONS", "FORMATTING_GUIDANCE"]
  ```

### Step 5: Verify File Structure
**File**: `/Users/wesleyreisz/work/mcp/icsaet-demo/src/icsaet_mcp/prompts.py`
- Confirm file contains:
  - Module docstring at top
  - Three prompt constants (ICAET_OVERVIEW, EXAMPLE_QUESTIONS, FORMATTING_GUIDANCE)
  - __all__ export list
  - No placeholder or TODO comments

### Step 6: Run Linter Check
**Command**: `ruff check src/icsaet_mcp/prompts.py`
**Working Directory**: `/Users/wesleyreisz/work/mcp/icsaet-demo/`
**Expected**: Zero errors reported

### Step 7: Run Formatter Check
**Command**: `black --check src/icsaet_mcp/prompts.py`
**Working Directory**: `/Users/wesleyreisz/work/mcp/icsaet-demo/`
**Expected**: No changes needed

### Step 8: Run Type Check
**Command**: `mypy src/icsaet_mcp/prompts.py`
**Working Directory**: `/Users/wesleyreisz/work/mcp/icsaet-demo/`
**Expected**: Zero type errors (constants are automatically typed as str)

### Step 9: Verify Import
**Command**: `python -c "from icsaet_mcp.prompts import ICAET_OVERVIEW, EXAMPLE_QUESTIONS, FORMATTING_GUIDANCE; print('Success')"`
**Working Directory**: `/Users/wesleyreisz/work/mcp/icsaet-demo/`
**Expected**: Prints "Success" without errors

### Step 10: Verify Content Length
**Command**: `python -c "from icsaet_mcp.prompts import *; print(f'Overview: {len(ICAET_OVERVIEW)} chars'); print(f'Examples: {len(EXAMPLE_QUESTIONS)} chars'); print(f'Formatting: {len(FORMATTING_GUIDANCE)} chars')"`
**Working Directory**: `/Users/wesleyreisz/work/mcp/icsaet-demo/`
**Expected**: Each prompt is between 300-1500 characters (concise but informative)

---

## 4. Verification

### Content Quality
- Each prompt is 3-7 paragraphs of actionable content
- Professional but friendly tone throughout
- No technical jargon about MCP or implementation
- Focused on user value and guidance
- Encouraging users to explore the knowledge base

### Prompt Structure
- ICAET_OVERVIEW explains what ICAET is and how to use it
- EXAMPLE_QUESTIONS provides 8+ diverse example queries
- FORMATTING_GUIDANCE provides 5-7 tips for better questions
- Each prompt uses markdown formatting for readability
- All prompts are complete (no placeholders or TODOs)

### Code Quality
- Module docstring present
- Three string constants defined
- __all__ export list included
- ruff reports zero errors
- black reports no formatting changes needed
- mypy reports zero type errors
- Can import all three prompts successfully

### Integration Readiness
- Prompts are structured as simple string constants
- Ready for fastmcp prompt registration in Task 06
- Content is final and production-ready
- No dynamic content or parameters needed

---

## IMPLEMENTATION CHECKLIST

:white_check_mark: 1. Replace prompts.py content with module docstring
:white_check_mark: 2. Add ICAET_OVERVIEW prompt constant with 3-5 paragraphs explaining ICAET
:white_check_mark: 3. Add EXAMPLE_QUESTIONS prompt constant with 8+ diverse example queries
:white_check_mark: 4. Add FORMATTING_GUIDANCE prompt constant with 5-7 tips for better questions
:white_check_mark: 5. Add __all__ export list with all three prompt names
:white_check_mark: 6. Run `ruff check` and verify zero errors
:white_check_mark: 7. Run `black --check` and verify no changes needed
:white_check_mark: 8. Run `mypy` and verify zero type errors
:white_check_mark: 9. Verify all three prompts can be imported successfully
:white_check_mark: 10. Verify each prompt is concise (300-1500 characters)
:white_check_mark: 11. Verify no placeholder text or TODO comments remain
:white_check_mark: 12. Verify professional but friendly tone throughout


