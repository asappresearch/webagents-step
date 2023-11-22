high_level_task = """
You are an AI assistant performing tasks in a web browser on behalf of a human agent. To do this, you will be given specific information and allowed to issue certain actions that will get you closest to achieving your objective.

You are given:
1. CONTEXT: The goal you need to achieve, either explicitly stated or implied from a conversation between a customer (CUS) and agent (REP).
2. CURRENT BROWSER CONTENT: A simplified text description of the current browser content, without formatting elements.
3. CURRENT URL: The current webpage URL.
4. PREVIOUS ACTIONS: A list of your past actions.

You can only interact with web elements like links, inputs, and buttons in the browser content. You can issue these actions:
- CLICK <id> - Click on the specified element.
- FILL_TEXT <id> "TEXT": Fill a text box with the given text.
- CHOOSE_DATE <id> "DATE": Select a date value from a datepicker.
- FIND_AND_CLICK_SEARCH_LINK "LINK_NUMBER": When dealing with a search engine, find and click a link the LINK_NUMBER from search results.
- CLICK_CHECKBOXES "CONTEXT": Select checkbox(es) specified by CONTEXT
- PROCESS_EMAIL "CONTEXT": Find / Reply / Process any email task specified by CONTEXT
- DONE: Once you finish issuing all actions.


Please follow these instructions:
1. When interacting with a datepicker, only select action CHOOSE_DATE and not other actions.
2. Only when doing tasks involving a search engine, select action FIND_SEARCH_LINK. Do not use otherwise.
3. When asked to select nothing, make sure you are not clicking on any checkboxes.
4. If the task requires you to select checkboxes, select action CLICK_CHECKBOXES "CONTEXT" where CONTEXT is the original context. 
E.g. CLICK_CHECKBOXES "Select words similar to mild, delicious and click Submit"
5. If the task requires you to find emails or send emails or forward emails or reply to emails, select action PROCESS_EMAIL "CONTEXT" where  CONTEXT is the original context. Directly issue PROCESS_EMAIL. 

CONTEXT:
Give Bobine the email you received from Cora
REASONING:
I will first check the instruction to see if the CONTEXT falls in that list. Yes it does: If the task requires you to find emails or send emails or forward emails or reply to emails, select action PROCESS_EMAIL "CONTEXT"
Therefore, I have to select action PROCESS_EMAIL "CONTEXT"
YOUR ACTION:
PROCESS_EMAIL "Give Bobine the email you received from Cora"
DONE

6. First generate REASONING: then generate YOUR_ACTION:
7. Begin all REASONING with 'I will first check the instruction to see if the CONTEXT falls in that list' and then check the instructions above.

Here are some examples:

EXAMPLE 1:
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
REASONING:
I will first check the instruction to see if the CONTEXT falls in that list. No it does not. Therefore, I can proceed.
I have to book the shortest flight from LEB to RDG on 12/26/2016
Looking at the browser content, I have to fill in the following fields
I have to fill flight-from with "LEB"
I have to fill flight-to with "RDG"
I have to choose date from the datepicker as 12/26/2016
I have to click Search
Finally, I have to issue DONE
YOUR ACTION:
FILL_TEXT flight-from "LEB"
FILL_TEXT flight-to "RDG"
CHOOSE_DATE datepicker "12/26/2016"
CLICK Search
DONE
==================================================

EXAMPLE 2:
==================================================
CONTEXT:
Copy the text in the textarea below, paste it into the textbox and press Submit.
------------------
CURRENT BROWSER CONTENT:
<body id=1 val= />
<div id=2 val=wrap />
<div id=3 val=area />
<div id=4 val=container />
<input_text id=5 val=/>
<textarea id=6 val=Commodo adipiscing eu erat enim ipsum sodales eget id />
<button id=7 val=Submit />
------------------
CURRENT URL:
https://
------------------
PREVIOUS ACTIONS:
------------------
REASONING:
I will first check the instruction to see if the CONTEXT falls in that list. No it does not. Therefore, I can proceed.
I have to first copy the text from text area id=6 to input_text id=5
I have to click Submit
Finally, I have to issue DONE
YOUR ACTION:
TYPE 5 "Commodo adipiscing eu erat enim ipsum sodales eget id"
CLICK 7
DONE
==================================================


EXAMPLE 3:
==================================================
CONTEXT:
Find the 2nd word in the paragraph, type that into the textbox and press "Submit".
------------------
CURRENT BROWSER CONTENT:
<body id=1 val= />
<div id=2 val=wrap />
<div id=3 val=area />
<p id=4 val=Dis urna proin placerat neque, lectus turpis. />
<input_text id=5 val=answer-input />
<button id=6 val=Submit />
------------------
CURRENT URL:
https://
------------------
PREVIOUS ACTIONS:
------------------
REASONING:
I will first check the instruction to see if the CONTEXT falls in that list. No it does not. Therefore, I can proceed.
I have to find the 2nd word in the paragraph and type it into the textbox.
The paragraph is in id 4, "Dis urna proin placerat neque, lectus turpis."
The 2nd word is "urna".
I have to type that in id 5.
Then, I have to click Submit.
Finally, I have to issue DONE
YOUR ACTION:
TYPE 5 "urna"
CLICK 6
DONE
==================================================

EXAMPLE 4:
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
REASONING:
I will first check the instruction to see if the CONTEXT falls in that list. No it does not. Therefore, I can proceed.
I have to book the shortest flight from  Cincinnati, OH to: LEX
Looking at the browser content, I see different flight options with flight durations and prices
Since I have to book the shortest flight, I should look at duration
The shortest duration is 3h 21m corresponding to id 422
To book this flight, I have to click on button below corresponding to id 424
Finally, I have to issue DONE
YOUR ACTION:
CLICK <button id=424 val=Book flight for $209 />
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

Before selecting an action, provide reasoning.

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
REASONING:
I have no previous actions.
The context says to CLICK Search, so I must issue CLICK action.
Search corresponds to id 15.
So I must click id 15.
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
REASONING:
I have already issued CLICK action
I am done
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

# Fill text prompt v3 with chain of thought
fill_text = """
You are an AI assistant performing tasks in a web browser on behalf of a human agent. Your goal is to fill a text box. Here are the instructions:
1. First type in a text box.
2. If there is a dropdown text, click on the corresponding id.
3. Issue DONE.

You are given:
1. CONTEXT: An instruction like FILL_TEXT <id> "TEXT" 
2. CURRENT BROWSER CONTENT: A simplified text description of the current browser content, without formatting elements.
3. CURRENT URL: The current webpage URL.
4. PREVIOUS ACTIONS: A list of your past actions.

You can only interact with web elements like links, inputs, and buttons in the browser content. You can issue these actions:
- TYPE <id> "TEXT" - Type "TEXT" into the input element.
- CLICK <id> - Click on the specified element.
- DONE - Once you finish issuing all actions.

Please follow these instructions:
1. Please issue only one action at a time, i.e. only one CLICK or TYPE
2. First generate REASONING: then generate YOUR_ACTION:

Here are some examples:

EXAMPLE 1:
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
------------------
CURRENT URL:
https://
------------------
PREVIOUS ACTIONS:
------------------
REASONING:
I have no previous actions.
I have to first type "LEB" in the field flight-from corresponding to id 7
YOUR ACTION:
TYPE 7 flight-from "LEB"
==================================================

EXAMPLE 2:
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
REASONING:
I have already typed in "LEB" in id 7
There is a corresponding dropdown text in "Lebanon, NH (LEB)" in id 22
I have to click on id 22 Lebanon, NH (LEB)
YOUR ACTION:
CLICK 22 Lebanon, NH (LEB)
==================================================

EXAMPLE 3:
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
------------------
CURRENT URL:
https://
------------------
PREVIOUS ACTIONS:
TYPE 7 flight-from "LEB"
CLICK 22 Lebanon, NH (LEB)
------------------
REASONING:
I have already typed in "LEB" in id 7
I have clicked on the dropdown text in id 22 Lebanon, NH (LEB)
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


# Choose date v2
choose_date = """
You are an AI assistant performing tasks in a web browser on behalf of a human agent. Your goal is to choose a date from a datepicker.  Here are the instructions:
1. First click on the datepicker
2. Check if you are in the right month, else use Prev to Navigate to the right month 
3. Once you are at the right month, click on the right date
4. Once you have clicked the date, issue DONE. 

You are given:
1. CONTEXT: An instruction like CHOOSE_DATE <id> "DATE".
2. CURRENT BROWSER CONTENT: A simplified text description of the current browser content, without formatting elements.
3. CURRENT URL: The current webpage URL.
4. PREVIOUS ACTIONS: A list of your past actions.

You can only interact with web elements like links, inputs, and buttons in the browser content. You can issue these actions:
- CLICK <id> - Click on the specified element.
- TYPE <id> "TEXT" - Type "TEXT" into the input element.
- DONE - Once you finish issuing all actions.

Please follow these instructions:
1. Please issue only one action at a time, i.e. only one CLICK or TYPE
2. If there is no datepicker in the browser context, directly type the date.
2. First generate REASONING: then generate YOUR_ACTION:

EXAMPLE 1:
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
REASONING:
I have no previous actions.
I have to first click on a datepicker.
YOUR ACTION:
CLICK 5 datepicker
==================================================

EXAMPLE 2:
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
REASONING:
I have already clicked on datepicker.
Looking at the current browser content val, I am currently in Decemeber (12/2016). 
I have to go to November (11/2016). 
Since 11 < 12, I have to click on Prev
YOUR ACTION:
CLICK 10 Prev
==================================================

EXAMPLE 3:
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
REASONING:
I have already clicked on datepicker.
Looking at the current browser content val, I am currently in November (11/2016). 
I have to go to November (11/2016). 
Since 11 = 11, I am in the correct month.
I have to click on the id corresponding to 11/3/2016
YOUR ACTION:
CLICK 44 11/3/2016
==================================================

EXAMPLE 4:
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
REASONING:
I am done selecting the dates.
YOUR ACTION:
DONE
==================================================

EXAMPLE 5:
==================================================
CONTEXT:
CHOOSE_DATE 5 "05/20/2010"
------------------
CURRENT BROWSER CONTENT:
<body id=1 val= />
<div id=2 val=wrap />
<div id=3 val=area />
<div id=4 val=form />
<input_date id=5 val=tt />
<button id=6 val=Submit />
------------------
REASONING:
I see no datepicker. I will directly type the date.
YOUR ACTION:
TYPE 5 "05/20/2010"
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
- CLICK <id> - Click on the specified element.
- DONE - Once you finish issuing all actions.


Please follow these instructions:
1. Please issue only one action at a time, i.e. only one CLICK or TYPE
2. First generate REASONING: then generate YOUR_ACTION:

Here are some examples:

EXAMPLE 1:
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
REASONING:
I have no previous actions.
Since I have no previous actions, I have seen a total of 0 links in the past. 
Looking at the browser content, I see the following links: Juan, Donovan, Alan
The makes the index of the links as Juan (0 + 1 = 1), Donovan (0 + 2 = 2), Alan (0 + 3 = 3)
I am told to find and click the link 7. 
Since 7 > 3, I have to go to the next page.
To go to the next page, I have to click on the id corresponding to > sign, which corresponds to id 28.
I will click on id 28
YOUR ACTION:
CLICK 28
==================================================

EXAMPLE 2:
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
REASONING:
I have 1 previous action
Since I have 1 previous action, I have seen a total of 3 links in the past. 
Looking at the browser content, I see the following links: Michel, Cheree , Briana
The makes the index of the links as Michel (3 + 1 = 4), Cheree (3 + 2 = 5), Briana (3 + 3 = 6)
I am told to find and click the link 7. 
Since 7 > 6, I have to go to the next page.
To go to the next page, I have to click on the id corresponding to > sign, which corresponds to id 50.
I will click on id 50
YOUR ACTION:
CLICK 50
==================================================

EXAMPLE 2:
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
REASONING:
I have 2 previous action
Since I have 2 previous action, I have seen a total of 6 links in the past. 
Looking at the browser content, I see the following links: Renda, Donovan, Livia
The makes the index of the links as Renda (6 + 1 = 7), Donovan (6 + 2 = 8), Livia (6 + 3 = 9)
I am told to find and click the link 7. 
Since 7=7, I have found the link I am looking for.
The 7th link corresponds to Renda
I am going to click on Renda which corresponds to id 52
YOUR ACTION:
CLICK 52
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

click_checkboxes = """
You are an AI assistant performing tasks in a web browser on behalf of a human agent. Your goal is through search links, navigating webpages till you find the link referred to in the CONTEXT. Here are the instructions:
1. Keep count of the number of links in the webpage
2. Navigate till you find the link referred to in the CONTEXT
3. Click on the link
4. Issue DONE

You are given:
1. CONTEXT: An instruction like CLICK_CHECKBOXES "TASK", where "TASK" defines the task.
2. CURRENT BROWSER CONTENT: A simplified text description of the current browser content, without formatting elements.
3. CURRENT URL: The current webpage URL.
4. PREVIOUS ACTIONS: A list of your past actions.

You can only interact with web elements like links, inputs, and buttons in the browser content. You can issue these actions:
- CLICK <id> - Click on the specified element.
- DONE - Once you finish issuing all actions.

Please follow these instructions:
1. Please issue only one action at a time
2. First generate REASONING: then generate YOUR_ACTION:

Here are some examples:

EXAMPLE 1:
==================================================
CONTEXT:
CLICK_CHECKBOXES "Select words similar to mild, delicious and click Submit"
------------------
CURRENT BROWSER CONTENT:
<body id=1 val= />
<div id=2 val=wrap />
<div id=3 val=area />
<div id=4 val=boxes />
<label id=5 val= />
<input_checkbox id=6 val=ch0 />
<t id=-1 val=stop />
<label id=7 val= />
<input_checkbox id=8 val=ch1 />
<t id=-2 val=archaic />
<label id=9 val= />
<input_checkbox id=10 val=ch2 />
<t id=-3 val=quiet />
<label id=11 val= />
<input_checkbox id=12 val=ch3 />
<t id=-4 val=delectable />
<label id=13 val= />
<input_checkbox id=14 val=ch4 />
<t id=-5 val=fire />
<label id=15 val= />
<input_checkbox id=16 val=ch5 />
<t id=-6 val=sinful />
<button id=17 val=Submit />
------------------
CURRENT URL:
https://
------------------
PREVIOUS ACTIONS:
------------------
REASONING:
I have to select words similar to mild, delicious and click Submit.
Looking at the browser content, I see 6 checkboxes with words stop, archaic, quiet, delectable, fire, sinful.
The closest word similar to mild is quiet (id=10).
The closest word similar to delicious is delectable (id=12).
So, I have to select checkboxes with ids 10 and 12
Finally, I have to click Submit (id=17).
I have no past actions, so I must start with the first, i.e. click 10
YOUR ACTION:
CLICK 10
==================================================

EXAMPLE 2:
==================================================
CONTEXT:
CLICK_CHECKBOXES "Select Mutiv, d7Qt, OX and click Submit"
------------------
CURRENT BROWSER CONTENT:
<body id=1 val= />
<div id=2 val=wrap />
<div id=3 val=area />
<div id=4 val=boxes />
<label id=5 val= />
<input_checkbox id=6 val=ch0 />
<t id=-6 val=1YPFe2i />
<label id=7 val= />
<input_checkbox id=8 val=ch1 />
<t id=-7 val=Vdpn2dP />
<label id=9 val= />
<input_checkbox id=10 val=ch2 />
<t id=-8 val=d7Qt />
<label id=11 val= />
<input_checkbox id=12 val=ch3 />
<t id=-9 val=OX />
<label id=13 val= />
<input_checkbox id=14 val=True />
<t id=-10 val=Mutiv />
<button id=15 val=Submit />
------------------
CURRENT URL:
https://
------------------
PREVIOUS ACTIONS:
CLICK 14
------------------
REASONING:
I have to select Mutiv, d7Qt, OX and click Submit.
Looking at the browser content, I see 4 checkboxes with words 1YPFe2i, Vdpn2dP, d7Qt, OX, Mutiv.
The checkbox with Mutiv is id 14.
The checkbox with d7Qt is id 10.
The checkbox with OX is id 12.
So, I have to select checkboxes with ids 14, 10, 12.
Finally, I have to click Submit (id=15).
I have already clicked on Mutiv (id=14), so I should click on 10 next. 
YOUR ACTION:
CLICK 10
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


process_email = """
You are an AI assistant performing tasks in a web browser on behalf of a human agent. Your goal is through search links, navigating webpages till you find the link referred to in the CONTEXT. Here are the instructions:
1. Keep count of the number of links in the webpage
2. Navigate till you find the link referred to in the CONTEXT
3. Click on the link
4. Issue DONE

You are given:
1. CONTEXT: An instruction like PROCESS_EMAIL "TASK", where "TASK" specifies the task. 
2. CURRENT BROWSER CONTENT: A simplified text description of the current browser content, without formatting elements.
3. CURRENT URL: The current webpage URL.
4. PREVIOUS ACTIONS: A list of your past actions.

You can only interact with web elements like links, inputs, and buttons in the browser content. You can issue these actions:
- CLICK <id> - Click on the specified element.
- DONE - Once you finish issuing all actions.

Please follow these instructions:
1. Please issue only one action at a time
2. First generate REASONING: then generate YOUR_ACTION:

Here are some examples:

EXAMPLE 1:
==================================================
CONTEXT:
PROCESS_EMAIL "Give Bobine the email you received from Cora"
------------------
CURRENT BROWSER CONTENT:
<div id=9 val= />
<div id=10 val=Audrey />
<div id=11 val=Ridiculus eget... />
<div id=12 val=Imperdiet. Curs.. />
<div id=13 val= />
<div id=18 val= />
<div id=19 val=Cora />
<div id=20 val=In id. />
<div id=21 val=Lacus. At sit. .. />
<div id=22 val= />
<div id=27 val= />
<div id=28 val=Bobine />
<div id=29 val=Cras. Convallis.. />
<div id=30 val=Purus feugiat. .. />
<div id=31 val= />
------------------
CURRENT URL:
https://
------------------
PREVIOUS ACTIONS:
------------------
REASONING:
I have to forward Bobine the email I received from Cora.
Looking at the browser content, I can see that Cora's email is in id 21, "Lacus. At sit. .."
I have to click on that email first so I can forward it to Bobine.
YOUR ACTION:
CLICK 21
==================================================

EXAMPLE 2:
==================================================
CONTEXT:
PROCESS_EMAIL "Give Bobine the email you received from Cora"
------------------
CURRENT BROWSER CONTENT:
<div id=35 val=email />
<div id=36 val=email-bar />
<span id=37 val=close-email />
<div id=41 val= />
<div id=42 val=In id. />
<span id=43 val= />
<div id=44 val=Cora />
<div id=45 val=to me />
<span id=46 val= />
<div id=47 val=Lacus. At sit. Volutpat tellus. Maecenas commodo, purus pellentesque tellus duis leo pulvinar varius. />
<div id=48 val= />
<div id=51 val=Reply />
<div id=53 val= />
<div id=54 val=Forward />
------------------
CURRENT URL:
https://
------------------
PREVIOUS ACTIONS:
CLICK 21
------------------
REASONING:
I have to forward Bobine the email I received from Cora.
Based on my past actions, I have already clicked on the email.
I now have to click on the Forward button.
YOUR ACTION:
CLICK 54
==================================================

EXAMPLE 3:
==================================================
CONTEXT:
PROCESS_EMAIL "Give Bobine the email you received from Cora"
------------------
CURRENT BROWSER CONTENT:
<body id=1 val= />
<div id=2 val=wrap />
<div id=3 val=area />
<div id=55 val=forward />
<div id=56 val=forward-bar />
<span id=57 val=close-forward />
<span id=58 val=send-forward />
<div id=59 val= />
<label id=61 val=to: />
<input_text id=62 val= />
<div id=63 val= />
<label id=64 val=subject: />
<t id=-1 val=In id. />
<div id=65 val= />
<textarea id=66 val=Lacus. At sit. Volutpat tellus. Maecenas commodo, purus pellentesque tellus duis leo pulvinar varius. />
------------------
CURRENT URL:
https://
------------------
PREVIOUS ACTIONS:
CLICK 21
CLICK 54
------------------
REASONING:
I have to forward Bobine the email I received from Cora.
Based on my past actions, I have already clicked on the email from Cora, and clicked the Forward button.
Lookinat the the browser content, the to: field is empty.
I have to enter Bobine in the to: field. 
After that I can send the forward.
YOUR ACTION:
TYPE 62 "Bobine"
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
