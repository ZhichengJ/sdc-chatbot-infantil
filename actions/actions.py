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

dia = ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"]
mes = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]


# Gets audio en images for a new classification:
class ActionGetSample(Action):
   def name(self):
      return "action_get_sample"

   def run(self,
           dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      
      # Test sample:
      # id = "fuenlabrada_2020-05-02-15453015"
      # audio = "http://138.100.100.143/fuenlabrada/opendata/sounds_test/mayo/fuenlabrada_2020-05-02-15453015.wav"

      # Get json from the API with the id and sound of a detection:
      url = "http://138.100.100.143:3001/sonidos?policy=random"
      r = requests.get(url, headers=headers)
      decoded = json.loads(r.text)
      id = decoded["_id"]
      audio = decoded["Ruta"]

      # Extracting echo info
      index = decoded['_id'].find('_')
      estacion = decoded['_id'][:index]
      date = decoded['_id'][index+1:-4]
      dateTimeObj = datetime.strptime(date, '%Y-%m-%d-%H%M')
      hour = dateTimeObj.strftime("%H:%M")
      day = dateTimeObj.day
      weekday = dia[dateTimeObj.weekday()]
      month = mes[dateTimeObj.month]
      year = dateTimeObj.year
      date = weekday + ' ' + str(day) + " de " + month + " del " + str(year) + " a las " + str(hour)

      # Creates JSON message to send the sample files:
      new_sample =  {
         "sample": 
			   { 
               "id": id ,
               "audio": audio,
            }
		}
      dispatcher.utter_message(json_message = new_sample) #dispatcher.utter_message(text = "Hey there")#
      return[SlotSet("id",id), SlotSet("audio", audio),SlotSet("estacion", estacion.capitalize()), SlotSet("fecha",date)]

class ActionRepetirSonido(Action):
   def name(self):
      return "action_repetir_sonido"

   def run(self,
           dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      
      id = tracker.get_slot("id")
      audio = tracker.get_slot("audio")
      if (id != None and audio != None):
         # Creates JSON message to send the sample files:
         new_sample =  {
            "sample": 
               { 
                  "id": id ,
                  "audio": audio,
               }
         }
         dispatcher.utter_message(json_message = new_sample)
      return[]

# Sends the answers of the last classification:
class ActionSendClassification(Action):
   def name(self):
      return "action_send_classification"

   def run(self,
           dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      
      url = 'http://138.100.100.143:3001/clasificaciones/'
      query_Dict = {}
      eco = tracker.get_slot('id')
      nombre = 'chatbot-infantil'

      # Get the value of the slots with the answers:
      r1 = tracker.get_slot("respuesta1")
      r2 = tracker.get_slot("respuesta2")
      r3 = tracker.get_slot("respuesta3")

      # Creates query:
      query_Dict['_id'] = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
      query_Dict['idEco'] = eco
      query_Dict['Tipo'] = 'Sonido'
      query_Dict['Respuesta1'] = r1 
      query_Dict['Respuesta2'] = r2
      query_Dict['Respuesta3'] = r3

      r = requests.post(url, data=json.dumps(query_Dict), headers=headers)

      # Reset slots:


      # Creates JSON message to increase counter:
      new_clasification =  {
         "clasification": 
			   { 
               "new": "true"
            }
		}
      dispatcher.utter_message(json_message = new_clasification)

      return [SlotSet("respuesta1",None),SlotSet("respuesta2",None),SlotSet("respuesta3",None),SlotSet("id",None)]

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
class ActionSetDuracion(Action):
   def name(self):
      return "action_set_duracion"

   def run(self,
           dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

      respuesta = tracker.latest_message['intent'].get('name')
      if (respuesta == 'corto'):
         return [SlotSet("duracion", "corto"), SlotSet("respuesta1", "Menos de 1 segundo")]
      elif (respuesta == 'mediano'):
         return [SlotSet("duracion", "mediano"), SlotSet("respuesta1", "Entre 1 y 5 segundos")]
      elif (respuesta == 'largo'):
         return [SlotSet("duracion", "largo"), SlotSet("respuesta1", "Mas de 9 segundos")]

class ActionSetR2(Action):
   def name(self):
      return "action_set_r2"

   def run(self,
           dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

      respuesta = tracker.latest_message['intent'].get('name')
      if (respuesta == 'afirmar'):
         return [SlotSet("respuesta2", "Sí")]
      elif (respuesta == 'negar'):
         return [SlotSet("respuesta2", "No")]

class ActionSetR3(Action):
   def name(self):
      return "action_set_r3"

   def run(self,
           dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      
      respuesta = tracker.latest_message['intent'].get('name')
      if (respuesta == 'afirmar'):
         return [SlotSet("respuesta3", "Sí")]
      elif (respuesta == 'negar'):
         return [SlotSet("respuesta3", "No")]

class ActionP1True(Action):
   def name(self):
      return "action_p1_true"

   def run(self,
           dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      
      return [SlotSet("p1",True)]

class ActionP2True(Action):
   def name(self):
      return "action_p2_true"

   def run(self,
           dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      
      return [SlotSet("p2",True)]

class ActionP3True(Action):
   def name(self):
      return "action_p3_true"

   def run(self,
           dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      
      return [SlotSet("p3",True)]

class ActionP1False(Action):
   def name(self):
      return "action_p1_false"

   def run(self,
           dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      
      return [SlotSet("p1",False)]

class ActionP2False(Action):
   def name(self):
      return "action_p2_false"

   def run(self,
           dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      
      return [SlotSet("p2",False)]

class ActionP3False(Action):
   def name(self):
      return "action_p3_false"

   def run(self,
           dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      
      return [SlotSet("p3",False)]


class ActionMenuFalse(Action):
   def name(self):
      return "action_menu_false"

   def run(self,
           dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      
      return [SlotSet("menu",False)]

class ActionMenuTrue(Action):
   def name(self):
      return "action_menu_true"

   def run(self,
           dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      
      return [SlotSet("menu",True)]

class ActionSeguirFalse(Action):
   def name(self):
      return "action_seguir_false"

   def run(self,
           dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      
      return [SlotSet("seguir",False)]

class ActionSeguirTrue(Action):
   def name(self):
      return "action_seguir_true"

   def run(self,
           dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      
      return [SlotSet("seguir",True)]


class ActionDefaultFallback(Action):
    """Executes the fallback action and goes back to the previous state
    of the dialogue"""

    def name(self) -> Text:
        return "action_default_fallback"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message("Creo que no te he entendido, ¿podrías repetirlo de otra forma?")

        # Revert user message which led to fallback.
        return [UserUtteranceReverted()]
      
