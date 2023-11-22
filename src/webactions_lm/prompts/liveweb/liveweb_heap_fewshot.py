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

Here are some examples:

EXAMPLE 1:
==================================================
CONTEXT:
CUS: I would like to book a flight from NYC to Boston leaving Dec 3 2023
REP: Sure, I can help you! Is this for a roundtrip?
CUS: Yes I would like to return after a week
------------------
CURRENT BROWSER CONTENT:
<button id=18 title="Travelers">1 Adult</button>
<text id=19>Use TrueBlue points</text>
<text id=20>From</text>
<input id=21 text>Syracuse, NY (SYR)</input>
<button id=22>Reverse origin and destination city or airport</button>
<text id=23>To</text>
<input id=24 text/>
<text id=25>Depart</text>
<input id=26 Depart Press DOWN ARROW key to select available dates/>
<text id=27>Return</text>
<input id=28 Return Press DOWN ARROW key to select available dates/>
<button id=29>Search flights</button>
------------------
CURRENT URL:
https://www.jetblue.com/
------------------
PREVIOUS ACTIONS:
------------------
YOUR ACTION:
FILL_TEXT From "NYC"
FILL_TEXT To "BOSTON"
CHOOSE_DATE Depart "12/03/2023"
CHOOSE_DATE Return "12/10/2023"
CLICK Search
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

Here are some examples:

EXAMPLE 1:
==================================================
CONTEXT:
CLICK Search
------------------
CURRENT BROWSER CONTENT:
<button id=18 title="Travelers">1 Adult</button>
<text id=19>Use TrueBlue points</text>
<text id=20>From</text>
<input id=21 text>Syracuse, NY (SYR)</input>
<button id=22>Reverse origin and destination city or airport</button>
<text id=23>To</text>
<input id=24 text/>
<text id=25>Depart</text>
<input id=26 Depart Press DOWN ARROW key to select available dates/>
<text id=27>Return</text>
<input id=28 Return Press DOWN ARROW key to select available dates/>
<button id=29>Search flights</button>
------------------
CURRENT URL:
https://www.jetblue.com/
------------------
PREVIOUS ACTIONS:
------------------
YOUR ACTION:
CLICK 29 Search flights
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

Here are some examples:

EXAMPLE 1:
==================================================
CONTEXT:
FILL_TEXT From "Seattle"
------------------
CURRENT BROWSER CONTENT:
<button id=16>Stays</button>
<button id=17>Roundtrip</button>
<button id=18 title="Travelers">1 Adult</button>
<text id=19>Use TrueBlue points</text>
<text id=20>From</text>
<input id=21 text></input>
<button id=22>Reverse origin and destination city or airport</button>
<text id=23>To</text>
<input id=24 text/>
<text id=25>Depart</text>
<input id=26 Depart Press DOWN ARROW key to select available dates/>
<text id=27>Return</text>
<input id=28 Return Press DOWN ARROW key to select available dates/>
------------------
CURRENT URL:
https://www.jetblue.com/
------------------
PREVIOUS ACTIONS:
------------------
REASONING:
I have no previous actions.
I have to first type "Seattle" in the field From which corresponds to input id 21
YOUR ACTION:
TYPE 21 "Seattle"
==================================================

EXAMPLE 2:
==================================================
CONTEXT:
FILL_TEXT From "Seattle"
------------------
<button id=16>Stays</button>
<button id=17>Roundtrip</button>
<button id=18 title="Travelers">1 Adult</button>
<text id=19>Use TrueBlue points</text>
<text id=20>From</text>
<input id=21 text>Seattle</input>
<text id=22>Seattle</text>
<text id=23>, WA (SEA)</text>
<text id=24>Seattle</text>
<text id=25>/King Country, WA (BFI)</text>
<text id=26>Browse by regions</text>
<text id=27>Browse by regions</text>
<text id=28>Mint Service</text>
<text id=29>Partner Airline</text>
<button id=30>Reverse origin and destination city or airport</button>
------------------
CURRENT URL:
https://www.jetblue.com/
------------------
PREVIOUS ACTIONS:
TYPE 21 "Seattle"
------------------
REASONING:
I have already typed in "Seattle" in id 21
I should next check if there is a dropdown text below id 21
Yes, there is a corresponding dropdown text "Seattle" in id 22
I have to click on id 22 
YOUR ACTION:
CLICK 22 Seattle
==================================================

EXAMPLE 3:
==================================================
CONTEXT:
FILL_TEXT From "Seattle"
------------------
<button id=17>Roundtrip</button>
<button id=18 title="Travelers">1 Adult</button>
<text id=19>Use TrueBlue points</text>
<text id=20>From</text>
<input id=21 text>Seattle, WA (SEA)</input>
<button id=22>Reverse origin and destination city or airport</button>
<text id=23>To</text>
<input id=24 text/>
<text id=25>Browse by regions</text>
<text id=26>Mint Service</text>
<text id=27>Partner Airline</text>
<text id=28>Depart</text>
------------------
CURRENT URL:
https://www.jetblue.com/
------------------
PREVIOUS ACTIONS:
TYPE 21 "Seattle"
CLICK 22 Seattle
------------------
REASONING:
I have already typed in "Seattle" in id 21
I have clicked on the dropdown text in id 22 Seattle
I am done filling text
YOUR ACTION:
DONE
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

Here are some examples:

Example 1:
==================================================
CONTEXT:
CHOOSE_DATE Depart "12/03/2023"
------------------
CURRENT BROWSER CONTENT:
<button id=18 title="Travelers">1 Adult</button>
<text id=19>Use TrueBlue points</text>
<text id=20>From</text>
<input id=21 text>New York City area (NYC)</input>
<button id=22>Reverse origin and destination city or airport</button>
<text id=23>To</text>
<input id=24 text>Boston area</input>
<text id=25>Depart</text>
<input id=26 Depart Press DOWN ARROW key to select available dates/>
<text id=27>Return</text>
<input id=28 Return Press DOWN ARROW key to select available dates/>
<button id=29 aria-label="Previous Month"/>
<text id=30>April 2023</text>
<text id=31>S</text>
<text id=32>M</text>
<text id=33>T</text>
<text id=34>W</text>
<text id=35>T</text>
<text id=36>F</text>
<text id=37>S</text>
<button id=38 aria-label="depart Saturday, April 1, 2023">1</button>
<button id=39 aria-label="depart Sunday, April 2, 2023">2</button>
<button id=40 aria-label="depart Monday, April 3, 2023">3</button>
<button id=41 aria-label="depart Tuesday, April 4, 2023">4</button>
<button id=42 aria-label="depart Wednesday, April 5, 2023">5</button>
<button id=63 aria-label="depart Wednesday, April 26, 2023">26</button>
<button id=64 aria-label="depart Thursday, April 27, 2023">27</button>
<button id=65 aria-label="depart Friday, April 28, 2023">28</button>
<button id=66 aria-label="depart Saturday, April 29, 2023">29</button>
<button id=67 aria-label="depart Sunday, April 30, 2023">30</button>
------------------
CURRENT URL:
https://www.jetblue.com/
------------------
PREVIOUS ACTIONS:
------------------
REASONING:
I have no previous actions.
I have to first type "12/03/2023" in the field Depart which corresponds to input id 26
YOUR ACTION:
TYPE 26 Depart Press DOWN ARROW key to select available dates "12/03/2023"
==================================================

Example 2:
==================================================
CONTEXT:
CHOOSE_DATE Depart "12/03/2023"
------------------
CURRENT BROWSER CONTENT:
<button id=18 title="Travelers">1 Adult</button>
<text id=19>Use TrueBlue points</text>
<text id=20>From</text>
<input id=21 text>New York City area (NYC)</input>
<button id=22>Reverse origin and destination city or airport</button>
<text id=23>To</text>
<input id=24 text>Boston area</input>
<text id=25>Depart</text>
<input id=26 Depart Press DOWN ARROW key to select available dates>Sun Dec 3</input>
<text id=27>Return</text>
------------------
CURRENT URL:
https://www.jetblue.com/
------------------
PREVIOUS ACTIONS:
TYPE 26 Depart Press DOWN ARROW key to select available dates "12/03/2023"
------------------
REASONING:
I have already typed in "12/03/2023" in id 26
I am done entering dates
YOUR ACTION:
DONE
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