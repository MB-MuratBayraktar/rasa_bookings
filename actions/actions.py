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


def clean_name(name):
    return "".join([c for c in name if c.isalpha()])

class ValidateBookingForm(FormValidationAction):

    def name(self) -> Text:
        return "validate_booking_form"

    @staticmethod
    def city_allowed() -> List[Text] :
        return ["berlin", "munich", "frankfurt", "hamburg"]
    
    @staticmethod
    def room_type_allowed() -> List[Text]:
        return ["single", "double", "suit"]
    
    
    def validate_first_name(self,slot_value: Any, dispatcher: CollectingDispatcher,
                      tracker: Tracker, domain: DomainDict) -> Dict[Text, Any]:
        
        name = clean_name(slot_value)

        if len(slot_value) == 0:
            dispatcher.utter_message(text=f"that's too short for a first name, I think you mis-spelled your name.")
            return {"first_name": None}
        else:
            dispatcher.utter_message(text=f"pleased to meet you {slot_value}")
            return {"first_name": name}
    
    def validate_last_name(self,slot_value : Any, dispatcher: CollectingDispatcher,
                      tracker: Tracker, domain: DomainDict) -> Dict[Text, Any]:
        
        last_name = clean_name(slot_value)
        reg_room_type = tracker.get_slot("room_type")

        if len(slot_value) ==0:
            dispatcher.utter_message(text=f"I think you mis-spelled your surname.")
            return {"last_name": None}
        else:
            reg_first_name = tracker.get_slot("first_name")
            if len(reg_first_name) + len(last_name) < 3: 
                dispatcher.utter_message(text="this is too short for a full name, i suspect a type. Restarting!")
                return {"first_name":None,"last_name":None}
            
            dispatcher.utter_message(text=f"Ok, successfuly registered your {reg_room_type} room under your name: {reg_first_name} {slot_value}.")    
            return {"last_name": slot_value}
    
    def validate_room_type(
        self,slot_value: Any,dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `room_type` value."""

        if slot_value.lower() not in self.room_type_allowed():
            dispatcher.utter_message(text=f"Currently, you can only book one of the following room types: {'/'.join(self.allowed_rooms())}")
            return {"room_type": None}
        else:
            dispatcher.utter_message(text=f"OK! You want to book a {slot_value} room.")
            return {"room_type": slot_value}
    
    def validate_num_visitors(
        self,slot_value: Any,dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `room_type` value."""
        visitors_number = int(slot_value)
        print(type(visitors_number))
        if visitors_number<1:
            dispatcher.utter_message(text=f"please enter a valid number of expected visitors")
            return {"num_visitors": None}
        else:
            dispatcher.utter_message(text=f"OK! the expected number of visitors is {slot_value}")
            return {"num_visitors": slot_value}
        
    def validate_city(self, slot_value: Any, dispatcher: CollectingDispatcher,tracker: Tracker,
                       domain: DomainDict) -> Dict[Text, Any]:
        """validate the city"""

        if slot_value.lower() not in self.city_allowed():
            dispatcher.utter_message(text=f"the current available rooms are only located in those cities: {'/'.join(self.allowed_cities())}, \n Please choose one of them.") 
            return {"city":None}
        else:
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
        else:         
            dispatcher.utter_message(text=f"please enter the time correctly") 
            return {"time":None}
            
    