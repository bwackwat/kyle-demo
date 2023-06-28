import json
import os
import time

import asyncio
import websockets
from twilio.rest import Client


sms_client = Client(os.getenv("TWILIO_ACCOUNT_SID").strip(), os.getenv("TWILIO_AUTH_TOKEN").strip())

messages = [
    {"type": "auth","access_token": os.getenv("HA_ACCESS_TOKEN").strip()},
    {"type":"subscribe_events","event_type":"state_changed","id":1},
]
messages = [
    f'{{"type": "auth","access_token": "{os.getenv("HA_ACCESS_TOKEN").strip()}"}}',
    '{"type":"subscribe_events","event_type":"state_changed","id":1}',
]
# print(json.dumps(json.loads(messages[1]), indent=4))
# print(json.dumps(messages[0], indent=4))
# print(json.dumps(messages[1], indent=4))
# {"id":1,"type":"event","event":{
#   "event_type":"state_changed","data":{
#       "entity_id":"binary_sensor.front_door_sensor_opening","old_state":{
#           "entity_id":"binary_sensor.front_door_sensor_opening","state":"on","attributes":{
#               "migrated_to_cache":true,"device_class":"opening","friendly_name":"Front Door Sensor Opening"}
#           ,"last_changed":"2023-06-28T02:07:18.022236+00:00","last_updated":"2023-06-28T02:07:18.022236+00:00","context":{
#               "id":"01H3ZW2K06GFZ2VQD5KQNB2GEE","parent_id":null,"user_id":null}
#           }
#       ,"new_state":{
#           "entity_id":"binary_sensor.front_door_sensor_opening","state":"off","attributes":{
#               "migrated_to_cache":true,"device_class":"opening","friendly_name":"Front Door Sensor Opening"}
#           ,"last_changed":"2023-06-28T02:07:19.961515+00:00","last_updated":"2023-06-28T02:07:19.961515+00:00","context":{
#               "id":"01H3ZW2MWSFHYVV3ZYF58SPWBM","parent_id":null,"user_id":null}
#           }
#       }
#   ,"origin":"LOCAL","time_fired":"2023-06-28T02:07:19.961515+00:00","context":{
#       "id":"01H3ZW2MWSFHYVV3ZYF58SPWBM","parent_id":null,"user_id":null}
#   }
# }

# def send_gvoice_sms(phone, text):
#     from googlevoice import Voice

#     voice = Voice()

#     voice.login(email="*******", passwd="*****")

#     voice.send_sms(phone, text)


async def listen(uri):
    async with websockets.connect(uri, ping_interval=None) as websocket:
        for message in messages:
            print(message)
            await websocket.send(message)
        # print(json.dumps(json.loads(messages[0]), indent=4))
        # await websocket.send(json.dumps(messages[0]))
        # await websocket.send(messages[0])
        # print(messages[0])

        while True:
            msg = await websocket.recv()

            data = json.loads(msg)
            # print(json.dumps(data, indent=4))
            # if data["type"] == "auth_required":
            #     print(messages[0])
            #     await websocket.send(messages[0])
                # for message in messages:
                #     print(message)
                #     await websocket.send(message)
            try:
                if data["event"]["event_type"] == "state_changed":

                    if data['event']['data']['new_state']['state'] == "off":
                        state = "Closed"
                    elif data['event']['data']['new_state']['state'] == "on":
                        state = "Opened"
                    else:
                        state = data['event']['data']['new_state']['state']
                    text = f"Entity: {data['event']['data']['new_state']['entity_id']}: {state}"

                    # send_gvoice_sms(os.getenv("TWILIO_PHONE"), text)

                    print(text)

                    if state == "Opened":
                        message = sms_client.messages.create(
                            body=text,
                            from_=os.getenv("TWILIO_PHONE"),
                            to=os.getenv("MY_PHONE"),
                        )
                        print(message)
                        print()
                        print()
                else:
                    print(json.dumps(data, indent=4))
            except KeyError as e:
                print(json.dumps(data, indent=4))


# messages = [
#     '{"type":"supported_features","id":1,"features":{"coalesce_messages":1}}',
#     '{"type":"subscribe_entities","id":3}',
#     '{"type":"subscribe_events","event_type":"component_loaded","id":4}',
#     '{"type":"subscribe_events","event_type":"core_config_updated","id":5}',
#     '{"type":"get_config","id":6}',
#     '{"type":"subscribe_events","event_type":"service_registered","id":7}',
#     '{"type":"subscribe_events","event_type":"service_removed","id":8}',
#     '{"type":"get_services","id":9}',
#     '{"type":"subscribe_events","event_type":"panels_updated","id":10}',
#     '{"type":"get_panels","id":11}',
#     '{"type":"subscribe_events","event_type":"themes_updated","id":12}',
#     '{"type":"frontend/get_themes","id":13}',
#     '{"type":"auth/current_user","id":14}',
#     '{"type":"frontend/get_user_data","key":"core","id":15}',
#     '{"type":"lovelace/config","url_path":null,"force":false,"id":16}',
#     '{"type":"lovelace/resources","id":17}',
#     '{"type":"subscribe_events","event_type":"entity_registry_updated","id":18}',
#     '{"type":"config/entity_registry/list_for_display","id":19}',
#     '{"type":"subscribe_events","event_type":"device_registry_updated","id":20}',
#     '{"type":"config/device_registry/list","id":21}',
#     '{"type":"subscribe_events","event_type":"area_registry_updated","id":22}',
#     '{"type":"config/area_registry/list","id":23}',
#     '{"type":"frontend/get_user_data","key":"language","id":24}',
#     '{"type":"subscribe_events","event_type":"component_loaded","id":25}',
#     '{"type":"frontend/get_translations","language":"en","category":"entity_component","id":26}',
#     '{"type":"frontend/get_translations","language":"en","category":"entity","id":27}',
#     '{"type":"frontend/get_translations","language":"en","category":"state","id":28}',
#     '{"type":"recorder/info","id":29}',
#     '{"type":"persistent_notification/subscribe","id":30}',
#     '{"type":"subscribe_events","event_type":"repairs_issue_registry_updated","id":31}',
#     '{"type":"repairs/list_issues","id":32}',
#     '{"type":"lovelace/resources","id":33}',
#     '{"type":"subscribe_events","event_type":"lovelace_updated","id":34}',
#     '{"type":"frontend/get_translations","language":"en","category":"title","id":35}',
#     '{"type":"energy/get_prefs","id":36}'
# ]

# class WebSocketClient:
#     def __init__(self):
#         pass

#     async def connect(self):
#         self.connection = await websockets.connect(
#             "", ping_interval=None
#         )
#         if self.connection.open:
#             await self.sendMessage(
#                 json.dumps(
#                     {
#                         "type": "auth",
#                         "access_token": "",
#                     }
#                 )
#             )
#             await self.sendMessage(json.dumps({"type": "recorder/info", "id": 29}))
#             return self.connection

#     async def sendMessage(self, message):
#         await self.connection.send(message)

#     async def receiveMessage(self, connection):
#         while True:
#             message = await connection.recv()
#             print(message)
#             print()
#             print()
#             # try:
#             #     message = await connection.recv()
#             #     print(message)
#             # except websockets.exceptions.ConnectionClosed as e:
#             #     print(e)
#             #     print("Connection with server closed")
#             #     break

#     async def heartbeat(self, connection):
#         while True:
#             try:
#                 await connection.send("ping")
#                 print("Pinged")
#                 await asyncio.sleep(5)
#             except websockets.exceptions.ConnectionClosed as e:
#                 print(e)
#                 print("Connection with server closed")
#                 break

# async def socket_consumer(socket):
#     # take messages from the web socket and push them into the queue
#     async for message in socket:
#         print(message)
#         # await outgoing.put(message)

# async def socket_producer(socket):
#     for message in messages:
#         await socket.send(message)

# async def socket_producer(socket):
#     # take messages from the queue and send them to the socket
#     while True:
#         # Queueing
#         # message = await incoming.get()
#         for message in messages:
#             await socket.send(message)
#             # await socket.send(json.dumps(message))

# async def connect_socket():
#     # header = {"Authorization": r"Basic XXXX="}
#     uri = ''
#     async with websockets.connect(uri, extra_headers=None) as websocket:
#         # create tasks for the consumer and producer. The asyncio loop will
#         # manage these independently
#         consumer_task = asyncio.create_task(socket_consumer(websocket))
#         producer_task = asyncio.create_task(socket_producer(websocket))

#         # start both tasks, but have the loop return to us when one of them
#         # has ended. We can then cancel the remainder
#         done, pending = await asyncio.wait(
#             [consumer_task, producer_task],
#             return_when=asyncio.FIRST_COMPLETED
#         )
#         for task in pending:
#             task.cancel()
#         # force a result check; if there was an exception it'll be re-raised
#         for task in done:
#             task.result()

# async def main():
#     # pipe_to_socket = asyncio.Queue()
#     # socket_to_pipe = asyncio.Queue()

#     socket_coro = connect_socket()

#     await asyncio.gather(socket_coro)

# if __name__ == '__main__':
#     asyncio.run(main())

# if __name__ == "__main__":
#     client = WebSocketClient()
#     loop = asyncio.get_event_loop()
#     connection = loop.run_until_complete(client.connect())
#     tasks = [
#         asyncio.ensure_future(client.heartbeat(connection)),
#         asyncio.ensure_future(client.receiveMessage(connection)),
#     ]

#     loop.run_until_complete(asyncio.wait(tasks))

if __name__ == "__main__":
    asyncio.run(listen(os.getenv("HA_WEBSOCKET_URL")))
