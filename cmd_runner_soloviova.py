import time
import json
import subprocess
import os
import requests
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
OWNER = 'WellnessCode'
REPO = 'Soloviova'
BRANCH = 'main'
HEADERS = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}

def get_file(path):
    url = f'https://api.github.com/repos/{OWNER}/{REPO}/contents/{path}?ref={BRANCH}'
    r = requests.get(url, headers=HEADERS)
    if r.status_code == 200:
        data = r.json()
        import base64
        content = base64.b64decode(data['content']).decode('utf-8')
        return json.loads(content), data['sha']
    return None, None

def put_file(path, content_dict, sha):
    import base64
    content = base64.b64encode(json.dumps(content_dict, ensure_ascii=False).encode()).decode()
    url = f'https://api.github.com/repos/{OWNER}/{REPO}/contents/{path}'
    payload = {
        'message': 'cmd result',
        'content': content,
        'sha': sha,
        'branch': BRANCH
    }
    requests.put(url, headers=HEADERS, json=payload)

last_id = 'init'

while True:
    try:
        pending, sha = get_file('cmds/pending.json')
        if pending and pending.get('id') != last_id:
            cmd_id = pending['id']
            cmd = pending['cmd']
            print(f'Executing: {cmd}')
            try:
                result = subprocess.run(
                    cmd, shell=True, capture_output=True,
                    text=True, timeout=120
                )
                output = (result.stdout + result.stderr)[:3000]
            except subprocess.TimeoutExpired:
                output = 'TIMEOUT'
            except Exception as e:
                output = str(e)
            _, result_sha = get_file('cmds/result.json')
            put_file('cmds/result.json', {'id': cmd_id, 'result': output}, result_sha)
            last_id = cmd_id
            print(f'Done: {output[:100]}')
    except Exception as e:
        print(f'Error: {e}')
    time.sleep(5)
