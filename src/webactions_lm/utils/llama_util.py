import warnings
import torch
import re
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    AutoModelForSeq2SeqLM,
)

import ctranslate2
from peft import PeftModel, PeftConfig
from time import sleep
from webactions_lm.prompts.processing import action_extractor
from webactions_lm.utils.llm import call_generic_llm

warnings.simplefilter("ignore")

@torch.no_grad()
def generate_prediction(
    context,
    model,
    tokenizer,
    max_new_tokens,
    is_seq2seq=False,
    **kwargs,
    # num_beams,
    # do_sample,
    # no_repeat_ngram_size,
    # temperature,
    # top_k,
    # top_p,
):
    input_ids = tokenizer(
        context,
        return_tensors="pt",
        truncation=True,
        max_length=tokenizer.model_max_length - max_new_tokens,
    ).input_ids
    outputs = model.generate(
        input_ids=input_ids.cuda(),
        max_new_tokens=max_new_tokens,
        **kwargs,
    ).cpu()

    torch.cuda.empty_cache()
    if not is_seq2seq:
        outputs = outputs[:, input_ids.shape[1] :]

    prediction = [
        p.split(tokenizer.pad_token, 1)[0]
        for p in tokenizer.batch_decode(outputs, skip_special_tokens=True)
    ][0].strip()
        
    return prediction

def load_model(mpath, dtype, device="cuda", context_len=4096, is_seq2seq=False, ct2_mpath=None):
    if is_seq2seq:
        model_loader = AutoModelForSeq2SeqLM
    else:
        model_loader = AutoModelForCausalLM

    if dtype == "bf16":
        model = model_loader.from_pretrained(
            mpath,
            max_position_embeddings=context_len,
            low_cpu_mem_usage=True,
            torch_dtype=torch.bfloat16,
            device_map="balanced_low_0",
            # rope_scaling={"type": "dynamic", "factor": 2.0}
        )
    elif dtype == "4bit":
        model = model_loader.from_pretrained(
            mpath,
            max_position_embeddings=context_len,
            low_cpu_mem_usage=True,
            load_in_4bit=True,
            device_map="auto",
        )
    elif dtype == "4bit-optimized":
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16,
        )
        model = model_loader.from_pretrained(
            mpath,
            use_cache=True,
            device_map="auto",
            quantization_config=bnb_config,
            max_position_embeddings=context_len,
        )
    elif dtype == "8bit":
        model = model_loader.from_pretrained(
            mpath,
            max_position_embeddings=context_len,
            low_cpu_mem_usage=True,
            load_in_8bit=True,
            device_map="auto",
        )
    elif dtype == "ct2":
        assert ct2_mpath is not None
        model = ctranslate2.Generator(ct2_mpath, device=device)

    return model

def load_tokenizer(mpath, context_size):
    tokenizer = AutoTokenizer.from_pretrained(mpath)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.pad_token_id = tokenizer.eos_token_id
    tokenizer.model_max_length = context_size
    tokenizer.padding_side = "left"
    tokenizer.add_eos_token = True
    return tokenizer


def call_llm_llama(prompt, model, tokenizer, delay=0.5, max_attempts=3, max_tokens=128):
    attempts = 0
    response = None
    action = "Do nothing."
    reason = None
    
    try: 
        while attempts < max_attempts:
            attempts = attempts + 1
            if delay:
                sleep(delay)
            response = generate_prediction(context = prompt,
                            model = model,
                            tokenizer = tokenizer,
                            max_new_tokens = max_tokens)
            #print(response)
                
            if response:
                reason_pattern = r'^(.+?)\n+\s*ACTION:'
                reason_match = re.search(reason_pattern, response, re.MULTILINE | re.DOTALL)
                reason = reason_match.group(1) if reason_match else None
                
                prompt_action_extractor = getattr(action_extractor, "action_extractor")
                prompt_action_extractor = prompt_action_extractor.replace("{input}", response)
                action = call_generic_llm(prompt_action_extractor, model_type='text-davinci-003')
                
                # print(f"RESPONSE:{response}")
                # print(f"REASON:{reason}")
                # print(f"ACTION:{action}")
                # import pdb; pdb.set_trace()
                
                return action, reason
    except Exception as e:
        print(f"Exception occurred: {e}")

    return action, reason
