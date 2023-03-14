import json
import os,ast
import subprocess
import sys

os.environ["REQUESTS_CA_BUNDLE"] = '/home/horcrux/gerrit.crt'
os.environ["SSL_CERT_FILE"] = '/home/horcrux/gerrit.crt'
from gerrit import GerritClient

client = GerritClient(base_url="https://localhost:8443", username="droidfreak32", password="AyRyYkhV2DAGf6Q0m615P8C2jZhHZiVUkr8Z8y27Ig")

if __name__ == "__main__":
    gerrit = client
    results = client.changes.search(query='intopic:^.%2b+status:merged')
    # results = client.changes.search(query='status:merged', limit=9999)
    change_topic_map = {}
    for result in results:
        change_topic_map[result['change_id']] = result['topic']
        pass
    print(change_topic_map)

    # with open('gerrit.json', 'w') as w:
    #     json.dump(change_topic_map, fp=w, indent=4)
    # pass
    # pass
    change_topic_map = {}
    tweets = []
    for line in open('gerrit.json', 'r'):
        change_topic_map[json.loads(line)['id']] = json.loads(line)['topic']
    pass
    print()
    print()

    for ID, topic in change_topic_map.items():
        with subprocess.Popen(["echo", "ssh", "lgerrit", "gerrit", "set-topic", ID, "-t", topic],
                              stdout=subprocess.PIPE) as proc:
            for c in iter(proc.stdout.readline, b''):
                sys.stdout.buffer.write(c)

            # print(proc.stdout.read())
    # tweets = []
    # for line in open('/home/horcrux/gerrit.json', 'r'):
    #     tweets.append(json.loads(ast.literal_eval(json.dumps(line))))
    #