import argparse
import ops as o
import os

def check_token():
    if not os.path.exists("dyn.tkn"):
        print("Token file missing - pass the --token argument or run \"dyncli config --token <token>\"")
        return None
    with open("dyn.tkn", "r") as f:
        return f.readline()

def write_token(args):
    with open('dyn.tkn', 'w') as f:
        f.write(args.token)
    print("Token file created/updated - ignore missing file warnings if any appeared.")

parser = argparse.ArgumentParser(description="Command line utility to update dynv6 domains and subdomains with the dynv6 API.")
ops = parser.add_subparsers(help="Operation to run")

op_config = ops.add_parser("config", help="Configure dyncli to save your token")
op_config.set_defaults(func=write_token)

op_add = ops.add_parser("add", help="Add record to a zone/domain")
op_add.add_argument('-a', help="Update A records instead of AAAA.", action='store_true')
op_add.add_argument('id', help="Zone ID (use ls to view)")
op_add.add_argument('--name', help="Name of the record. Will fail if left blank on an A record.")
op_add.add_argument('--addr', help="Address. If not defined, it'll be set to your public IP.")
op_add.set_defaults(func=o.add_record)

# TODO: op_update = ops.add_parser("update", help="Update record")
# TODO: op_add.add_argument('id', help="Zone ID (use ls to view)")
# TODO: op_add.add_argument('record_id', help="ID of the record.")
# TODO: op_add.add_argument('--addr', help="Address. If not defined, it'll be set to your public IP.")

# TODO: op_rm = ops.add_parser("rm", help="Remove a record from a zone/domain")

op_list = ops.add_parser("ls", help="List domains/zones")
op_list.set_defaults(func=o.ls)

op_listzones = ops.add_parser("lsr", help="List records of a domain/zone")
op_listzones.add_argument("id", help="ID of the zone")
op_listzones.set_defaults(func=o.ls_record)

parser.add_argument('--token', help="HTTP Token. Get one at https://dynv6.com/keys/", default=check_token())
args = parser.parse_args()
if hasattr(args, "func"):
    args.func(args)
else:
    parser.print_help()
