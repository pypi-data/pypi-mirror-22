#!/usr/bin/env python
import argparse
from pg_chameleon import replica_engine
from pg_chameleon import config_dir
configdir = config_dir()
configdir.set_config()

commands = [
	'create_schema',
	'init_replica',
	'start_replica',
	'upgrade_schema',
	'drop_schema', 
	'list_config', 
	'add_source', 
	'drop_source', 
	'stop_replica', 
	'disable_replica', 
	'enable_replica', 
	'sync_replica', 
	'show_status' , 
	'detach_replica'
	]
command_help = 'Available commands, ' + ','.join(commands)
table_help =  """Specifies the table's name to sync. It's possible to specify multiple table names separated by comma. If the parameter is omitted all tables will be syncronised."""
config_help =  """Specifies the configuration to use. The configuration shall be specified without extension (e.g. --config foo) and the file foo.yaml should be in ~/.pg_chameleon/config/"""

parser = argparse.ArgumentParser(description='Command line for pg_chameleon.',  add_help=True)
parser.add_argument('command', metavar='command', type=str, help=command_help)
parser.add_argument('--config', metavar='config', type=str,  default='default',  required=False, help=config_help)
parser.add_argument('--table', metavar='table', type=str,  default='*',  required=False, help=table_help)

args = parser.parse_args()

if args.command in commands:
	replica = replica_engine(args.config)
	if args.command == commands[0]:
		replica.create_service_schema()
	elif args.command == commands[1]:
		replica.init_replica()
	elif args.command == commands[2]:
		replica.run_replica()
	elif args.command == commands[3]:
		replica.upgrade_service_schema()
	elif args.command == commands[4]:
		replica.drop_service_schema()
	elif args.command == commands[5]:
		replica.list_config()
	elif args.command == commands[6]:
		replica.add_source()
	elif args.command == commands[7]:
		replica.drop_source()
	elif args.command == commands[8]:
		replica.stop_replica()
	elif args.command == commands[9]:
		replica.stop_replica(allow_restart=False)
	elif args.command == commands[10]:
		replica.enable_replica()
	elif args.command == commands[11]:
		replica.sync_replica(args.table)
	elif args.command == commands[12]:
		replica.show_status()
	elif args.command == commands[13]:
		replica.detach_replica()
