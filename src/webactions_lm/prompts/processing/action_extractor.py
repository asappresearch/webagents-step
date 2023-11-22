action_extractor = """

Your goal is to take as input a response generated from an action LLM, and parse action or a list of actions to follow a particular format.

The input will have a sentence, followed by \n delimters, then ACTION: followed by one or a list of actions. 

Your goal is to extract ONLY the actions.

Here are the instructions:
1. Actions are either CLICK <id> or TYPE <id< <text> or DONE
2. If a single action is predicted, return a string containing only that action
3. If a list of actions is predicted, return the list where every element is separated by \n. But make sure the list is not numbered.
4. If the response has CLICK #5, please convert that to CLICK 5 (there should be no #)

Here are some examples:

Example 1:
==================================================
INPUT:
# To achieve the goal of clicking the "Ok" button, we need to find the element with the id "6" in the current browser content.


ACTION:
CLICK 6
------------------
OUTPUT:
CLICK 6
==================================================

Example 2:
==================================================
INPUT:
# To achieve the context of clicking button ONE and then button TWO, we need to first click button ONE to activate it, and then click button TWO.

ACTION:

1. CLICK 4 (to activate button ONE)
2. CLICK 5 (to activate button TWO)

DONE
------------------
OUTPUT:
CLICK 4
CLICK 5
DONE
==================================================

Given the current input, respond with output.

==================================================
INPUT:
{input}
------------------
OUTPUT:
"""