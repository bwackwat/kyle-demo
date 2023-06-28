import json
import os
import time

import asyncio
import websockets
from twilio.rest import Client


sms_client = Client(
    os.getenv("TWILIO_ACCOUNT_SID").strip(), os.getenv("TWILIO_AUTH_TOKEN").strip()
)

messages = [
    f'{{"type": "auth","access_token": "{os.getenv("HA_ACCESS_TOKEN").strip()}"}}',
    '{"type":"subscribe_events","event_type":"state_changed","id":1}',
]

async def listen(uri):
    async with websockets.connect(uri) as websocket:
        for message in messages:
            print(message)
            await websocket.send(message)

        while True:
            msg = await websocket.recv()
            data = json.loads(msg)

            try:
                if data["event"]["event_type"] == "state_changed":
                    if data["event"]["data"]["new_state"]["state"] == "off":
                        state = "Closed"
                    elif data["event"]["data"]["new_state"]["state"] == "on":
                        state = "Opened"
                    else:
                        state = data["event"]["data"]["new_state"]["state"]
                    text = f"Entity: {data['event']['data']['new_state']['entity_id']}: {state}"

                    print(text)

                    if state == "Opened":
                        message = sms_client.messages.create(
                            body=text,
                            from_=os.getenv("TWILIO_PHONE"),
                            to=os.getenv("MY_PHONE"),
                        )
                        print(json.dumps(message.__dict__, indent=4, default=str))
                else:
                    print(json.dumps(data, indent=4))
            except KeyError as e:
                print(json.dumps(data, indent=4))


if __name__ == "__main__":
    asyncio.run(listen(os.getenv("HA_WEBSOCKET_URL")))
