autolabel_liveweb = """

You are an AI assistant labeling web actions as one of several skills.

You are given:
- a CONTEXT that contains the objective you are trying to achieve. The objective may be explicitly stated or be implicit in a conversation between a customer (CUS) and agent (REP).
- A simplified text description of the browser content and the current webpage URL. The browser content is highly simplified with all formatting elements removed. 
- The current web action being performed
- The previous label that was assigned

You can only assign labels from the following types
- FILL_TEXT "desription" "TEXT" - fill a text box
- CHOOSE_DATE "desription" "DATE" - choose a date from a date grid
- CLICK "desription" - click a button

==================================================
CONTEXT:
Book a flight from Boston to Chicago departing on Dec 1, 2023 and returning on Dec 12, 2023
------------------
CURRENT BROWSER CONTENT:
<text id=10>JetBlue Home</text>
<text id=11>Where on Earth are you headed?</text>
<button id=12>Flights</button>
<button id=13>Flights + Hotel</button>
<button id=14>Flights + Cruise</button>
<button id=15>Cars</button>
<button id=16>Stays</button>
<button id=17>Roundtrip</button>
<button id=18 title="Travelers">1 Adult</button>
<text id=19>Use TrueBlue points</text>
<text id=20>From</text>
<input id=21 text>Washington D.C. area (WAS)</input>
<button id=22>Reverse origin and destination city or airport</button>
<text id=23>To</text>
<input id=24 text/>
<text id=25>Depart</text>
<input id=26 Depart Press DOWN ARROW key to select available dates/>
<text id=27>Return</text>
<input id=28 Return Press DOWN ARROW key to select available dates/>
<button id=29>Search flights</button>
------------------
CURRENT ACTION:
TYPE 21 Boston
PREVIOUS LABEL:
CURRENT LABEL:
FILL_TEXT From "Boston"
==================================================

==================================================
CONTEXT:
Book a flight from Boston to Chicago departing on Dec 1, 2023 and returning on Dec 12, 2023
------------------
CURRENT BROWSER CONTENT:
<text id=20>From</text>
<input id=21 text>Boston</input>
<text id=22>Boston</text>
<text id=23>area</text>
<text id=24>Boston</text>
<text id=25>, MA (BOS)</text>
<text id=26>Providence, RI (PVD)</text>
<text id=27>Worcester, MA (ORH)</text>
<text id=28>Browse by regions</text>
<text id=29>Browse by regions</text>
<text id=30>Mint Service</text>
<text id=31>Partner Airline</text>
<button id=32>Reverse origin and destination city or airport</button>
<text id=33>To</text>
<input id=34 text/>
<text id=35>Depart</text>
<input id=36 Depart Press DOWN ARROW key to select available dates/>
<text id=37>Return</text>
<input id=38 Return Press DOWN ARROW key to select available dates/>
<button id=39>Search flights</button>
------------------
CURRENT ACTION:
CLICK 24
PREVIOUS LABEL:
FILL_TEXT From "Boston"
CURRENT LABEL:
FILL_TEXT From "Boston"
==================================================

==================================================
CONTEXT:
Book a flight from Boston to Chicago departing on Dec 1, 2023 and returning on Dec 12, 2023
------------------
CURRENT BROWSER CONTENT:
<button id=13>Flights + Hotel</button>
<button id=14>Flights + Cruise</button>
<button id=15>Cars</button>
<button id=16>Stays</button>
<button id=17>Roundtrip</button>
<button id=18 title="Travelers">1 Adult</button>
<text id=19>Use TrueBlue points</text>
<text id=20>From</text>
<input id=21 text>Boston, MA (BOS)</input>
<button id=22>Reverse origin and destination city or airport</button>
<text id=23>To</text>
<input id=24 text/>
<text id=25>Browse by regions</text>
<text id=26>Mint Service</text>
<text id=27>Partner Airline</text>
<text id=28>Depart</text>
<input id=29 Depart Press DOWN ARROW key to select available dates/>
<text id=30>Return</text>
<input id=31 Return Press DOWN ARROW key to select available dates/>
<button id=32>Search flights</button>
------------------
CURRENT ACTION:
TYPE 24 Chicago
PREVIOUS LABEL:
FILL_TEXT From "Boston"
CURRENT LABEL:
FILL_TEXT To "Chicago"
==================================================

==================================================
CONTEXT:
Book a flight from Boston to Chicago departing on Dec 1, 2023 and returning on Dec 12, 2023
------------------
CURRENT BROWSER CONTENT:
<text id=20>From</text>
<input id=21 text>Boston, MA (BOS)</input>
<button id=22>Reverse origin and destination city or airport</button>
<text id=23>To</text>
<input id=24 text>Chicago</input>
<text id=25>Chicago</text>
<text id=26>, IL (ORD)</text>
<text id=27>Browse by regions</text>
<text id=28>Browse by regions</text>
<text id=29>Mint Service</text>
<text id=30>Partner Airline</text>
<text id=31>Depart</text>
<input id=32 Depart Press DOWN ARROW key to select available dates/>
<text id=33>Return</text>
<input id=34 Return Press DOWN ARROW key to select available dates/>
<button id=35>Search flights</button>
------------------
CURRENT ACTION:
CLICK 25
PREVIOUS LABEL:
FILL_TEXT To "Chicago"
CURRENT LABEL:
FILL_TEXT To "Chicago"
==================================================

==================================================
CONTEXT:
Book a flight from Boston to Chicago departing on Dec 1, 2023 and returning on Dec 12, 2023
------------------
CURRENT BROWSER CONTENT:
<button id=17>Roundtrip</button>
<button id=18 title="Travelers">1 Adult</button>
<text id=19>Use TrueBlue points</text>
<text id=20>From</text>
<input id=21 text>Boston, MA (BOS)</input>
<button id=22>Reverse origin and destination city or airport</button>
<text id=23>To</text>
<input id=24 text>Chicago, IL (ORD)</input>
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
<button id=43 aria-label="depart Thursday, April 6, 2023">6</button>
<button id=44 aria-label="depart Friday, April 7, 2023">7</button>
------------------
CURRENT ACTION:
TYPE 26 12/01/2023
PREVIOUS LABEL:
FILL_TEXT To "Chicago"
CURRENT LABEL:
CHOOSE_DATE Depart 12/01/2023
==================================================

==================================================
CONTEXT:
Book a flight from Boston to Chicago departing on Dec 1, 2023 and returning on Dec 12, 2023
------------------
CURRENT BROWSER CONTENT:
<button id=18 title="Travelers">1 Adult</button>
<text id=19>Use TrueBlue points</text>
<text id=20>From</text>
<input id=21 text>Boston, MA (BOS)</input>
<button id=22>Reverse origin and destination city or airport</button>
<text id=23>To</text>
<input id=24 text>Chicago, IL (ORD)</input>
<text id=25>Depart</text>
<input id=26 Depart Press DOWN ARROW key to select available dates>12/01/2023</input>
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
------------------
CURRENT ACTION:
TYPE 28 12/12/2023
PREVIOUS LABEL:
CHOOSE_DATE Depart 12/01/2023
CURRENT LABEL:
CHOOSE_DATE Return 12/12/2023
==================================================

==================================================
CONTEXT:
Book a flight from Boston to Chicago departing on Dec 1, 2023 and returning on Dec 12, 2023
------------------
CURRENT BROWSER CONTENT:
<link id=4>Book</link>
<link id=5>Manage Trips</link>
<link id=6>Check In</link>
<link id=7>Travel Info</link>
<link id=8>TrueBlue</link>
<link id=9 aria-label="Shopping cart (Empty)"/>
<text id=108>Flights available for sale through Mar 19, 2024.</text>
<button id=109>Done</button>
<button id=110>Search flights</button>
------------------
CURRENT ACTION:
CLICK 110
PREVIOUS LABEL:
CHOOSE_DATE Return 12/12/2023
CURRENT LABEL:
CLICK Search flights
==================================================

The current context, browser content, action, previous label are below. Reply with your current label.

==================================================
CONTEXT:
{context}
------------------
CURRENT BROWSER CONTENT:
{browser_content}
------------------
CURRENT ACTION:
{current_action}
------------------
PREVIOUS LABEL:
{previous_label}
------------------
CURRENT LABEL:
"""