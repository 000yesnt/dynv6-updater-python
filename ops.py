import requests
import json

api = "https://dynv6.com/api/v2/"
ipify = ['https://api64.ipify.org?format=json', 'https://api.ipify.org?format=json']

def ls_record(args):
    id = args.id
    auth = args.token
    r = requests.get(api + f'zones/{id}/records', headers={"Authorization": f"Bearer {auth}"})
    if r.ok:
        records = r.json()
        print(f"Received {len(records)} records")
        for re in records:
            print(f"Record name: {re['name']}\n"
                  f"Record value: {re['data']}\n"
                  f"Record type: {re['type']}\n"
                  f"Record ID: {re['id']}\n")

def add_record(args):
    id = args.id
    name = args.name
    addr = args.addr if args.addr else requests.get(ipify[int(args.a)]).json()["ip"]
    auth = args.token

    r = requests.post(api + f"zones/{id}/records", headers={"Authorization": f"Bearer {auth}"}, json={
        'name': name,
        'data': addr,
        'type': "A" if args.a else "AAAA"
    })
    if r.ok:
        print(f"Request successful: {r.json()}")

def upd_record(args):
    auth = args.token
    zid = args.id
    rid = args.record_id
    type = requests.get(api + f'zones/{zid}/records/{rid}', headers={"Authorization": f"Bearer {auth}"}).json()['type']
    ip = args.addr if args.addr else requests.get(ipify[int(type == 'A')]).json()["ip"]
    r = requests.patch(api + f"zones/{zid}/records/{rid}", headers={"Authorization": f"Bearer {auth}"}, json={
        'data': ip
    })
    if r.ok:
        print(f"success: {r.json()}")
    else:
        print(f"fail {r.status_code}: {r.json()} ")

def ls(args):
    auth = args.token
    r = requests.get(api + "zones", headers={"Authorization": f"Bearer {auth}"})
    if r.ok:
        zones = r.json()
        print(f"Received {len(zones)} zones.")
        for z in zones:
            print(f"Zone name: {z['name']}\n"
                  f"Zone ID: {z['id']}\n"
                  f"Zone IPv4 address: {z['ipv4address']}\n"
                  f"Zone IPv6 prefix: {z['ipv6prefix']}\n"
                  f"Created: {z['createdAt']}\n"
                  f"Last updated: {z['updatedAt']}\n")
    else:
        raise requests.exceptions.HTTPError(f"Response failed with code {r.status_code}")