reasoning_1 = """
You are an AI assistant whose goal is to generate reasoning as to why a particular web action was taken. You are given:
1. CONTEXT: An instruction stating the overall goal you need to achieve
2. CURRENT BROWSER CONTENT: A simplified text description of the current browser content, without formatting elements.
3. CURRENT URL: The current webpage URL
4. PREVIOUS ACTIONS: A list of your past actions.
5. YOUR ACTION: The current action that you took

Provide reasoning (after REASONING:) for why the current action (YOUR ACTION:) was taken.

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
YOUR ACTION:
TYPE 26 Depart Press DOWN ARROW key to select available dates "12/03/2023"
REASONING:
I have no previous actions.
I have to first type "12/03/2023" in the field Depart which corresponds to input id 26
==================================================

Example 2:
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
YOUR ACTION:
CLICK 22 Seattle
REASONING:
I have already typed in "Seattle" in id 21
I should next check if there is a dropdown text below id 21
Yes, there is a corresponding dropdown text "Seattle" in id 22
I have to click on id 22 
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
YOUR ACTION: {current_action}
REASONING:
"""

#### test time example ###
# CONTEXT:
# CHOOSE_DATE datepicker "11/03/2016"
# ------------------
# CURRENT BROWSER CONTENT:
# <div id=8 val= />
# <a id=9 val= />
# <span id=10 val=Prev />
# <a id=11 val= />
# <div id=13 val= />
# <span id=14 val=December />
# <span id=15 val=2016 />
# <a id=40 val=12/1/2016 />
# <a id=42 val=12/2/2016 />
# <a id=44 val=12/3/2016 />
# <a id=47 val=12/4/2016 />
# <a id=49 val=12/5/2016 />
# <a id=51 val=12/6/2016 />
# <a id=53 val=12/7/2016 />
# <a id=55 val=12/8/2016 />
# <a id=57 val=12/9/2016 />
# <a id=59 val=12/10/2016 />
# <a id=62 val=12/11/2016 />
# <a id=64 val=12/12/2016 />
# <a id=66 val=12/13/2016 />
# <a id=68 val=12/14/2016 />
# ------------------
# CURRENT URL:
# https://
# ------------------
# PREVIOUS ACTIONS:
# CLICK 5 datepicker
# ------------------
# YOUR ACTION: CLICK 10 Prev
# REASONING:

# CONTEXT:
# FIND_AND_CLICK_TAB_LINK "aliquet"
# ------------------
# CURRENT BROWSER CONTENT:
# <ul id=4 val= />
# <li id=5 val= />
# <a id=6 val=Tab #1 />
# <li id=7 val= />
# <a id=8 val=Tab #2 />
# <li id=9 val= />
# <a id=10 val=Tab #3 />
# <div id=11 val=tabs-1 />
# <p id=12 val= />
# <t id=-1 val=Donec />
# <span id=13 val=ridiculus />
# <span id=14 val=eget />
# <t id=-2 val=rhoncus, pellentesque />
# <span id=15 val=malesuada />
# <t id=-3 val=non, donec />
# <t id=-4 val=morbi. Nunc id auctor. />
# <span id=16 val=Eget />
# <t id=-5 val=tortor, />
# <span id=17 val=pretium />
# <t id=-6 val=neque dui />
# <t id=-7 val=feugiat lacus. At. />
# ------------------
# CURRENT URL:
# https://
# ------------------
# PREVIOUS ACTIONS:
# ------------------
# REASONING:
# I have no previous actions.
# I am currently in tab-1.
# Looking at the browser content, I can see all the links corresponding to <span id> elements as ridiculus, eget, malesuada, Eget, pretium.
# None of these links match aliquet.
# Since I am at tab-1, I will go to tab-2. 
# To go to tab-2, I must click on id 8. 
# YOUR ACTION:
# CLICK 8

reasoning_2 = """
You are an AI assistant whose goal is to generate reasoning as to why a particular web action was taken. You are given:
1. CONTEXT: An instruction stating the overall goal you need to achieve
2. CURRENT BROWSER CONTENT: A simplified text description of the current browser content, without formatting elements.
3. CURRENT URL: The current webpage URL
4. PREVIOUS ACTIONS: A list of your past actions.
5. CURRENT ACTION: The current action that you took

Provide reasoning (after REASONING:) that justifies the action you took (YOUR ACTION:) 

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
==================================================

Example 2:
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

==================================================
CONTEXT:
CHOOSE_DATE datepicker "11/03/2016"
------------------
CURRENT BROWSER CONTENT:
<div id=8 val= />
<a id=9 val= />
<span id=10 val=Prev />
<a id=11 val= />
<div id=13 val= />
<span id=14 val=December />
<span id=15 val=2016 />
<a id=40 val=12/1/2016 />
<a id=42 val=12/2/2016 />
<a id=44 val=12/3/2016 />
<a id=47 val=12/4/2016 />
<a id=49 val=12/5/2016 />
<a id=51 val=12/6/2016 />
<a id=53 val=12/7/2016 />
<a id=55 val=12/8/2016 />
<a id=57 val=12/9/2016 />
<a id=59 val=12/10/2016 />
<a id=62 val=12/11/2016 />
<a id=64 val=12/12/2016 />
<a id=66 val=12/13/2016 />
<a id=68 val=12/14/2016 />
------------------
CURRENT URL:
https://
------------------
PREVIOUS ACTIONS:
CLICK 5 datepicker
------------------
REASONING:
"""