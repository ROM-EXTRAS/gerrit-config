import copy
import json
import os,ast
import subprocess
import sys
import urllib.parse

os.environ["REQUESTS_CA_BUNDLE"] = '/Users/russhah/gerrit.crt'
os.environ["SSL_CERT_FILE"] = '/Users/russhah/gerrit.crt'
from gerrit import GerritClient

client = GerritClient(base_url="https://localhost:8443", username="droidfreak32", password="AyRyYkhV2DAGf6Q0m615P8C2jZhHZiVUkr8Z8y27Ig")

if __name__ == "__main__":
    gerrit = client

    results = []
    # results = client.changes.search(query='status:merged', limit=9999)
    skip = 0
    jump = 360
    while True:
        query = client.changes.search(query='intopic:^.%2b', limit=jump, skip=skip)
        if len(query) == jump:
            skip += jump
            results += query
        else:
            results += query
            break

    current_mapping = {}
    for result in results:
        current_mapping[urllib.parse.unquote(result['id'])] = result['topic']
    pass
    # print(current_mapping)

    # with open('gerrit.json', 'w') as w:
    #     json.dump(current_mapping, fp=w, indent=4)
    # pass
    # pass

    change_topic_map = {}
    tweets = []
    for line in open('gerrit.json', 'r'):
        change_topic_map[json.loads(line)['id']] = json.loads(line)['topic']
    pass
    print()
    print()

    for ID, topicname in current_mapping.items():
        project, branch, change_id = ID.split('~')
        topic = topicname
        try:
            if change_topic_map[change_id] == topicname:
                pass
            else:
                # print(f"Gerrit Topic vs json topic:\n{topicname}\n{change_topic_map[change_id]}\n")
                print(f"sed -i '/{change_id}/d' gerrit_fresh.json")
                print(f'echo {{"topic":"{topicname}","id":"{change_id}"}}')
                pass
        except:
            print(f"{change_id} Does not exist in gerrit.json")


    for ID, topic in change_topic_map.items():
        try:
            if current_mapping[ID] == topic:
                print(f"Matching {topic} for Change {ID}")
                continue
        except:
            print(f"Exception for ID {ID}")
        with subprocess.Popen(["echo", "ssh", "lgerrit", "gerrit", "set-topic", ID, "-t", topic],
                            stdout=subprocess.PIPE) as proc:
            for c in iter(proc.stdout.readline, b''):
                sys.stdout.buffer.write(c)
            # print(proc.stdout.read())
    # tweets = []
    # for line in open('/home/horcrux/gerrit.json', 'r'):
    #     tweets.append(json.loads(ast.literal_eval(json.dumps(line))))
    #