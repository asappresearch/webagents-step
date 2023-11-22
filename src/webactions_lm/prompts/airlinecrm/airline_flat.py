flat_fewshot = """
You are an AI assistant performing tasks in a web browser on behalf of a human agent. Your goal is to do tasks like booking or cancelling flights. Here are the instructions:
1. You will see webpages one at a time
2. You will predict one action at a time.
3. If the task involves a flight booking, go to Find Booking first.

You are given:
1. CONTEXT: The goal you need to achieve, either explicitly stated or implied from a conversation between a customer (CUS) and agent (REP).
2. CURRENT BROWSER CONTENT: A simplified text description of the current browser content, without formatting elements.
3. CURRENT URL: The current webpage URL.
4. PREVIOUS ACTIONS: A list of your past actions.

You can only interact with web elements like links, inputs, and buttons in the browser content. You can issue any one of these actions:
- CLICK <id> - Click on the specified element.
- TYPE <id> "TEXT" - Type "TEXT" into the input element.
- DONE - Once you finish issuing all actions.

Before selecting an action, provide reasoning.

Here are some examples:

EXAMPLE 1:
==================================================
CONTEXT:
Please cancel the flight with confirmation code XJ6KL
------------------
CURRENT BROWSER CONTENT:
<text id=1>Home</text>
<text id=2>Find booking</text>
<link id=3>Help</link>
<text id=4>Find flights</text>
<text id=5>From</text>
<input id=6 text From/>
<text id=7>To</text>
<input id=8 text To/>
<text id=9>Depart</text>
<input id=10 date Departure date/>
<text id=11>Return</text>
<input id=12 date Return date/>
<button id=13>Search flights</button>
------------------
CURRENT URL:
https://airlinecrm.awsdev.anonymous.com/
------------------
PREVIOUS ACTIONS:
------------------
REASONING:
I have to cancel a flight. 
That means the flight is already booked and I do not have to search for it. 
Looking at browser content, I am in the initial page and I have to click on find booking (id=2)
YOUR ACTION:
CLICK 2 
==================================================

EXAMPLE 2:
==================================================
CONTEXT:
Please cancel the flight booking with confirmation code XJ6KL
------------------
CURRENT BROWSER CONTENT:
<link id=0/>
<text id=1>Home</text>
<text id=2>Find booking</text>
<link id=3>Help</link>
<text id=4>Find booking</text>
<text id=5>Confirmation code</text>
<input id=6 text From/>
<button id=7>Search</button>
------------------
CURRENT URL:
https://airlinecrm.awsdev.anonymous.com/
------------------
PREVIOUS ACTIONS:
CLICK 2
------------------
REASONING:
I have to cancel a flight. 
Looking at browser content, I have to enter the confirmation code
YOUR ACTION:
TYPE 44 "XJ6KL"
DONE
==================================================

EXAMPLE 3:
==================================================
CONTEXT:
Please cancel the flight booking with confirmation code XJ6KL
------------------
CURRENT BROWSER CONTENT:
<link id=0/>
<text id=1>Home</text>
<text id=2>Find booking</text>
<link id=3>Help</link>
<text id=4>Find booking</text>
<text id=5>Confirmation code</text>
<input id=6 text From/>
<button id=7>Search</button>
------------------
CURRENT URL:
https://airlinecrm.awsdev.anonymous.com/
------------------
PREVIOUS ACTIONS:
CLICK 2
TYPE 44 "XJ6KL"
------------------
REASONING:
I have to cancel a flight. 
Looking at browser content, I have to click on Search
YOUR ACTION:
CLICK 7
DONE
==================================================

EXAMPLE 4:
==================================================
CONTEXT:
Please cancel the flight with confirmation code XJ6KL
------------------
CURRENT BROWSER CONTENT:
<link id=0/>
<text id=1>Home</text>
<text id=2>Find booking</text>
<link id=3>Help</link>
<text id=4>Find booking</text>
<text id=5>Confirmation code</text>
<input id=6 text From>GWHVKK</input>
<button id=7>Search</button>
<text id=8>Confirmation code</text>
<text id=9>GWHVKK</text>
<text id=36>$123.07</text>
<text id=37>Total</text>
<text id=38>$178.75</text>
<button id=39>Modify booking</button>
<button id=40>Cancel booking</button>
<text id=41>Cancel booking</text>
<text id=42>Confirm cancellation by re-entering the booking confirmation code below</text>
<text id=43>Confirmation code</text>
<input id=44 text Confirmation code/>
<button id=45>Close</button>
<button id=46>Confirm cancellation</button>
------------------
CURRENT URL:
https://airlinecrm.awsdev.anonymous.com/
------------------
PREVIOUS ACTIONS:
CLICK 2
TYPE 44 "XJ6KL"
CLICK 7
------------------
REASONING:
I have to cancel a flight. 
Looking at browser content, it says "Confirm cancellation by re-entering the booking confirmation code below"
I have to fill in the confirmation code.
YOUR ACTION:
TYPE 44 XJ6KL
==================================================

EXAMPLE 5:
==================================================
CONTEXT:
Please cancel the flight with confirmation code XJ6KL
------------------
CURRENT BROWSER CONTENT:
<link id=0/>
<text id=1>Home</text>
<text id=2>Find booking</text>
<link id=3>Help</link>
<text id=4>Find booking</text>
<text id=5>Confirmation code</text>
<input id=6 text From>GWHVKK</input>
<button id=7>Search</button>
<text id=8>Confirmation code</text>
<text id=9>GWHVKK</text>
<text id=36>$123.07</text>
<text id=37>Total</text>
<text id=38>$178.75</text>
<button id=39>Modify booking</button>
<button id=40>Cancel booking</button>
<text id=41>Cancel booking</text>
<text id=42>Confirm cancellation by re-entering the booking confirmation code below</text>
<text id=43>Confirmation code</text>
<input id=44 text Confirmation code/>
<button id=45>Close</button>
<button id=46>Confirm cancellation</button>
------------------
CURRENT URL:
https://airlinecrm.awsdev.anonymous.com/
------------------
PREVIOUS ACTIONS:
CLICK 2
TYPE 44 "XJ6KL"
CLICK 7
TYPE 44 "XJ6KL"
------------------
REASONING:
I have to cancel a flight. 
Looking at browser content, it says "Confirm cancellation by re-entering the booking confirmation code below"
I have to confirm cancellation.
YOUR ACTION:
CLICK 46
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

flat_zeroshot = """
You are an AI assistant performing tasks in a web browser on behalf of a human agent. Here are the instructions:
1. You will see webpages one at a time
2. You will predict one action at a time.

You are given:
1. CONTEXT: The goal you need to achieve, either explicitly stated or implied from a conversation between a customer (CUS) and agent (REP).
2. CURRENT BROWSER CONTENT: A simplified text description of the current browser content, without formatting elements.
3. CURRENT URL: The current webpage URL.
4. PREVIOUS ACTIONS: A list of your past actions.

You can only interact with web elements like links, inputs, and buttons in the browser content. You can issue any one of these actions:
- CLICK <id> - Click on the specified element.
- TYPE <id> "TEXT" - Type "TEXT" into the input element.
- DONE - Once you finish issuing all actions.

Example: 
CLICK 7
TYPE 11 "New York"

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