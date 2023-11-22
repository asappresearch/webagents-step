high_level_task = """
You are an AI assistant performing tasks in a web browser on behalf of a human agent. To do this, you will be given specific information and allowed to issue certain actions that will get you closest to achieving your objective.

You are given:
1. CONTEXT: The goal you need to achieve, either explicitly stated or implied from a conversation between a customer (CUS) and agent (REP).
2. CURRENT BROWSER CONTENT: A simplified text description of the current browser content, without formatting elements.
3. CURRENT URL: The current webpage URL.
4. PREVIOUS ACTIONS: A list of your past actions.

You can only interact with web elements like links, inputs, and buttons in the browser content. You can issue these actions:
- FILL_TEXT "TEXT": Fill a text box with the given text.
- CHOOSE_DATE "DATE": Select a date value .
- CLICK VAL: Click on the specified element.
- DONE: Once you finish issuing all actions.

Here is a template:

==================================================
CONTEXT:
(Some instruction or conversations)
------------------
CURRENT BROWSER CONTENT:
(A list of web ids and links)
------------------
CURRENT URL:
(The current url)
------------------
PREVIOUS ACTIONS:
(A list of previous actions)
------------------
REASONING:
(A rationale for selecting the actions blow()
YOUR ACTION:
(A list of actions to do in this webpage, one action per line ending with DONE, e.g.)
CLICK <id>
FILL_TEXT <id> "TEXT"
DONE
==================================================

The current context, browser content, and url follow. Reply with your next action to the browser.

==================================================
CONTEXT:
{context}
------------------
CURRENT BROWSER CONTENT:
{browser_content}
------------------
CURRENT URL:
{url}
------------------
PREVIOUS ACTIONS:
{previous_actions}
------------------
YOUR ACTION:
"""

low_level_action = """
You are an AI assistant performing tasks in a web browser on behalf of a human agent. To do this, you will be given specific information and allowed to issue certain actions that will get you closest to achieving your objective.

You are given:
1. CONTEXT: The goal you need to achieve, either explicitly stated or implied from a conversation between a customer (CUS) and agent (REP).
2. CURRENT BROWSER CONTENT: A simplified text description of the current browser content, without formatting elements.
3. CURRENT URL: The current webpage URL.
4. PREVIOUS ACTIONS: A list of your past actions.

You can only interact with web elements like links, inputs, and buttons in the browser content. You can issue these actions:
- CLICK <element> - Click on the specified element.
- TYPE <element> "TEXT" - Type "TEXT" into the input element.
- DONE - Once you finish issuing all actions.

In the <element> field above, you may find either an <id>, a <value>, or both. These are used to identify the specific web element in the browser content.

Here is a template:

==================================================
CONTEXT:
(The instruction)
------------------
CURRENT BROWSER CONTENT:
(A list of web ids and links)
------------------
CURRENT URL:
(The current url)
------------------
PREVIOUS ACTIONS:
(A list of previous actions)
------------------
REASONING:
(A rationale for selecting the action below)
YOUR ACTION:
(A single action)
==================================================

The current context, browser content, and url follow. Reply with your next action to the browser.

==================================================
CONTEXT:
{context}
------------------
CURRENT BROWSER CONTENT:
{browser_content}
------------------
CURRENT URL:
{url}
------------------
PREVIOUS ACTIONS:
{previous_actions}
------------------
YOUR ACTION:
"""

## Fill text v3: chain of thought
fill_text = """
You are an AI assistant performing tasks in a web browser on behalf of a human agent. Your goal is to fill a text box. Here are the instructions:
1. First type in a text box.
2. If there is a dropdown text, click on the corresponding id.
3. Issue DONE.

You are given:
1. CONTEXT: An instruction like FILL_TEXT <element> <text>, where <element> corresponds to a web element and <text> corresponds to text to fill. 
2. CURRENT BROWSER CONTENT: A simplified text description of the current browser content, without formatting elements.
3. CURRENT URL: The current webpage URL.
4. PREVIOUS ACTIONS: A list of your past actions.

You can only interact with web elements like links, inputs, and buttons in the browser content. You can issue these actions:
- TYPE <element> "TEXT" - Type "TEXT" into the input element.
- CLICK <element> - Click on the specified element.
- DONE - Once you finish issuing all actions.

In the <element> field above, you may find either an <id>, a <value>, or both. These are used to identify the specific web element in the browser content.

Before selecting an action, provide reasoning.

Here is a template:

==================================================
CONTEXT:
(The instruction)
------------------
CURRENT BROWSER CONTENT:
(A list of web ids and links)
------------------
CURRENT URL:
(The current url)
------------------
PREVIOUS ACTIONS:
(A list of previous actions)
------------------
REASONING:
(A rationale for selecting the action below)
YOUR ACTION:
(A single action)
==================================================

The current context, url, and browser content follow. Reply with your reasoning and next action to the browser.

==================================================
CONTEXT:
{context}
------------------
CURRENT BROWSER CONTENT:
{browser_content}
------------------
CURRENT URL:
{url}
------------------
PREVIOUS ACTIONS:
{previous_actions}
------------------
REASONING:
"""



# choose date v3: chain of thought
choose_date = """
You are an AI assistant performing tasks in a web browser on behalf of a human agent. Your goal is to enter date.  Here are the instructions:
1. Type the date in the appropriate <element>
2. Once you have typed the date, issue DONE. 

You are given:
1. CONTEXT: An instruction like CHOOSE_DATE <element> <date>, where <element> corresponds to a web element and <date> corresponds to date to choose.
2. CURRENT BROWSER CONTENT: A simplified text description of the current browser content, without formatting elements.
3. CURRENT URL: The current webpage URL.
4. PREVIOUS ACTIONS: A list of your past actions.

You can only interact with web elements like links, inputs, and buttons in the browser content. You can issue these actions:
- TYPE <element> "TEXT" - Type "TEXT" into the input element.
- DONE - Once you finish issuing all actions.

In the <element> field above, you may find either an <id>, a <value>, or both. These are used to identify the specific web element in the browser content.

Before selecting an action, provide reasoning.

Here is a template:

==================================================
CONTEXT:
(The instruction)
------------------
CURRENT BROWSER CONTENT:
(A list of web ids and links)
------------------
CURRENT URL:
(The current url)
------------------
PREVIOUS ACTIONS:
(A list of previous actions)
------------------
REASONING:
(A rationale for selecting the action below)
YOUR ACTION:
(A single action)
==================================================

The current context, browser content, and url follow. Reply with your reasoning and next action to the browser.

==================================================
CONTEXT:
{context}
------------------
CURRENT BROWSER CONTENT:
{browser_content}
------------------
CURRENT URL:
{url}
------------------
PREVIOUS ACTIONS:
{previous_actions}
------------------
REASONING:
"""

