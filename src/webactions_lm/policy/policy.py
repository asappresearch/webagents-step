class Policy():
    def __init__(self, env):
        self.env = env
        self.model_type = None
        self.prompt_library = None
        self.base_prompt = None
        self.prev_actions = []

    def act(self, **kwargs):
        is_success = False
        done = False
        while not done:
            is_success = True
        return is_success