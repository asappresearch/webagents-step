import openai
from time import sleep

def add_latest_state_to_prompt(prompt, context, url, browser_content, prev_actions):
    prompt = prompt.replace("{context}", context)
    prompt = prompt.replace("{url}", url)
    prompt = prompt.replace("{browser_content}", browser_content[:10000])
    prompt = prompt.replace("{previous_actions}", prev_actions)
    return prompt

def call_llm(prompt, model_type="gpt-3.5-turbo", delay=0.5, max_attempts=3, max_tokens=256):
    attempts = 0
    response = None
    action = "Do nothing."
    reason = None
    
    try: 
        while attempts < max_attempts:
            attempts = attempts + 1
            if delay:
                sleep(delay)
            if (model_type == "gpt-3.5-turbo"):
                response = openai.ChatCompletion.create(
                    model=model_type, messages=[{"role": "user", "content": prompt}],
                    temperature=0.3, top_p=1, n=3, max_tokens=max_tokens)
                response = response.choices[0].message.content.strip()
            elif (model_type == "gpt-4"):
                response = openai.ChatCompletion.create(
                    model=model_type, messages=[{"role": "user", "content": prompt}],
                    temperature=0.3, top_p=1, n=3, max_tokens=max_tokens)
                response = response.choices[0].message.content.strip()
            elif (model_type == "text-davinci-003"):
                response = openai.Completion.create(
                    model=model_type, prompt=prompt,
                    temperature=0.3, best_of=3, n=3, max_tokens=max_tokens)
                response = response.choices[0].text.strip()
            elif (model_type == "text-davinci-002"):
                response = openai.Completion.create(
                    model=model_type, prompt=prompt,
                    temperature=0.3, best_of=3, n=3, max_tokens=max_tokens)
                response = response.choices[0].text.strip()
            else:
                raise NotImplementedError(f"{model_type=}")
                
            if response:
                action_str = 'ACTION:\n'
                if "REASONING" in prompt and action_str in response:
                    # This means there is a reason
                    reason = response[:response.index(action_str)]
                    action = response[response.index(action_str) + len(action_str):]
                    break_str = '\n=='
                    if break_str in action:
                        action = action[:action.index(break_str)]
                elif "REASONING" in prompt and action_str not in response:
                    prompt = prompt + response + "\n" + action_str
                    continue
                elif "REASONING" not in prompt:
                    action = response
                
                return action, reason
    except Exception as e:
        print(f"Exception occurred: {e}")

    return action, reason


def call_generic_llm(prompt, model_type="gpt-3.5-turbo", delay=0.5, max_attempts=5, max_tokens=256):
    attempts = 0
    response = None
    while attempts < max_attempts:
        if delay:
            sleep(delay)
        if (model_type == "gpt-3.5-turbo"):
            response = openai.ChatCompletion.create(
                model=model_type, messages=[{"role": "user", "content": prompt}],
                temperature=0.6, top_p=1, n=3, max_tokens=max_tokens)
            response = response.choices[0].message.content.strip()
        elif (model_type == "gpt-4"):
            response = openai.ChatCompletion.create(
                model=model_type, messages=[{"role": "user", "content": prompt}],
                temperature=0.3, top_p=1, n=3, max_tokens=max_tokens)
            response = response.choices[0].message.content.strip()
        elif (model_type == "text-davinci-003"):
            response = openai.Completion.create(
                model=model_type, prompt=prompt,
                temperature=0.3, best_of=3, n=3, max_tokens=max_tokens)
            response = response.choices[0].text.strip()
        elif (model_type == "text-davinci-002"):
            response = openai.Completion.create(
                model=model_type, prompt=prompt,
                temperature=0.3, best_of=3, n=3, max_tokens=max_tokens)
            response = response.choices[0].text.strip()
        else:
            raise NotImplementedError(f"{model_type=}")
        return response
    
    return response