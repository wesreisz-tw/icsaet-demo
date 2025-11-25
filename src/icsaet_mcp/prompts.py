"""MCP prompt definitions for ICAET guidance.

Provides user-friendly prompts that help users understand ICAET,
discover example questions, and learn best practices for querying.
"""

from typing import TypedDict


class PromptDefinition(TypedDict):
    """Structure for MCP prompt definitions."""

    name: str
    description: str
    content: str


ICAET_OVERVIEW = """
# What is ICAET?

ICAET is a knowledge base containing content from software engineering and architecture conference sessions. It includes talks, speaker insights, and discussions from industry experts on topics ranging from system architecture to team leadership.

## What's Inside

The knowledge base contains:
- **Speaker presentations** - Detailed content from conference talks
- **Expert insights** - Advice and lessons learned from industry practitioners  
- **Technical topics** - Discussions on architecture, platforms, AI, DevOps, and more
- **Leadership wisdom** - Guidance on teams, culture, and growing as an engineer

## How to Use It

Simply ask questions in natural language. You can query about specific speakers, topics, or themes. The system will search the conference content and return relevant information.

Start with broad questions to explore, then ask follow-ups to dive deeper into specific areas that interest you.
"""

EXAMPLE_QUESTIONS = """
# Example Questions for ICAET

Here are some questions you can ask to explore the conference content:

## Speaker-Focused Questions
- "What did Leslie Miley talk about?"
- "What insights did Suhail Patel share about IC growth?"
- "Who spoke about platform engineering?"

## Topic-Focused Questions
- "What sessions covered microservices architecture?"
- "Which talks discussed AI and machine learning?"
- "What was said about building effective teams?"

## Theme and Pattern Questions
- "What were the main themes of the conference?"
- "What advice was given about scaling systems?"
- "What stories were shared about startup to scale-up journeys?"

## Track-Specific Questions
- "What topics were covered in the FinTech track?"
- "What health tech sessions were presented?"
- "What frontend and mobile trends were discussed?"
"""

FORMATTING_GUIDANCE = """
# Tips for Better ICAET Questions

Get more helpful answers by following these best practices:

## Do This

✓ **Be specific** - Mention speaker names, topics, or sessions when you know them
✓ **Ask one thing at a time** - Single-focus questions get clearer answers
✓ **Use natural language** - No special syntax needed, just ask normally
✓ **Start broad, then narrow** - Explore with general questions, then follow up
✓ **Ask about patterns** - "What themes emerged?" or "What advice was repeated?"

## Avoid This

✗ **Overly vague questions** - "Tell me everything" won't work well
✗ **Multiple questions in one** - Split them up for better results
✗ **Yes/no questions** - Open-ended questions reveal more insights

## Example Comparison

**Less effective:** "What happened at the conference?"
**More effective:** "What key insights were shared about building engineering teams?"

**Less effective:** "Tell me about talks"  
**More effective:** "What did speakers say about scaling microservices?"
"""

PROMPTS: list[PromptDefinition] = [
    {
        "name": "icaet_overview",
        "description": "Learn what ICAET is and how to use it",
        "content": ICAET_OVERVIEW.strip(),
    },
    {
        "name": "example_questions",
        "description": "Sample questions to ask ICAET",
        "content": EXAMPLE_QUESTIONS.strip(),
    },
    {
        "name": "formatting_guidance",
        "description": "Tips for writing better ICAET questions",
        "content": FORMATTING_GUIDANCE.strip(),
    },
]
