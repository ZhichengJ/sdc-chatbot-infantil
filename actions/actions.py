# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from rasa_sdk.events import SlotSet
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
import json

""" Links of interest:
- Dispatcher: https://rasa.com/docs/action-server/sdk-dispatcher
"""
headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Access-Control-Allow-Origin':'*'}

# Gets audio en images for a new classification:
class ActionGetSample(Action):
   def name(self):
      return "action_get_sample"

   def run(self,
           dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      
      # Test sample:
      #id = "fuenlabrada_2020-05-02-15453015"
      #audio = "http://138.100.100.143/fuenlabrada/opendata/sounds_test/mayo/fuenlabrada_2020-05-02-15453015.wav"

      # Get json from the API with the id and sound of a detection:
      url = "http://138.100.100.143:3001/sonidos?policy=random"
      r = requests.get(url, headers=headers)
      decoded = json.loads(r.text)
      id = decoded["_id"]
      audio = decoded["Ruta"]

      # Set value to slots:
      SlotSet(key = "id", value = id)
      SlotSet(key = "audio", value = audio)

      # Creates JSON message to send the sample files:
      new_sample =  {
         "Sample": 
			   { 
               "id": id ,
               "audio": audio,
            }
		}
      return dispatcher.utter_message(json_message = new_sample) #dispatcher.utter_message(text = "Hey there")#


# Sends the answers of the last classification:
class ActionSendClassification(Action):
   def name(self):
      return "action_send_classification"

   def run(self,
           dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      
      # Get the value of the slots with the answers
      duracion = tracker.get_slot("duracion")
      corto_silencio = tracker.get_slot("corto_silencio")
      suena_igual = tracker.get_slot("suena_igual")

      # POST API: this code must be replaced with the call to our API
      new_classification =  {
         "classification": 
			   {
               "id": 1 ,
               "duracion": duracion,
               "corto_silencio": corto_silencio,
               "suena_igual": suena_igual,
            }
		}
      return dispatcher.utter_message(json_message = new_classification) 

## Set values slots:
class ActionSetCorto(Action):
   def name(self):
      return "action_set_r1_corto"

   def run(self,
           dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      return [SlotSet("duracion", "corto"), SlotSet("respuesta1", "Menos de 1 segundo")]

class ActionSetMediano(Action):
   def name(self):
      return "action_set_r1_mediano"

   def run(self,
           dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      return [SlotSet("duracion", "mediano"), SlotSet("respuesta1", "Entre 1 y 5 segundos")]

class ActionSetLargo(Action):
   def name(self):
      return "action_set_r1_largo"

   def run(self,
           dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      return [SlotSet("duracion", "largo"), SlotSet("respuesta1", "Mas de 9 segundos")]

class ActionSetCortoLargoSi(Action):
   def name(self):
      return "action_set_r2_si"

   def run(self,
           dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      return [SlotSet("respuesta2", "Sí")]

class ActionSetCortoLargoNo(Action):
   def name(self):
      return "action_set_r2_no"

   def run(self,
           dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      return [SlotSet("respuesta2", "No")]

class ActionSetIgualSi(Action):
   def name(self):
      return "action_set_r3_si"

   def run(self,
           dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      return [SlotSet("respuesta3", "Sí")]

class ActionSetIgualNo(Action):
   def name(self):
      return "action_set_r3_no"

   def run(self,
           dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      return [SlotSet("respuesta3", "No")]