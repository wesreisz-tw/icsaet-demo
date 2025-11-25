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

__all__ = ["ICAET_OVERVIEW", "EXAMPLE_QUESTIONS", "FORMATTING_GUIDANCE"]
