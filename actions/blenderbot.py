
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

step = 0
tokenizer = AutoTokenizer.from_pretrained("facebook/blenderbot-3B")
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/blenderbot-3B")


class CallBlenderBot3BModel(Action):
    """Call Blenderbot3B to get the answer"""

    def name(self) -> Text:
        return "call_blenderbot_3B_model"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        current_state = tracker.current_state()
        latest_message = current_state["latest_message"]["text"]

        inputs = tokenizer([latest_message], return_tensors='pt')

        reply_ids = model.generate(**inputs)

        dispatcher.utter_message(text=tokenizer.batch_decode(
            reply_ids, skip_special_tokens=True)[0])

        # Revert user message which led to fallback.
        return [UserUtteranceReverted()]
