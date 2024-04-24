from time import sleep
import pandas as pd
import re

from webagents_step.parser import (
    heihei_web_parser,
    playwright_parser_nat,
    playwright_parser_webarena,
)
from webagents_step.environment.env import WebEnvironment


class LiveWebEnvironmentWrapper(WebEnvironment):
    def __init__(
        self,
        url=None,
        objective=None,
        parser_type="heihei",
        observation_type="text",
        text_observation_type="accesibility_tree",
        max_browser_rows=1000,
        max_steps=50,
        step_delay=2,
        headless=False,
    ):
        self.url = url
        self.objective = objective
        self.headless = headless
        self.parser_type = parser_type
        self.observation_type = observation_type
        self.text_observation_type = text_observation_type
        self.max_browser_rows = max_browser_rows
        self.max_steps = max_steps

        self.steps = 0
        self.is_done = False
        self.parse_timeout = 5
        self.step_delay = step_delay
        self.response = ""

    async def init_parser(self):
        if self.parser_type == "heihei":
            self.parser = heihei_web_parser.HeiHeiWebParser()
            await self.parser.init()
        elif self.parser_type == "playwright_webarena":
            self.parser = playwright_parser_webarena.PlaywrightParserWebArena(
                headless=self.headless,
                observation_type=self.observation_type,
                text_observation_type=self.text_observation_type,
            )
            self.parser.init()
        elif self.parser_type == "playwright_nat":
            self.parser = playwright_parser_nat.PlaywrightParserNat(
                headless=self.headless
            )
            await self.parser.init()
        else:
            raise NotImplementedError(f"{self.parser_type} not implemented.")

        if self.url is not None:
            await self.parser.go_to_page(self.url)
            self.clear_page_presets()
            await self.parser.parse_page()

    def clear_page_presets(self):
        pass

    async def reset(self):
        await self.close()
        await self.init_parser()

    async def close(self):
        await self.parser.close()

    async def observation(self, tab_id=None, format=None):
        format = self.text_observation_type if format is None else format
        if self.parser_type == "heihei":
            try:
                browser_content = await self.parser.parse_page(
                    format=format, tab_id=tab_id
                )
            except:
                sleep(self.parse_timeout)
                browser_content = await self.parser.parse_page(
                    format=format, tab_id=tab_id
                )
        else:
            browser_content = await self.parser.parse_page()

        if format not in ["htree", "html", "json"]:
            browser_content = [str(w) for w in browser_content]
            browser_content = browser_content[: self.max_browser_rows]
            browser_content = "\n".join(browser_content)

        return browser_content

    def get_log(self):
        return self.df_log

    def get_response(self):
        return self.response

    def get_url(self):
        return self.parser.get_url()

    async def execute_action(self, action):
        """
        Execute a given action based on the action type,
        - click [id]: Clicks an element based on the provided id.
        - type [id] [content]: Types the provided content into the element with the specified id.
        - goto [url]: Navigates to an existing tab at that URL
        - open [url]: Opens a new tab with provided URL
        - copy [content]: Copies content, but no-op action
        - stop [response]: Stops execution and optionally provides a response.
        """
        click_match = re.match(r"click \[(\S+)\]", action, re.IGNORECASE)
        type_match = re.match(r"type \[(\S+)\] \[(.+)\]", action, re.IGNORECASE)
        goto_match = re.match(r"goto \[(\S+)\]", action, re.IGNORECASE)
        open_match = re.match(r"open \[(\S+)\]", action, re.IGNORECASE)
        copy_match = re.match(r"copy \[(\S+)\]", action, re.IGNORECASE)
        stop_match = re.match(r"stop \[([^\]]*)\]", action, re.IGNORECASE)

        if click_match:
            id = click_match.group(1)
            if not id.isdigit():
                raise Exception("Id not a valid integer")
            await self.parser.click(int(id))

        elif type_match:
            id = type_match.group(1)
            content = type_match.group(2)
            if not id.isdigit():
                raise Exception("Id not a valid integer")
            await self.parser.type(int(id), content)

        elif goto_match:
            url = goto_match.group(1)
            tab_id, tab_url = await self.parser.get_tab_from_url(url)
            await self.parser.go_to_page(url)

        elif open_match:
            url = open_match.group(1)
            await self.parser.go_to_page(url)

        elif copy_match:
            pass

        elif stop_match:
            self.response = stop_match.group(1)
            self.is_done = True

        else:
            print(f"[execute_action] Error {action} not defined")

    async def step(self, action, delay=None):
        delay = self.step_delay if delay is None else delay

        if self.steps > self.max_steps:
            print(f"Steps {self.steps} exceeded maximum {self.max_steps}")
            self.is_done = True
            return

        print(f"[Step {self.steps+1}] {action}")
        try:
            await self.execute_action(action)
        except Exception as e:
            print(f"Error while executing action '{action}'. Details: {e}")

        sleep(delay)
        self.steps = self.steps + 1

        return {"done": self.is_done, "response": self.response}

    def done(self):
        return self.is_done
