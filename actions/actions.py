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
import dateutil.parser


class ValidateBookingForm(FormValidationAction):

    @staticmethod
    def allowed_cities() -> List[Text] :
        return ["berlin", "munich", "frankfurt", "hamburg"]
    
    @staticmethod
    def allowed_rooms() -> List[Text]:
        return ["single", "double", "suit"]
    
    def name(self) -> Text:
        return "validate_booking_form"

    def validate_room_type(
        self,slot_value: Any,dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `room_type` value."""

        if slot_value.lower() not in self.allowed_rooms():
            dispatcher.utter_message(text=f"Currently, you can only book one of the following room types: {'/'.join(self.allowed_rooms())}")
            return {"room_type": None}
        dispatcher.utter_message(text=f"OK! You want to book a {slot_value} room.")
        return {"room_type": slot_value}
        
    def validate_city(self, slot_value: Any, dispatcher: CollectingDispatcher,tracker: Tracker,
                       domain: DomainDict) -> Dict[Text, Any]:
        """validate the city"""

        if slot_value.lower() not in self.allowed_cities():
            dispatcher.utter_message(text=f"the current available rooms are only located in those cities: {'/'.join(self.allowed_cities())}, \n Please choose one of them.") 
            return {"city":None}
        dispatcher.utter_message(text=f"OK! your reservation will be set in {slot_value}")
        return {"city":slot_value}
    
    def validate_time(self, slot_value: Any, dispatcher: CollectingDispatcher,tracker: Tracker,
                       domain: DomainDict) -> Dict[Text, Any]:
        """validate the time"""
        
        duckling_time = tracker.get_slot("time")
        
        if duckling_time is not None:
            if type(duckling_time) is dict:
                from_time = tracker.get_slot("time")["from"][:19]
                to_time = tracker.get_slot("time")["to"][:19]
            
                from_date = dateutil.parser.parse(from_time, dayfirst=True)
                formatted_from_date = from_date.strftime("%Y-%m-%d")
                formatted_from_timing = from_date.strftime("%H:%M")

                to_date = dateutil.parser.parse(to_time, dayfirst=True)
                formatted_to_date = to_date.strftime("%Y-%m-%d")
                formatted_to_timing = to_date.strftime("%H:%M")
                
                print(f"duckling_time: {type(duckling_time)}, value: {duckling_time}, from_time: {from_time}, to_time: {to_time}, ")
                print("/"*20)
                print(f"type of from_time is {type(from_time)} and its {from_time}..same goes for to_time")
                #dispatcher.utter_message("I got this time: " + time + ". This is the full date: " + humanDate)
        
                dispatcher.utter_message(text=f"OK! your reservation time will be set on the following date interval: \n from date: {formatted_from_date} at: {formatted_from_timing} \nto date: {formatted_to_date} at: {formatted_to_timing}")    
                    
                return {"time":duckling_time}            
        dispatcher.utter_message(text=f"please enter teh time correctly") 
        return {"time":None}
        
    