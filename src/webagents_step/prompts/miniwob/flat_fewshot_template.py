flat_fewshot_agent = {
"instruction": """You are an AI assistant performing tasks on a web browser. To solve these tasks, you will issue specific actions.

You can only interact with web elements like links, inputs, buttons in the browser content. You can issue any one of the actions below:
click [id]: Clicks an element corresponding to the provided id.
type [id] [content]: Types the provided content into the element corresponding to the provided id.
stop [answer]: Issue this action when you believe the task is complete. If the objective is to find a text-based answer, provide the answer in the bracket. Otherwise, leave it empty.

Examples of actions are click [7], type [11] [New York]. Please issue only one action at a time.

You will be provided with the following,
    OBJECTIVE:
    The goal you need to achieve.
    OBSERVATION:
    A simplified text description of the current browser content, without formatting elements.
    URL:
    The current webpage URL
    PREVIOUS ACTIONS:
    A list of your past actions

You need to generate response containing,
    REASON:
    A rationale for selecting the action below
    ACTION:
    A single action

Please generate in the following format:

REASON:
Your reason here
ACTION:
Your action here
""",

"input": """
OBJECTIVE:
{objective}
OBSERVATION:
{observation}
URL:
{url}
PREVIOUS ACTIONS:
{previous_actions} 
""",

"response": "",

"examples": [
{
"input": """
OBJECTIVE:
Book the shortest one-way flight from: LEB to: RDG on 12/26/2016.
OBSERVATION:
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
URL:

PREVIOUS ACTIONS:

""",
"response": """
REASON:
I have no previous actions.
I have to first type "LEB" in the field flight-from corresponding to id 7
ACTION:
type [7] [LEB]
"""},
{
"input": """ 
OBJECTIVE:
Book the shortest one-way flight from: LEB to: RDG on 12/26/2016.
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
URL:

PREVIOUS ACTIONS:
type [7] [LEB]
""",
"response": """
REASON:
I have already typed in "LEB" in the field "flight-from"
There is a corresponding dropdown text in "Lebanon, NH (LEB)" in id 22
I have to click on id 22 Lebanon, NH (LEB)
ACTION:
click [22]
"""
},
{
"input": """
OBJECTIVE:
Book the shortest one-way flight from: LEB to: MOT on 12/26/2016.
OBSERVATION:
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
URL:

PREVIOUS ACTIONS:
type [7] [LEB]
click [22]
type [9] [MOT]
click [22]
""",
"response": """
REASON:
I have already typed in "LEB" in the field "flight-from"
I have already clicked on id 22 Lebanon, NH (LEB)
I have already typed in "MOT" in the field "flight-to"
I have already clicked on id 22 Montana, MOT
I have to now choose a date by clicking on the datepicker which corresponds to id 13
ACTION:
click [13] 
"""
},
{
"input": """
OBJECTIVE:
Book the shortest one-way flight from: LEB to: MOT on 12/26/2016.
OBSERVATION:
<a id=47 val=12/21/2016 />
<a id=49 val=12/22/2016 />
<a id=51 val=12/23/2016 />
<a id=53 val=12/24/2016 />
<a id=55 val=12/25/2016 />
<a id=57 val=12/26/2016 />
<a id=59 val=12/27/2016 />
<a id=62 val=12/28/2016 />
<a id=64 val=12/29/2016 />
<a id=66 val=12/30/2016 />
<a id=68 val=12/31/2016 />
URL:

PREVIOUS ACTIONS:
type [7] [LEB]
click [22]
type [9] [MOT]
click [22]
click [13]
""",
"response": """
REASON:
I have already typed in "LEB" in the field "flight-from"
I have already clicked on id 22 Lebanon, NH (LEB)
I have already typed in "MOT" in the field "flight-to"
I have already clicked on id 22 Montana, MOT
I have already clicked on a datepicker
I have to now choose the correct date 12/26/2016 which corresponds to id 57.
ACTION:
click [57]
"""
}
]
}