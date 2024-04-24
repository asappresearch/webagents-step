import re
import datetime

from miniwob.action import create_element_click_action, create_focus_and_type_action, create_coord_click_action

def parse_dom_browser_content(dom, ignore_tags=["tr", "td"], format='html', process_dates=False):
    """
    Parse dom observations into a browser action set
    """
    if format == "html":
        output = parse_dom_browser_content_html(
            dom, ignore_tags=ignore_tags, process_dates=process_dates)
    else:
        raise NotImplementedError

    return output


def parse_dom_browser_content_html(dom, ignore_tags, process_dates):
    action_set = []

    for node in dom:
        if node['tag'] in ignore_tags:
            continue
        attrs = f" id={node['ref']}"
        if len(node['text']) > 0:
            value = f" val={node['text']}"
        elif 'value' in node and (len(node['value']) > 0):
            value = f" val={node['value']}"
        else:
            value = f" val={node['id']}"
        action_set.append(f"<{node['tag']}{attrs}{value} />")

    if process_dates:
        action_set = parse_dates_table(action_set)

    return action_set


def parse_dates_table(action_set):
    action_set_text = "\n".join(action_set)
    if "val=ui-datepicker-div" not in action_set_text:
        return action_set

    pattern = r"\b(January|February|March|April|May|June|July|August|September|October|November|December)\b"
    month = re.findall(pattern, action_set_text)[0]  # month name
    month = datetime.datetime.strptime(month, '%B').month  # month number
    pattern = r"20[0-4][0-9]|2050"
    year = re.findall(pattern, action_set_text)[0]

    pattern = r'<a\s+id=(\d+)\s+val=(\d+)\s*/>'
    action_set_text = re.sub(
        pattern, lambda m: f'<a id={m.group(1)} val={month}/{int(m.group(2)):d}/{year} />', action_set_text)

    action_set = action_set_text.split("\n")

    return action_set
