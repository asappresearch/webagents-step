conversation_generator = """

Your goal is to take as input a flight booking query, and generate a short conversation between a customer and an agent that conveys the same information. Make sure to include any relevant details. Please follow these instructions:
1. Make sure the conversation is short (at most 2-3 exchanges)
2. Try to vary the order in which information is presented, for example providing the return date later on
3. Make sure to not alter any detail
4. Whenever you mention the date, always mention the year 2023.
5. Try to vary the conversation as much as possible

Here are some examples:

==================================================
INPUT:
Book a flight from Boston to Chicago departing on Dec 1, 2023 and returning on Dec 12, 2023
------------------
OUTPUT:
CUS: Hi, I want to book a flight from Boston to Chicago. I want to leave on Dec 1, 2023. 
REP: Sure, I can help you! Is this a roundtrip?
CUS: Yes, I would like to return on Dec 12, 2023
==================================================

The current context, browser content, action, previous label are below. Reply with your current label.

==================================================
INPUT:
{input}
------------------
OUTPUT:
"""