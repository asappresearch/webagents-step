import openai
import os
import tiktoken

from miniwob.environment import MiniWoBEnvironment

from webactions_lm.parser import miniwob_parsers, liveweb_parsers 

openai.api_key = os.environ.get('OPENAI_API_KEY')

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    encoding = tiktoken.encoding_for_model(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

for env_type in ["miniwob", "liveweb", "airlinecrm"]:
    encoding_name = "text-davinci-003"
    if (env_type == "miniwob"):
        task_name = "book-flight"
        miniwob_env = MiniWoBEnvironment(subdomain=task_name, wait_ms=300, render_mode="human")
        obs, info = miniwob_env.reset(0)
        dom_elements = obs['dom_elements']
        browser_content = "\n".join(miniwob_parsers.parse_dom_browser_content(dom_elements, ignore_tags=[], process_dates=True))
        print("Not compressed")
        print(num_tokens_from_string(browser_content, encoding_name))
        browser_content = "\n".join(miniwob_parsers.parse_dom_browser_content(dom_elements, process_dates=True))
        print("Compressed")
        print(num_tokens_from_string(browser_content, encoding_name))
    elif (env_type == "liveweb"):
        parser = liveweb_parsers.LiveWebParser()
        parser.go_to_page("https://www.united.com/")
        browser_content = "\n".join(parser.parse_page(compress=False))
        print("Not compressed")
        print(num_tokens_from_string(browser_content, encoding_name))
        browser_content = "\n".join(parser.parse_page(compress=True))
        print("Compressed")
        print(num_tokens_from_string(browser_content, encoding_name))
        parser.close()
    elif (env_type == "airlinecrm"):
        parser = liveweb_parsers.LiveWebParser()
        parser.go_to_page("https://airlinecrm.awsdev.anonymous.com/")
        import pdb; pdb.set_trace()
        browser_content = "\n".join(parser.parse_page(compress=False))
        print("Not compressed")
        print(num_tokens_from_string(browser_content, encoding_name))
        browser_content = "\n".join(parser.parse_page(compress=True))
        print("Compressed")
        print(num_tokens_from_string(browser_content, encoding_name))
        parser.close()