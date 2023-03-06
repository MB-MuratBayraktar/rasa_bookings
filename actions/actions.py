# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
from typing import Text, List, Any, Dict

from rasa_sdk import Tracker, FormValidationAction, Action
from rasa_sdk.events import EventType
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

ALLOWED_CITIES = ["berlin", "munich", "frankfurt", "hamburg"]
ALLOWED_ROOM_TYPES =["single", "double", "suit"]

class ValidateSimpleBookingForm(FormValidationAction):

    def name(self) -> Text:
        return "validate_simple_booking_form"

    def validate_room_type(
        self,slot_value: Any,dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `room_type` value."""

        if slot_value.lower() not in ALLOWED_ROOM_TYPES:
            dispatcher.utter_message(text=f"Currently, you can only book one of the following room types: single/double/suit")
            return {"room_type": None}
        dispatcher.utter_message(text=f"OK! You want to book a {slot_value} room.")
        return {"room_type": slot_value}
        
    def validate_city(self, slot_value: Any, dispatcher: CollectingDispatcher,tracker: Tracker,
                       domain: DomainDict) -> Dict[Text, Any]:
        """validate the city"""

        if slot_value.lower() not in ALLOWED_CITIES:
            dispatcher.utter_message(text=f"the current available rooms are only located in those cities: {'/'.join(ALLOWED_CITIES)}, \n Please choose one of them.") 
            return {"city":None}
        dispatcher.utter_message(text=f"OK! your reservation will be set in {slot_value}")
        return {"city":slot_value}
    
    def validate_time(self, slot_value: Any, dispatcher: CollectingDispatcher,tracker: Tracker,
                       domain: DomainDict) -> Dict[Text, Any]:
        """validate the time"""
        
        duckling_time = tracker.get_slot("time")
        if duckling_time is not None:
            dispatcher.utter_message(text=f"OK! your reservation time will be set on the following date: {slot_value}")    
            return {"time":duckling_time}
    
        dispatcher.utter_message(text=f"the current available rooms are only located in those cities: {'/'.join(ALLOWED_CITIES)}, \n Please choose one of them.") 
        return {"time":None}
        
    