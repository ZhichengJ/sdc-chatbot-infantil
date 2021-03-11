# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from rasa_sdk.events import SlotSet
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from datetime import datetime
import time
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
      id = "fuenlabrada_2020-05-02-15453015"
      audio = "http://138.100.100.143/fuenlabrada/opendata/sounds_test/mayo/fuenlabrada_2020-05-02-15453015.wav"

      # Get json from the API with the id and sound of a detection:
      #url = "http://138.100.100.143:3001/sonidos?policy=random"
      #r = requests.get(url, headers=headers)
      #decoded = json.loads(r.text)
      #id = decoded["_id"]
      #audio = decoded["Ruta"]

      # Set value to slots:
      SlotSet(key = "id", value = id)
      SlotSet(key = "audio", value = audio)

      # Creates JSON message to send the sample files:
      new_sample =  {
         "sample": 
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
      
      url = 'http://138.100.100.143:3001/clasificaciones/'
      query_dict = {}
      eco = tracker.get_slot('id')
      nombre = 'chatbot-infantil'

      # Get the value of the slots with the answers:
      r1 = tracker.get_slot("respuesta1")
      r2 = tracker.get_slot("respuesta2")
      r3 = tracker.get_slot("respuesta3")

      # Creates query:
      query_dict['_id'] = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
      query_dict['idEco'] = eco
      query_dict['Nombre'] = nombre
      query_dict['Respuesta1'] = r1 
      query_dict['Respuesta2'] = r2
      query_dict['Respuesta3'] = r3

      #r = requests.post(url, data=json.dumps(query_dict), headers=headers)

      # Reset slots:
      SlotSet(key = "id", value = None)
      SlotSet(key = "respuesta1", value = None)
      SlotSet(key = "respuesta2", value = None)
      SlotSet(key = "respuesta3", value = None)

      # Creates JSON message to increase counter:
      new_clasification =  {
         "clasification": 
			   { 
               "new": "true"
            }
		}
      return dispatcher.utter_message(json_message = new_clasification)


# Reproduce video in front:
class ActionPlayVideo(Action):
   def name(self):
      return "action_play_video"

   def run(self,
           dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      
      # Creates JSON message to trigger reproduction:
      video_trigger =  {
         "video": 
			   { 
               "tutorial": "true"
            }
		}
      return dispatcher.utter_message(json_message = video_trigger)


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