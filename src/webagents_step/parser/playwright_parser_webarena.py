from sys import platform
from playwright.sync_api import sync_playwright
from browser_env.processors import TextObervationProcessor, ImageObservationProcessor


class PlaywrightParserWebArena:
    def __init__(
        self,
        headless=True,
        observation_type="text",
        text_observation_type="accessibility_tree",
        viewport_size={"width": 1280, "height": 1080},
        current_viewport_only=True,
    ):
        self.headless = headless
        self.viewport_size = viewport_size
        self.current_viewport_only = current_viewport_only
        self.observation_type = observation_type
        self.text_observation_type = text_observation_type

        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=self.headless)
        self.context = self.browser.new_context(
            viewport=self.viewport_size,
            device_scale_factor=1,
        )
        
        self.page = self.context.new_page()
        client = self.page.context.new_cdp_session(self.page)
        if (self.observation_type == "text") and (
            self.text_observation_type == "accessibility_tree"
        ):
            client.send("Accessibility.enable")
        self.page.client = client
        
        ## scratch ##
        # initialize with html string
        # self.page.goto(url if "://" in url else "http://" + url)
        # potentially later
        # self.page.goto("https://www.google.com", wait_until='networkidle')
        # print(self.page.accessibility.snapshot())
        # self.page = self.page.accessibility.snapshot()

        self.text_processor = TextObervationProcessor(
            observation_type=self.text_observation_type,
            current_viewport_only=self.current_viewport_only,
            viewport_size=self.viewport_size,
        )
        self.image_processor = ImageObservationProcessor(observation_type="image")
    
    def clear_page_presets():
        pass
    
    def observation_processor(self):
        if self.observation_type == "text":
            return self.text_processor
        elif self.observation_type == "image":
            return self.image_processor
        else:
            raise ValueError("Invalid observation type")

    def get_url(self):
        return self.page.url

    def go_to_page(self, url: str):
        self.page.goto(url if "://" in url else "http://" + url)

    def close(self):
        self.browser.close()
        self.playwright_context.stop()

    def click_xy(self, x: float, y: float) -> None:
        viewport_size = self.page.viewport_size
        self.page.mouse.click(x * viewport_size["width"], y * viewport_size["height"])

    def click(self, id: int) -> None:
        element_center = self.observation_processor().get_element_center(id)
        self.click_xy(element_center[0], element_center[1])

    def type(self, id: int, text: str, clear: bool = True):
        if clear:
            self.clear(id)
        self.click(id)
        self.page.keyboard.type(text)

    def clear(self, id: int) -> None:
        self.click(id)
        select_key = "Meta" if platform.startswith("darwin") else "Control"
        self.page.keyboard.down(select_key)
        self.page.keyboard.press("a")
        self.page.keyboard.up(select_key)
        self.page.keyboard.press("Backspace")

    def parse_page(self):
        observation = self.observation_processor().process(
            page=self.page, client=self.page.client
        )

        return observation
