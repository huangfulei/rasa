
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-large")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-large")
step = 0


class CallDialoGPTModel(Action):
    """Call DialoGPT to get the answer"""

    def name(self) -> Text:
        return "call_dialoGPT_model"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        current_state = tracker.current_state()
        latest_message = current_state["latest_message"]["text"]
        # encode the new user input, add the eos_token and return a tensor in Pytorch
        new_user_input_ids = tokenizer.encode(
            latest_message + tokenizer.eos_token, return_tensors='pt')

        # append the new user input tokens to the chat history
        bot_input_ids = torch.cat(
            [chat_history_ids, new_user_input_ids], dim=-1) if step > 0 else new_user_input_ids

        # generated a response while limiting the total chat history to 1000 tokens,
        chat_history_ids = model.generate(
            bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)

        # pretty print last ouput tokens from bot
        print("DialoGPT: {}".format(tokenizer.decode(
            chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)))

        dispatcher.utter_message(text="DialoGPT: {}".format(tokenizer.decode(
            chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)))

        # Revert user message which led to fallback.
        return [UserUtteranceReverted()]
