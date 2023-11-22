high_level_task = """
You are an AI assistant performing tasks in a web browser on behalf of a human agent. To do this, you will be given specific information and allowed to issue certain actions that will get you closest to achieving your objective.

You are given:
1. CONTEXT: The goal you need to achieve, either explicitly stated or implied from a conversation between a customer (CUS) and agent (REP).
2. CURRENT BROWSER CONTENT: A simplified text description of the current browser content, without formatting elements.
3. CURRENT URL: The current webpage URL.
4. PREVIOUS ACTIONS: A list of your past actions.

You can only interact with web elements like links, inputs, and buttons in the browser content. You can issue these actions:
- CLICK <element>: Click on the specified element.
- FILL_TEXT <element> "TEXT": Fill a text box with the given text.
- CHOOSE_DATE <element> "DATE": Select a date value from a datepicker.
- FIND_AND_CLICK_SEARCH_LINK "LINK_NUMBER": Find and click a link the LINK_NUMBER from search results.
- FIND_AND_CLICK_TAB_LINK "LINK": Find and click a link "LINK" by switching between tabs.
- DONE: Once you finish issuing all actions.

In the <element> field above, you may find either an <id>, a <value>, or both. These are used to identify the specific web element in the browser content.

Please stick to the following constraints:
1. When interacting with a datepicker, only use CHOOSE_DATE and not other actions.
2. When asked to find a link from search results, use FIND_SEARCH_LINK.
3. When asked to find a link by switching between tabs, directly use FIND_TAB_LINK without clicking on tabs.
4. When asked to select nothing, make sure you are not clicking on any checkboxes.

Here are some examples:

EXAMPLE 1:
==================================================
CONTEXT:
Find the 9th word in the paragraph, type that into the textbox and press "Submit".
<p id=4 val=Egestas lectus sit commodo turpis ultrices ut malesuada vestibulum />
<input_text id=5 val=answer-input />
<button id=6 val=Submit />
------------------
CURRENT URL:
https://
------------------
PREVIOUS ACTIONS:
------------------
YOUR ACTION:
TYPE 5 answer-input "vestibulum"
CLICK Submit
DONE
==================================================

EXAMPLE 2:
==================================================
CONTEXT:
Book the shortest one-way flight from: LEB to: RDG on 12/26/2016.
------------------
CURRENT BROWSER CONTENT:
<body id=1 val= />
<div id=2 val=wrap />
<div id=3 val=area />
<div id=4 val=menu />
<h2 id=5 val=Book Your One-Way Flight />
<div id=6 val= />
<input_text id=7 val=flight-from />
<div id=8 val= />
<input_text id=9 val=flight-to />
<div id=10 val= />
<div id=11 val=Departure Date />
<div id=12 val= />
<input_text id=13 val=datepicker />
<div id=14 val= />
<button id=15 val=Search />
<div id=16 val= />
<div id=23 val=1 result is available, use up and down arrow keys to navigate. />
<div id=18 val= />
<div id=27 val=1 result is available, use up and down arrow keys to navigate. />
------------------
CURRENT URL:
https://
------------------
PREVIOUS ACTIONS:
------------------
YOUR ACTION:
FILL_TEXT flight-from "LEB"
FILL_TEXT flight-to "RDG"
CHOOSE_DATE datepicker "12/26/2016"
CLICK Search
DONE
==================================================

EXAMPLE 3:
==================================================
CONTEXT:
Book the shortest one-way flight from: Cincinnati, OH to: LEX on 10/16/2016.
------------------
CURRENT BROWSER CONTENT:
<label id=362 val=Depart: />
<div id=364 val=2:50 PM />
<div id=365 val=Sun Oct 16 2016 />
<div id=366 val=Cincinnati, OH (CVG) />
<label id=369 val=Arrives: />
<div id=371 val=5:32 AM />
<div id=372 val=Mon Oct 17 2016 />
<div id=373 val=LEX />
<label id=376 val=Duration: />
<div id=378 val=14h 42m />
<button id=380 val=Book flight for $379 />
<div id=383 val= />
<label id=406 val=Depart: />
<div id=408 val=11:06 PM />
<div id=409 val=Sun Oct 16 2016 />
<div id=410 val=Cincinnati, OH (CVG) />
<label id=413 val=Arrives: />
<div id=415 val=2:27 AM />
<div id=416 val=Mon Oct 17 2016 />
<div id=417 val=LEX />
<label id=420 val=Duration: />
<div id=422 val=3h 21m />
<button id=424 val=Book flight for $209 />
<div id=425 val= />
<label id=428 val=Depart: />
<div id=430 val=3:23 AM />
<div id=431 val=Sun Oct 16 2016 />
<div id=432 val=Cincinnati, OH (CVG) />
<label id=435 val=Arrives: />
<div id=437 val=5:19 AM />
<div id=438 val=Mon Oct 17 2016 />
<div id=439 val=LEX />
<label id=442 val=Duration: />
<div id=444 val=25h 56m />
<button id=446 val=Book flight for $1197 />
------------------
CURRENT URL:
https://
------------------
PREVIOUS ACTIONS:
------------------
YOUR ACTION:
CLICK <button id=424 val=Book flight for $209 />
DONE
==================================================

The current context, url, and browser content follow. Reply with your next action to the browser.

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
You are an AI assistant performing tasks in a web browser on behalf of a human agent. Your goal is to done one action. Here are the instructions:
1. Do either a click or type action
2. Issue DONE.


You are given:
1. CONTEXT: The single action to perform
2. CURRENT BROWSER CONTENT: A simplified text description of the current browser content, without formatting elements.
3. CURRENT URL: The current webpage URL.
4. PREVIOUS ACTIONS: A list of your past actions.

You can only interact with web elements like links, inputs, and buttons in the browser content. You can issue these actions:
- CLICK <element> - Click on the specified element.
- TYPE <element> "TEXT" - Type "TEXT" into the input element.
- DONE - Once you finish issuing all actions.

In the <element> field above, you may find either an <id>, a <value>, or both. These are used to identify the specific web element in the browser content.

Please stick to the following constraints:
1. If the CONTEXT says CLICK, only issue CLICK
2. If the CONTEXT says TYPE, only issue TYPE
3. Issue DONE immediately after doing the action.

Here are some examples:

EXAMPLE 1:
==================================================
CONTEXT:
CLICK Search
------------------
CURRENT BROWSER CONTENT:
<input_text id=13 val=datepicker />
<div id=14 val= />
<button id=15 val=Search />
<div id=16 val= />
------------------
CURRENT URL:
https://
------------------
PREVIOUS ACTIONS:
------------------
YOUR ACTION:
CLICK 15 Search 
==================================================

EXAMPLE 2:
==================================================
CONTEXT:
CLICK Search
------------------
CURRENT BROWSER CONTENT:
<button id=577 val=Book flight for $220 />
------------------
CURRENT URL:
https://
------------------
PREVIOUS ACTIONS:
CLICK 15 Search 
------------------
YOUR ACTION:
DONE
==================================================

The current context, url, and browser content follow. Reply with your next action to the browser.

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

# Fill text prompt v3 with chain of thought
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

Here are some examples:

Example 1:
==================================================
CONTEXT:
FILL_TEXT 10 "Bowen"
------------------
CURRENT BROWSER CONTENT:
<body id=1 val= />
<div id=2 val=wrap />
<div id=3 val=area />
<div id=4 val=Movie Search />
<table id=5 val= />
<tbody id=6 val= />
<th id=8 val=Director />
<input_text id=10 val= />
<th id=12 val=Genre />
<input_text id=14 val= />
<th id=16 val=Year />
<input_text id=18 val= />
<div id=19 val=Submit />
------------------
CURRENT URL:
https://
------------------
PREVIOUS ACTIONS:
------------------
YOUR ACTION:
TYPE 10 "Bowen"
==================================================

Example 2:
==================================================
CONTEXT:
FILL_TEXT 10 "Bowen"
------------------
CURRENT BROWSER CONTENT:
<body id=1 val= />
<div id=2 val=wrap />
<div id=3 val=area />
<div id=4 val=Movie Search />
<table id=5 val= />
<tbody id=6 val= />
<th id=8 val=Director />
<input_text id=10 val= Bowen/>
<th id=12 val=Genre />
<input_text id=14 val= />
<th id=16 val=Year />
<input_text id=18 val= />
<div id=19 val=Submit />
------------------
CURRENT URL:
https://
------------------
PREVIOUS ACTIONS:
TYPE 10 "Bowen"
------------------
YOUR ACTION:
DONE
==================================================

Example 3:
==================================================
CONTEXT:
FILL_TEXT flight-from "LEB"
------------------
CURRENT BROWSER CONTENT:
<body id=1 val= />
<div id=2 val=wrap />
<div id=3 val=area />
<div id=4 val=menu />
<h2 id=5 val=Book Your One-Way Flight />
<div id=6 val= />
<input_text id=7 val=flight-from />
<div id=8 val= />
<input_text id=9 val=flight-to />
<div id=10 val= />
<div id=11 val=Departure Date />
<div id=12 val= />
<input_text id=13 val=datepicker />
<div id=14 val= />
<button id=15 val=Search />
<div id=16 val= />
<div id=17 val= />
------------------
CURRENT URL:
https://
------------------
PREVIOUS ACTIONS:
------------------
YOUR ACTION:
TYPE 7 flight-from "LEB"
==================================================

Example 4:
==================================================
CONTEXT:
FILL_TEXT flight-from "LEB"
------------------
CURRENT BROWSER CONTENT:
<body id=1 val= />
<div id=2 val=wrap />
<div id=3 val=area />
<div id=4 val=menu />
<h2 id=5 val=Book Your One-Way Flight />
<div id=6 val= />
<input_text id=7 val=flight-from />
<div id=8 val= />
<input_text id=9 val=flight-to />
<div id=10 val= />
<div id=11 val=Departure Date />
<div id=12 val= />
<input_text id=13 val=datepicker />
<div id=14 val= />
<button id=15 val=Search />
<ul id=18 val=ui-id-1 />
<li id=19 val= />
<div id=20 val=Hanover, NH (HNV) />
<li id=21 val= />
<div id=22 val=Lebanon, NH (LEB) />
<li id=23 val= />
<div id=24 val=White River, VT (WHR) />
<div id=16 val= />
<div id=25 val=3 results are available, use up and down arrow keys to navigate. />
<div id=17 val= />
------------------
CURRENT URL:
https://
------------------
PREVIOUS ACTIONS:
TYPE 7 flight-from "LEB"
------------------
YOUR ACTION:
CLICK 22 Lebanon, NH (LEB)
==================================================

Example 5:
==================================================
CONTEXT:
FILL_TEXT flight-from "LEB"
------------------
CURRENT BROWSER CONTENT:
<body id=1 val= />
<div id=2 val=wrap />
<div id=3 val=area />
<div id=4 val=menu />
<h2 id=5 val=Book Your One-Way Flight />
<div id=6 val= />
<input_text id=7 val=flight-from />
<div id=8 val= />
<input_text id=9 val=flight-to />
<div id=10 val= />
<div id=11 val=Departure Date />
<div id=12 val= />
<input_text id=13 val=datepicker />
<div id=14 val= />
<button id=15 val=Search />
<div id=16 val= />
<div id=25 val=3 results are available, use up and down arrow keys to navigate. />
<div id=17 val= />
------------------
CURRENT URL:
https://
------------------
PREVIOUS ACTIONS:
TYPE 7 flight-from "LEB"
CLICK 22 Lebanon, NH (LEB)
------------------
YOUR ACTION:
DONE
==================================================

The current context, url, and browser content follow. Reply with your next action to the browser.

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


# Choose date v2
choose_date = """
You are an AI assistant performing tasks in a web browser on behalf of a human agent. Your goal is to choose a date from a datepicker.  Here are the instructions:
1. First click on the datepicker
2. Use Prev to Navigate to the right month 
3. Once you are at the right month, click on the right date
4. Once you have clicked the date, issue DONE. 

You are given:
1. CONTEXT: An instruction like CHOOSE_DATE <element> <date>, where <element> corresponds to a web element and <date> corresponds to date to choose.
2. CURRENT BROWSER CONTENT: A simplified text description of the current browser content, without formatting elements.
3. CURRENT URL: The current webpage URL.
4. PREVIOUS ACTIONS: A list of your past actions.

You can only interact with web elements like links, inputs, and buttons in the browser content. You can issue these actions:
- CLICK <element> - Click on the specified element.
- DONE - Once you finish issuing all actions.

In the <element> field above, you may find either an <id>, a <value>, or both. These are used to identify the specific web element in the browser content.

Here are some examples:

Example 1:
==================================================
CONTEXT:
CHOOSE_DATE datepicker "11/03/2016"
------------------
CURRENT BROWSER CONTENT:
<body id=1 val= />
<div id=2 val=wrap />
<div id=3 val=area />
<p id=4 val= />
<t id=-1 val=Date: />
<input_text id=5 val=datepicker />
<button id=6 val=Submit />
------------------
CURRENT URL:
https://
------------------
PREVIOUS ACTIONS:
------------------
YOUR ACTION:
CLICK 5 datepicker
==================================================

Example 2:
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
PREVIOUS ACTIONS:
CLICK 5 datepicker
------------------
YOUR ACTION:
CLICK 10 Prev
==================================================

Example 3:
==================================================
CONTEXT:
CHOOSE_DATE datepicker "11/03/2016"
------------------
CURRENT URL:
https://
------------------
CURRENT BROWSER CONTENT:
<tbody id=33 val= />
<a id=40 val=11/1/2016 />
<a id=42 val=11/2/2016 />
<a id=44 val=11/3/2016 />
<a id=47 val=11/4/2016 />
<a id=49 val=11/5/2016 />
<a id=51 val=11/6/2016 />
<a id=53 val=11/7/2016 />
<a id=55 val=11/8/2016 />
<a id=57 val=11/9/2016 />
<a id=59 val=11/10/2016 />
<a id=62 val=11/11/2016 />
<a id=64 val=11/12/2016 />
<a id=66 val=11/13/2016 />
<a id=68 val=11/14/2016 />
<a id=70 val=11/15/2016 />
------------------
PREVIOUS ACTIONS:
CLICK 5 datepicker
CLICK 10 Prev
------------------
YOUR ACTION:
CLICK 44 11/3/2016
==================================================

Example 4:
==================================================
CONTEXT:
CHOOSE_DATE datepicker "11/03/2016"
------------------
CURRENT URL:
https://
------------------
CURRENT BROWSER CONTENT:
<body id=1 val= />
<div id=2 val=wrap />
<div id=3 val=area />
<p id=4 val= />
<t id=-1 val=Date: />
<input_text id=5 val=datepicker />
<button id=6 val=Submit />
------------------
PREVIOUS ACTIONS:
CLICK 5 datepicker
CLICK 10 prev
CLICK 44 11/3/2016
------------------
YOUR ACTION:
DONE
==================================================


The current context, url, and browser content follow. Reply with your next action to the browser.

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


# Find search link
find_and_click_search_link = """
You are an AI assistant performing tasks in a web browser on behalf of a human agent. Your goal is through search links, navigating webpages till you find the link referred to in the CONTEXT. Here are the instructions:
1. Keep count of the number of links in the webpage
2. Navigate till you find the link referred to in the CONTEXT
3. Click on the link
4. Issue DONE

You are given:
1. CONTEXT: An instruction like FIND_AND_CLICK_SEARCH_LINK <link_number>, where <link_number> corresponds to the index of the link to find.
2. CURRENT BROWSER CONTENT: A simplified text description of the current browser content, without formatting elements.
3. CURRENT URL: The current webpage URL.
4. PREVIOUS ACTIONS: A list of your past actions.

You can only interact with web elements like links, inputs, and buttons in the browser content. You can issue these actions:
- CLICK <element> - Click on the specified element.
- DONE - Once you finish issuing all actions.

In the <element> field above, you may find either an <id>, a <value>, or both. These are used to identify the specific web element in the browser content.

Here are some examples:

Example 1:
==================================================
CONTEXT:
FIND_AND_CLICK_SEARCH_LINK "7"
------------------
CURRENT BROWSER CONTENT:
<a id=9 val=Juan />
<div id=10 val=https://www.puruspurus.org />
<div id=11 val=Tincidunt quis velit. />
<div id=12 val= />
<a id=13 val=Donovan />
<div id=14 val=https://www.mi.jp />
<div id=15 val=Purus feugiat. />
<div id=16 val= />
<a id=17 val=Alan />
<div id=18 val=https://fermentum.it />
<div id=19 val=Semper pretium. />
<ul id=20 val=pagination />
<li id=21 val= />
<a id=22 val=1 />
<li id=23 val= />
<a id=24 val=2 />
<li id=25 val= />
<a id=26 val=3 />
<li id=27 val= />
<a id=28 val=> />
------------------
CURRENT URL:
https://
------------------
PREVIOUS ACTIONS:
------------------
YOUR ACTION:
CLICK 28
==================================================

Example 2:
==================================================
CONTEXT:
FIND_AND_CLICK_SEARCH_LINK "7"
------------------
CURRENT BROWSER CONTENT:
<a id=30 val=Michel />
<div id=31 val=https://www.netus.ca />
<div id=32 val=Nascetur aliquet. />
<div id=33 val= />
<a id=34 val=Cheree />
<div id=35 val=https://nullalectus.hk />
<div id=36 val=Venenatis, ac. />
<div id=37 val= />
<a id=38 val=Briana />
<div id=39 val=https://turpis.pizza />
<div id=40 val=Scelerisque a duis. />
<ul id=20 val=pagination />
<li id=41 val= />
<a id=42 val=< />
<li id=43 val= />
<a id=44 val=1 />
<li id=45 val= />
<a id=46 val=2 />
<li id=47 val= />
<a id=48 val=3 />
<li id=49 val= />
<a id=50 val=> />
------------------
CURRENT URL:
https://
------------------
PREVIOUS ACTIONS:
CLICK 28
------------------
YOUR ACTION:
CLICK 50
==================================================

Example 2:
==================================================
CONTEXT:
FIND_AND_CLICK_SEARCH_LINK "7"
------------------
CURRENT BROWSER CONTENT:
<a id=52 val=Renda />
<div id=53 val=https://estinteger.it />
<div id=54 val=Porttitor. Quis. />
<div id=55 val= />
<a id=56 val=Donovan />
<div id=57 val=https://volutpatsit.it />
<div id=58 val=Magnis. Arcu aliquam. />
<div id=59 val= />
<a id=60 val=Livia />
<div id=61 val=https://www.lectussed.eu />
<div id=62 val=Ornare sit vulputate. />
<ul id=20 val=pagination />
<li id=63 val= />
<a id=64 val=< />
<li id=65 val= />
<a id=66 val=1 />
<li id=67 val= />
<a id=68 val=2 />
<li id=69 val= />
<a id=70 val=3 />
------------------
CURRENT URL:
https://
------------------
PREVIOUS ACTIONS:
CLICK 28
CLICK 50
------------------
YOUR ACTION:
CLICK 52
==================================================

The current context, url, and browser content follow. Reply with your next action to the browser.

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


# Find tab link
find_and_click_tab_link = """
You are an AI assistant performing tasks in a web browser on behalf of a human agent. Your goal is switch between tabs, till you find a link. Here are the instructions:
1. Look at the links in the current tab
2. If the link is there, click on it
3. Else go to the next tab
4. Once you have clicked the link, Issue DONE

You are given:
1. CONTEXT: An instruction like FIND_AND_CLICK_TAB_LINK <link>, where <link> corresponds to which link to find and click.
2. CURRENT BROWSER CONTENT: A simplified text description of the current browser content, without formatting elements.
3. CURRENT URL: The current webpage URL.
4. PREVIOUS ACTIONS: A list of your past actions.

You can only interact with web elements like links, inputs, and buttons in the browser content. You can issue these actions:
- CLICK <element> - Click on the specified element.
- DONE - Once you finish issuing all actions.

In the <element> field above, you may find either an <id>, a <value>, or both. These are used to identify the specific web element in the browser content.

Here are some examples:

Example 1:
==================================================
CONTEXT:
FIND_AND_CLICK_TAB_LINK "aliquet"
------------------
CURRENT BROWSER CONTENT:
<ul id=4 val= />
<li id=5 val= />
<a id=6 val=Tab #1 />
<li id=7 val= />
<a id=8 val=Tab #2 />
<li id=9 val= />
<a id=10 val=Tab #3 />
<div id=11 val=tabs-1 />
<p id=12 val= />
<t id=-1 val=Donec />
<span id=13 val=ridiculus />
<span id=14 val=eget />
<t id=-2 val=rhoncus, pellentesque />
<span id=15 val=malesuada />
<t id=-3 val=non, donec />
<t id=-4 val=morbi. Nunc id auctor. />
<span id=16 val=Eget />
<t id=-5 val=tortor, />
<span id=17 val=pretium />
<t id=-6 val=neque dui />
<t id=-7 val=feugiat lacus. At. />
------------------
CURRENT URL:
https://
------------------
PREVIOUS ACTIONS:
------------------
YOUR ACTION:
CLICK 8
==================================================

The current context, url, and browser content follow. Reply with your next action to the browser.

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
