import websocket, json, threading, time
from googletrans import Translator

def send_json_request(ws, request):
    ws.send(json.dumps(request))

def recieve_json_response(ws):
    response = ws.recv()
    if response:
        return json.loads(response)   

def heartbeat(interval, ws):
    print('Heartbeat begin')
    while True:
        time.sleep(interval)
        heartbeatJSON = {
            'op': 1,
            'd': 'null'
        }
        send_json_request(ws, heartbeatJSON)

ws = websocket.WebSocket()
ws.connect('wss://gateway.discord.gg/?v=6&encording=json')
event = recieve_json_response(ws)

heartbeat_interval = event['d']['heartbeat_interval'] / 1000
threading._start_new_thread(heartbeat, (heartbeat_interval, ws))

token = 'こちらにAuthenticationトークンを入力してください'
payload = {
    'op': 2,
    'd': {
        'token': token,
        'properties': {
            '$os': 'windows',
            '$browser': 'chrome',
            '$device': 'pc'
        }
    }
}
send_json_request(ws, payload)

tr = Translator()

while True:
    event = recieve_json_response(ws)

    try:
        content = event['d']['content']
        author = event['d']['author']['username']
        print(f'{author}: {content}')
        print(tr.translate(text = content, dest='ja').text, '\n')
        op_code = event('op')
        if op_code == 11:
            print('heartbeat recieved')
    except:
        pass    
