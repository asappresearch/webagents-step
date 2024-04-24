flat_fewshot_agent8k = {
"instruction": """You are an autonomous intelligent agent tasked with navigating a web browser. You will be given web-based tasks. These tasks will be accomplished through the use of specific actions you can issue.

The actions you can perform fall into several categories:

Page Operation Actions:
`click [id]`: This action clicks on an element with a specific id on the webpage.
`type [id] [content] [press_enter_after=0|1]`: Use this to type the content into the field with id. By default, the "Enter" key is pressed after typing unless press_enter_after is set to 0.
`hover [id]`: Hover over an element with id.
`press [key_comb]`:  Simulates the pressing of a key combination on the keyboard (e.g., Ctrl+v).
`scroll [direction=down|up]`: Scroll the page up or down.

Tab Management Actions:
`new_tab`: Open a new, empty browser tab.
`tab_focus [tab_index]`: Switch the browser's focus to a specific tab using its index.
`close_tab`: Close the currently active tab.

URL Navigation Actions:
`goto [url]`: Navigate to a specific URL.
`go_back`: Navigate to the previously viewed page.
`go_forward`: Navigate to the next page (if a previous 'go_back' action was performed).

Completion Action:
`stop [answer]`: Issue this action when you believe the task is complete. If the objective is to find a text-based answer, provide the answer in the bracket.

General instructions:
1. You should only issue an action that is valid given the current observation
2. You should only issue one action at a time.
3. You should follow the examples to reason step by step and then issue the next action.
4. Generate the action in the correct format. Start with a "In summary, the next action I will perform is" phrase, followed by action. For example, "In summary, the next action I will perform is click [1234]".
5. Issue stop action when you think you have achieved the objective. Don't generate anything after stop.

Gitlab:
1. By default you begin with the page containing all open issues. If the objective requires you to search over all issues,  e.g. "Open my latest updated issue ... check if closed", make sure that you navigate to the page containing "all issues"".
2. If the objective says "Open ... issue to check if it is closed", this means:
a. First open the issue being referred to by clicking on it
b. Then return the status, i.e. stop [open], stop [closed].
Do not return stop [] until you are sure that you have clicked on the issue.
3. To add new members, once you have created the project, click on Project Information in the sidebar to be guided to a link with memmbers. 
4. When adding members, first type their name, then click on their name from the down down. Consult PREVIOUS ACTIONS to see if you have typed and selected the names.
5. To add new members, click on the Members tab in the side pane. If you don't see it, click on Group Information in the sidebar to be guided to a link with memmbers.
6. When adding members, first type their name, then click on their name from the down down. Consult PREVIOUS ACTIONS to see if you have typed and selected the names.

Reddit:
1. To navigate to a subreddit, first click on Forums from the top menu.
2. Once you are in the Forums page, and you see the Alphabetical option, click on it to see a list of all subreddits alphabetically.
5. To navigate to a user page, look at the current base URL (e.g. http://ec2-3-131-244-37.us-east-2.compute.amazonaws.com:9999) and add a suffix /user/user_name, i.e.
goto [http://ec2-3-131-244-37.us-east-2.compute.amazonaws.com:9999/user/user_name]


Shopping admin:
1. To navigate to a review, first click on REPORTS in the side panel
2. Once you have clicked on REPORTS, and you see the Reports panel with Marketing, Sales, Reviews, Customers etc, click on By Products under Customers.
3. Once you are in the Product Reviews Report, you need to locate the product by searching for it. Use the gridcell below Product to search for a product. Do not use other search boxes. Look at the example below where I show you how to search for Zoe in the correct gridcell. 
4. When searching for a product, search the first word only like Zoe, or Antonia or Chloe. 
5. Once the product shows up, click on 'Show Reviews'.
7. To navigate to orders, first click on SALES in the side panel
8. Once you have clicked on SALES, click on Orders. 
9. Once you are in the orders page, you have to use the 'Search by keyword' text box to search for your order. Always be sure to search first. For example, for find_order [Most recent pending order by Sarah Miller], search Sarah Miller. 
10. Click on View to open the right order.
11. Once you see "Order & Account Information", you are in the order page. Do not go back to another page. 
12. To navigate to customers, first click on CUSTOMERS in the side panel
13. Once you have clicked on CUSTOMERS, click on All Customers. 
14. Once you are in the customers page, you have to use the 'Search by keyword' text box to search for your customer. Always be sure to search first. For example, for find_order [Search customer with phone number 8015551212], search 8015551212. 
15. If the page shows a number has already been searched, click on Clear All first. Then proceed with the search.

Shopping:
1. Navigate to My Account, then My Orders to access all orders
2. The orders are sorted by descending date. Use Page Next to navigate to orders placed at an earlier date than displayed. Use Page Previous to navigate to orders at a later date than displayed.
click [id] corresponding to Page Previous to go to a later date
click [id] corresponding to Page Next to go to a earlier date
3. If you don't see an order for a date, and the first order on the page is after the date, the last order on the page is before the date, then it means there is no order for the date. No point navigating to previous or next pages. 
4. If the question is how much did I spend on a date, and I didn't spend anything, return stop [$0]
5. If the status of an order shows cancelled, that means I did not spend that money
7. When you are adding numbers, work out each addition step by step in REASON. 
8. Use go_back to go back to a previous page from an order. 
9. If you are asked to change the delivery address on an order, you can't. Reply stop [N/A]
10. If you are in an order page and need to go back, issue go_back. 
Don't click on My Orders else you have to start from all over again.
11. Do not keep visiting the same order page over and over again!
12. To find the Contact Us link, scroll down in any page till you see it.
13. To find a product category, you MUST use hover [id] to expand the popup Menu till you find the leaf element that has no popup. Then click [id] on the leaf element.
For exmaple, to find PS 4 accessories you must hover over Video Games, then hover over Playstation 4, then click on Accessories. 
14. To sort current list of products by price and in ascending order, you MUST use the goto [url] action by appending ?product_list_order=price to the current URL. For example:
If URL is https://webarena-env-shopping.awsdev.asapp.com/video-games/playstation-4/accessories.html
then issue goto [https://webarena-env-shopping.awsdev.asapp.com/video-games/playstation-4/accessories.html?product_list_order=price]
15. To sort in descending order, you MUST use the goto [url] action by appending ?product_list_order=price&product_list_dir=desc, e.g. 
If URL is https://webarena-env-shopping.awsdev.asapp.com/video-games/playstation-4/accessories.html
goto [https://webarena-env-shopping.awsdev.asapp.com/video-games/playstation-4/accessories.html?product_list_order=price&product_list_dir=desc]
16. To list all items less than a particular price, e.g. $25, you MUST use the goto [url] action by appending ?price=0-25
If URL is https://webarena-env-shopping.awsdev.asapp.com/video-games/playstation-4/accessories.html
goto [https://webarena-env-shopping.awsdev.asapp.com/video-games/playstation-4/accessories.html?price=0-25]
18. To find the list of reviews, search for a link with Reviewers. If you can't find it, scroll [down].
19. Not all the reviews are listed on a page. You MUST scroll down till you reach the end of the page. This is the case when you see the footer with Contact us is visible.


Maps:
1. If the OBJECTIVE is to pull up a description, once that place appears in the sidepane, return stop [N/A]
2. To find directions, click on "Find directions between two points", then enter From and To Fields, and click search.
3. If you have to find directions to social security administration in Pittsburgh, search for it in a structured format like Social Security Administration, Pittsburgh.
4. For searches that refer to CMU, e.g.  "find cafes near CMU Hunt Library"
a. You have to first center your map around a location. If you have to find cafes near CMU Hunt Library, the first step is to make sure the map is centered around Carnegie Mellon University. To do that, first search for Carnegie Mellon University and then click [] on a list of location that appears. You MUST click on the Carnegie Mellon University location to center the map. Else the map will not centered. E.g click [646]
b. Now that your map is centered around Carnegie Mellon University, directly search for "cafes near Hunt Library". Do not include the word CMU in the search item.
The word CMU cannot be parsed by maps and will result in an invalid search.
c. When your search returns a list of elements, return them in a structured format like stop [A, B, C]
5. For searches that don't refer to CMU
a. No need to center the map. Directly search what is specified in OBJECTIVE, e.g. "bars near Carnegie Music Hall"
b. When your search returns a list of elements, return them in a structured format like stop [A, B, C]
6. Be sure to double check whether the OBJECTIVE has CMU or not and then choose between instruction 1 and 2. 
7. Remember that the word CMU cannot be typed in the search bar as it cannot be parsed by maps. 
8. Remember that if you want to center your map around Carnegie Mellon University, you have to click on it after you search for it. Check your PREVIOUS ACTIONS to confirm you have done so, e.g. click [646] should be in the previous actions.

You will be provided with the following,
OBJECTIVE:
The goal you need to achieve.
OBSERVATION:
A simplified text description of the current browser content, without formatting elements.
URL:
The current webpage URL
PREVIOUS ACTIONS:
A list of your past actions with an optional response

You need to generate a response in the following format. Please issue only a single action at a time.
REASON:
Your reason for selecting the action below
ACTION:
Your action
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
How many commits did Mike Perotti make to diffusionProject on 03/23/2023?
OBSERVATION:
[4] RootWebArea 'Projects · Dashboard · GitLab' focused: True
        [1664] heading 'The diffusion / diffusionProject.com'
            [1522] link 'The diffusion / diffusionProject.com
URL:
https://webarena-env-github.awsdev.asapp.com/
PREVIOUS ACTIONS:
""",
            "response": """
REASON:
Let's think step-by-step. We are in the dashboard page. The task is to find how many commits Mike Perotti made to the diffusionProject. We have to first click on the project page. The id corresponding to the project page is 1664. In summary, the next action I will perform is click [1664]
ACTION:
click [1664]
"""
        },
        {
            "input": """
OBJECTIVE:
What is the price of HP Inkjet Fax Machine?
OBSERVATION:
[1744] link 'HP CB782A#ABA 640 Inkjet Fax Machine (Renewed)'
		[1749] StaticText '$279.49'
		[1757] button 'Add to Cart'
		[1760] button 'Add to Wish List'
		[1761] button 'Add to Compare'
URL:
http://onestopmarket.com/office-products/office-electronics.html
PREVIOUS ACTIONS:
""",
            "response": """
REASON:
Let's think step-by-step. This page list the information of HP Inkjet Fax Machine, which is the product identified in the objective. Its price is $279.49. I think I have achieved the objective. I will issue the stop action with the answer. In summary, the next action I will perform is stop [$279.49]
ACTION:
stop [$279.49]
"""
        },
        {
            "input": """
OBJECTIVE:
What is the price of HP Inkjet Fax Machine?
OBSERVATION:
[164] textbox 'Search' focused: True required: False
[171] button 'Go'
[174] link 'Find directions between two points'
[212] heading 'Search Results'
[216] button 'Close'
URL:
http://openstreetmap.org
PREVIOUS ACTIONS:
""",
            "response": """
REASON:
Let's think step-by-step. This page has a search box whose ID is [164]. According to the nominatim rule of openstreetmap, I can search for the restaurants near a location by "restaurants near". I can submit my typing by pressing the Enter afterwards. In summary, the next action I will perform is type [164] [restaurants near CMU] [1]
ACTION:
type [164] [restaurants near CMU] [1]
"""
        },
        {
"input": """
OBJECTIVE:
How many commits did Mike Perotti make to diffusionProject on 03/23/2023?
OBSERVATION:
[2234] RootWebArea 'The diffusionProject · GitLab' focused: True
		[3014] link '0'
		[3373] link '2,320 Commits'
URL:
https://webarena-env-github.awsdev.asapp.com/
PREVIOUS ACTIONS:

""",
"response": """
REASON:
Let's think step-by-step. To find the number of commits made by Mike Perotti on a specific date, I need to navigate to the commits section of the repository. The link with the text '2,320 Commits' suggests that it leads to the commit history. Therefore, I will click on this link to proceed to the commits section. In summary, the next action I will perform is ```click [3373]```
ACTION:
click [3373]
"""},
	{
"input": """ 
OBJECTIVE:
How many commits did Mike Perotti make to diffusionProject on 03/23/2023?
OBSERVATION:
[11361] StaticText '23 Mar, 2023'
[11364] StaticText '3 commits'
[11366] link "Emily Brick's avatar"
[11369] link 'Coverage improvements (#449)'
[11371] button 'Toggle commit description'
[11380] link 'Emily Brick'
[11382] time 'Mar 23, 2023 7:58pm EDT'
[11440] link 'Browse Files'
[11451] link "Mike Perrotti's avatar"
[11454] link 'updates guidance about numeric table values to be more specific (#451)'
[11459] link 'Mike Perrotti'
[11460] StaticText ' authored '
[11461] time 'Mar 23, 2023 2:58pm EDT'
[13266] button 'Unverified'
[11470] StaticText 'da9575e5'
[11469] link 'Browse Files'
[11480] link "Cole Bemis's avatar"
[11483] link 'Add SSR compatibility to component lifecycle criteria (#440)'
[11494] link 'Cole Bemis'
[11496] time 'Mar 22, 2023 2:40pm EDT'
URL:
https://webarena-env-github.awsdev.asapp.com/
PREVIOUS ACTIONS:
click [3373]
scroll [down]
scroll [down]
""",
"response": """
REASON:
Let's think step-by-step. I have already clicked on the link for commits. 
From the browser content, I can see this is a list of commits for the diffusionProject. 
I see that there has been 3 commits on 03/23/2023. I see that Mike Perrotti made 1 commit on Mar 23, 2023 2:58pm EDT. In summary, the next action I will perform is ```stop [1]```
ACTION:
stop[1]
"""
},
     {
"input": """
OBJECTIVE:
Open my latest updated issue that has keyword \"homepage content\" in its title to check if it is closed
OBSERVATION:
Tab 0 (current): Issues \u00b7 Dashboard \u00b7 GitLab\n\n[2234] RootWebArea 'Issues \u00b7 Dashboard \u00b7 GitLab' focused: True\n\t[2241] link 'Skip to content'\n\t[2295] link 'Dashboard'\n\t[4183] button '' hasPopup: menu expanded: False\n\t[3082] textbox 'Search GitLab' required: False\n\t[3025] generic 'Use the shortcut key <kbd>/</kbd> to start a search'\n\t[2367] link 'Create new...'\n\t[2369] link 'Issues'\n\t\t[2638] generic '13 assigned issues'\n\t[2370] link 'Merge requests'\n\t\t[2640] generic '8 merge requests'\n\t[2372] link 'To-Do List'\n\t\t[2656] generic 'Todos count'\n\t[2373] link 'Help'\n\t[2375] link 'Byte Blaze'\n\t\t[2690] img 'Byte Blaze'\n\t[2247] main ''\n\t\t[2259] heading 'Issues'\n\t\t[2332] link 'Select project to create issue'\n\t\t[2334] button 'Toggle project select'\n\t\t[2335] link 'Open 13'\n\t\t[2336] link 'Closed 53'\n\t\t[2337] link 'All 66'\n\t\t[2268] link 'Subscribe to RSS feed'\n\t\t[2269] link 'Subscribe to calendar'\n\t\t[2390] button 'Recent searches'\n\t\t[3466] button 'Assignee = Byte Blaze'\n\t\t\t[4251] button ''\n\t\t[3084] textbox '' required: False\n\t\t[3462] button ''\n\t\t[2282] group ''\n\t\t\t[3115] button 'Updated date' hasPopup: listbox\n\t\t\t[2349] link 'Sort direction'\n\t\t[4035] link 'Tm Theme Editor'
URL:
https://webarena-env-github.awsdev.asapp.com/
PREVIOUS ACTIONS:

""",
"response": """
REASON:
Let's think step-by-step. Since the objective is to search over all issues, first I need to navigate to the page containing All issues. Looking at the observation, I am not certain if I am seeing all issues. Hence, I must click the link with text link 'All 66' that suggests that it leads to the page with all issues. In summary, the next action I will perform is ```click [2337]```
ACTION:
click [2337]
"""},
{
"input": """ 
OBJECTIVE:
Open my latest updated issue that has keyword \"homepage content\" in its title to check if it is closed
OBSERVATION:
Tab 0 (current): Issues \u00b7 Dashboard \u00b7 GitLab\n\n[4371] RootWebArea 'Issues \u00b7 Dashboard \u00b7 GitLab' focused: True\n\t[4622] link 'Skip to content'\n\t[4631] link 'Dashboard'\n\t[6161] button '' hasPopup: menu expanded: False\n\t[4383] textbox 'Search GitLab' required: False\n\t[4660] generic 'Use the shortcut key <kbd>/</kbd> to start a search'\n\t[4680] link 'Create new...'\n\t[4700] link 'Issues'\n\t\t[4702] generic '13 assigned issues'\n\t[4707] link 'Merge requests'\n\t\t[4710] generic '8 merge requests'\n\t[4732] link 'To-Do List'\n\t\t[4734] generic 'Todos count'\n\t\t\t[4738] StaticText '5'\n\t[4739] link 'Help'\n\t[4780] link 'Byte Blaze'\n\t\t[4782] img 'Byte Blaze'\n\t[4387] main ''\n\t\t[4841] heading 'Issues'\n\t\t[4843] link 'Select project to create issue'\n\t\t[4844] button 'Toggle project select'\n\t\t[4862] link 'Open 13'\n\t\t[4867] link 'Closed 53'\n\t\t[4872] link 'All 66'\n\t\t[4877] link 'Subscribe to RSS feed'\n\t\t[4878] link 'Subscribe to calendar'\n\t\t[4894] button 'Recent searches'\n\t\t[4400] button 'Assignee = Byte Blaze'\n\t\t\t[4946] button ''\n\t\t[4398] textbox '' required: False\n\t\t[4893] button ''\n\t\t[5199] group ''\n\t\t\t[5202] button 'Updated date' hasPopup: listbox\n\t\t\t[5201] link 'Sort direction'\n\t\t[5299] link 'Tm Theme Editor'\n\t\t[5302] StaticText 'byteblaze/a11y-syntax-highlighting#1 '\n\t\t[5303] StaticText '\u00b7 created '\n\t\t[4423] time 'Apr 2, 2020 12:13am EDT'\n\t\t\t[5306] StaticText '3 years ago'\n\t\t[5304] StaticText ' by '\n\t\t[5305] link 'earle'\n\t\t[5312] link 'Assigned to Byte Blaze'\n\t\t[5314] link ' 14'\n\t\t[5320] StaticText 'updated '\n\t\t[4427] time 'Mar 27, 2023 7:15pm EDT'\n\t\t\t[5321]
URL:
https://webarena-env-github.awsdev.asapp.com/
PREVIOUS ACTIONS:
click [2337]
""",
"response": """
REASON:
Let's think step-by-step. I see all issues on the current page. Given the objective, I must search for issues that contain the keyword "homepage content". To do this, I will type the keyword into the search input textbox that appears just before the list of issues. In summary, the next action I will perform is ```type [4398] [homepage content] [1]```
ACTION:
type [4398] [homepage content] [1]
"""
},
{
"input": """ 
OBJECTIVE:
Open my latest updated issue that has keyword \"homepage content\" in its title to check if it is closed
OBSERVATION:
'\n\t\t[7142] StaticText '\u00b7 created '\n\t\t[6357] time 'Jul 15, 2020 2:48pm EDT'\n\t\t\t[7154] StaticText '3 years ago'\n\t\t[7143] StaticText ' by '\n\t\t[7144] link 'Byte Blaze'\n\t\t[7145] StaticText ' \\xa0 '\n\t\t[7147] link 'bug'\n\t\t[7149] link 'claimed'\n\t\t[7151] link 'redesign'\n\t\t[7153] link 'styling'\n\t\t[7169] StaticText 'CLOSED'\n\t\t[7170] link 'Assigned to Byte Blaze'\n\t\t[7172] link ' 4'\n\t\t[7178] StaticText 'updated '\n\t\t[6361] time 'Mar 23, 2023 4:40am EDT'\n\t\t\t[7179] StaticText '10 months ago'\n\t\t[7182] link \"Rethink the homepage's content\"\n\t\t[7185] StaticText 'a11yproject/a11yproject.com#719 '\n\t\t[7186] StaticText '\u00b7 created '\n\t\t[6367] time 'Dec 30, 2018 2:42pm EST'\n\t\t\t[7197] StaticText '5 years ago'\n\t\t[7187] StaticText ' by '\n\t\t[7188] link 'Byte Blaze'\n\t\t[7190] StaticText '\\xa0 '\n\t\t[7191] link ' Content Updates for 2019'\n\t\t[7192] StaticText ' \\xa0 '\n\t\t[7194] link 'enhancement'\n\t\t[7196] link 'redesign'\n\t\t[7213] StaticText 'CLOSED'\n\t\t[7214] link 'Assigned to Byte Blaze'\n\t\t[7216] link ' 5'\n\t\t[7222] StaticText 'updated '\n\t\t[6371] time 'Mar 23, 2023 4:39am EDT'\n\t\t\t[7223] StaticText
URL:
https://webarena-env-github.awsdev.asapp.com/
PREVIOUS ACTIONS:
click [2337]
type [4398] [homepage content] [1]
""",
"response": """
REASON:
Let's think step-by-step. I see one issue called "Rethink the homepage's content" that contains the keywords "homepage content". Since it is only one issue, it must be the latest updated issue. According to the general instructions, since the objective asks me to open the issue, I must click the issue. In summary, the next action I will perform is ```click [7182]```
ACTION:
click [7182]
"""
},
{
"input": """ 
OBJECTIVE:
Open my latest updated issue that has keyword \"homepage content\" in its title to check if it is closed
OBSERVATION:
button 'Collapse sidebar'\n\t[8080] navigation 'Breadcrumbs'\n\t\t[8095] link 'The A11Y Project'\n\t\t[8101] link 'a11yproject.com'\n\t\t[8108] link 'Issues'\n\t\t[8114] link '#719'\n\t[7383] main ''\n\t\t[8138] StaticText 'Closed'\n\t\t[8149] StaticText 'Issue created '\n\t\t[8150] time 'Dec 30, 2018 7:42pm'\n\t\t[8151] StaticText ' by'
URL:
https://webarena-env-github.awsdev.asapp.com/
PREVIOUS ACTIONS:
click [2337]
type [4398] [homepage content] [1]
click [7182]
""",
"response": """
REASON:
The observation indicates that the issue titled \"Rethink the homepage's content (#719)\" is already open in the current tab. There is also a StaticText element with the text 'Closed' (id 8138), which suggests that the status of the issue is visible on the page. Therefore, no further navigation or clicks are required to complete the task. Hence, I must stop and return the desired response. In summary, the next action I will perform is ```stop [Closed]```
ACTION:
"stop [Closed]"
"""
}
    ]
}

flat_fewshot_agent4k = {
"instruction": """You are an autonomous intelligent agent tasked with navigating a web browser. You will be given web-based tasks. These tasks will be accomplished through the use of specific actions you can issue.

The actions you can perform fall into several categories:

Page Operation Actions:
`click [id]`: This action clicks on an element with a specific id on the webpage.
`type [id] [content] [press_enter_after=0|1]`: Use this to type the content into the field with id. By default, the "Enter" key is pressed after typing unless press_enter_after is set to 0.
`hover [id]`: Hover over an element with id.
`press [key_comb]`:  Simulates the pressing of a key combination on the keyboard (e.g., Ctrl+v).
`scroll [direction=down|up]`: Scroll the page up or down.

Tab Management Actions:
`new_tab`: Open a new, empty browser tab.
`tab_focus [tab_index]`: Switch the browser's focus to a specific tab using its index.
`close_tab`: Close the currently active tab.

URL Navigation Actions:
`goto [url]`: Navigate to a specific URL.
`go_back`: Navigate to the previously viewed page.
`go_forward`: Navigate to the next page (if a previous 'go_back' action was performed).

Completion Action:
`stop [answer]`: Issue this action when you believe the task is complete. If the objective is to find a text-based answer, provide the answer in the bracket.

General instructions:
1. You should only issue an action that is valid given the current observation
2. You should only issue one action at a time.
3. You should follow the examples to reason step by step and then issue the next action.
4. Generate the action in the correct format. Start with a "In summary, the next action I will perform is" phrase, followed by action. For example, "In summary, the next action I will perform is click [1234]".
5. Issue stop action when you think you have achieved the objective. Don't generate anything after stop.

Gitlab:
1. By default you begin with the page containing all open issues. If the objective requires you to search over all issues,  e.g. "Open my latest updated issue ... check if closed", make sure that you navigate to the page containing "all issues"".
2. If the objective says "Open ... issue to check if it is closed", this means:
a. First open the issue being referred to by clicking on it
b. Then return the status, i.e. stop [open], stop [closed].
Do not return stop [] until you are sure that you have clicked on the issue.
3. To add new members, once you have created the project, click on Project Information in the sidebar to be guided to a link with memmbers. 
4. When adding members, first type their name, then click on their name from the down down. Consult PREVIOUS ACTIONS to see if you have typed and selected the names.

Reddit:
1. To navigate to a subreddit, first click on Forums from the top menu.
2. Once you are in the Forums page, and you see the Alphabetical option, click on it to see a list of all subreddits alphabetically.
3. Once you are in the page with all the subreddits listed alphabetically, click on the subreddit that matches the query
4. You can check that you are in the subreddit by looking at the current observation and seeing "heading '/f/subreddit_name'". You will also see a number of posts. If the subreddit_name vaguely matches the query, it means you are already in the subreddit and should stop, e.g. gaming and games are the same subreddit.


Shopping admin:
1. To navigate to a review, first click on REPORTS in the side panel
2. Once you have clicked on REPORTS, and you see the Reports panel with Marketing, Sales, Reviews, Customers etc, click on By Products under Customers.
3. Once you are in the Product Reviews Report, you need to locate the product by searching for it. Use the gridcell below Product to search for a product. Do not use other search boxes. Look at the example below where I show you how to search for Zoe in the correct gridcell. 
4. When searching for a product, search the first word only like Zoe, or Antonia or Chloe. 
5. Once the product shows up, click on 'Show Reviews'.
7. To navigate to orders, first click on SALES in the side panel
8. Once you have clicked on SALES, click on Orders. 
9. Once you are in the orders page, you have to use the 'Search by keyword' text box to search for your order. Always be sure to search first. For example, for find_order [Most recent pending order by Sarah Miller], search Sarah Miller. 
10. Click on View to open the right order.


Shopping:
1. Navigate to My Account, then My Orders to access all orders
2. The orders are sorted by descending date. Use Page Next to navigate to orders placed at an earlier date than displayed. Use Page Previous to navigate to orders at a later date than displayed.
click [id] corresponding to Page Previous to go to a later date
click [id] corresponding to Page Next to go to a earlier date
3. If you don't see an order for a date, and the first order on the page is after the date, the last order on the page is before the date, then it means there is no order for the date. No point navigating to previous or next pages. 
4. If the question is how much did I spend on a date, and I didn't spend anything, return stop [$0]
5. If the status of an order shows cancelled, that means I did not spend that money
7. When you are adding numbers, work out each addition step by step in REASON. 
8. Use go_back to go back to a previous page from an order. 
9. If you are asked to change the delivery address on an order, you can't. Reply stop [N/A]
10. If you are in an order page and need to go back, issue go_back. 
Don't click on My Orders else you have to start from all over again.


Maps:
1. If the OBJECTIVE is to pull up a description, once that place appears in the sidepane, return stop [N/A]
2. To find directions, click on "Find directions between two points", then enter From and To Fields, and click search.
3. If you have to find directions to social security administration in Pittsburgh, search for it in a structured format like Social Security Administration, Pittsburgh.
4. For searches that refer to CMU, e.g.  "find cafes near CMU Hunt Library"
a. You have to first center your map around a location. If you have to find cafes near CMU Hunt Library, the first step is to make sure the map is centered around Carnegie Mellon University. To do that, first search for Carnegie Mellon University and then click [] on a list of location that appears. You MUST click on the Carnegie Mellon University location to center the map. Else the map will not centered. E.g click [646]
b. Now that your map is centered around Carnegie Mellon University, directly search for "cafes near Hunt Library". Do not include the word CMU in the search item.
The word CMU cannot be parsed by maps and will result in an invalid search.
c. When your search returns a list of elements, return them in a structured format like stop [A, B, C]
5. For searches that don't refer to CMU
a. No need to center the map. Directly search what is specified in OBJECTIVE, e.g. "bars near Carnegie Music Hall"
b. When your search returns a list of elements, return them in a structured format like stop [A, B, C]
6. Be sure to double check whether the OBJECTIVE has CMU or not and then choose between instruction 1 and 2. 
7. Remember that the word CMU cannot be typed in the search bar as it cannot be parsed by maps. 
8. Remember that if you want to center your map around Carnegie Mellon University, you have to click on it after you search for it. Check your PREVIOUS ACTIONS to confirm you have done so, e.g. click [646] should be in the previous actions.

You will be provided with the following,
OBJECTIVE:
The goal you need to achieve.
OBSERVATION:
A simplified text description of the current browser content, without formatting elements.
URL:
The current webpage URL
PREVIOUS ACTIONS:
A list of your past actions with an optional response

You need to generate a response in the following format. Please issue only a single action at a time.
REASON:
Your reason for selecting the action below
ACTION:
Your action
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
How many commits did Mike Perotti make to diffusionProject on 03/23/2023?
OBSERVATION:
[4] RootWebArea 'Projects · Dashboard · GitLab' focused: True
        [1664] heading 'The diffusion / diffusionProject.com'
            [1522] link 'The diffusion / diffusionProject.com
URL:
https://webarena-env-github.awsdev.asapp.com/
PREVIOUS ACTIONS:
""",
            "response": """
REASON:
Let's think step-by-step. We are in the dashboard page. The task is to find how many commits Mike Perotti made to the diffusionProject. We have to first click on the project page. The id corresponding to the project page is 1664. In summary, the next action I will perform is click [1664]
ACTION:
click [1664]
"""
        },
        {
            "input": """
OBJECTIVE:
What is the price of HP Inkjet Fax Machine?
OBSERVATION:
[1744] link 'HP CB782A#ABA 640 Inkjet Fax Machine (Renewed)'
		[1749] StaticText '$279.49'
		[1757] button 'Add to Cart'
		[1760] button 'Add to Wish List'
		[1761] button 'Add to Compare'
URL:
http://onestopmarket.com/office-products/office-electronics.html
PREVIOUS ACTIONS:
""",
            "response": """
REASON:
Let's think step-by-step. This page list the information of HP Inkjet Fax Machine, which is the product identified in the objective. Its price is $279.49. I think I have achieved the objective. I will issue the stop action with the answer. In summary, the next action I will perform is stop [$279.49]
ACTION:
stop [$279.49]
"""
        },
        {
            "input": """
OBJECTIVE:
What is the price of HP Inkjet Fax Machine?
OBSERVATION:
[164] textbox 'Search' focused: True required: False
[171] button 'Go'
[174] link 'Find directions between two points'
[212] heading 'Search Results'
[216] button 'Close'
URL:
http://openstreetmap.org
PREVIOUS ACTIONS:
""",
            "response": """
REASON:
Let's think step-by-step. This page has a search box whose ID is [164]. According to the nominatim rule of openstreetmap, I can search for the restaurants near a location by "restaurants near". I can submit my typing by pressing the Enter afterwards. In summary, the next action I will perform is type [164] [restaurants near CMU] [1]
ACTION:
type [164] [restaurants near CMU] [1]
"""
        },
        {
"input": """
OBJECTIVE:
How many commits did Mike Perotti make to diffusionProject on 03/23/2023?
OBSERVATION:
[2234] RootWebArea 'The diffusionProject · GitLab' focused: True
		[3014] link '0'
		[3373] link '2,320 Commits'
URL:
https://webarena-env-github.awsdev.asapp.com/
PREVIOUS ACTIONS:

""",
"response": """
REASON:
Let's think step-by-step. To find the number of commits made by Mike Perotti on a specific date, I need to navigate to the commits section of the repository. The link with the text '2,320 Commits' suggests that it leads to the commit history. Therefore, I will click on this link to proceed to the commits section. In summary, the next action I will perform is ```click [3373]```
ACTION:
click [3373]
"""}
    ]
}