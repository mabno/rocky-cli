#!/usr/bin/python
import argparse
from db import Database
import helpers
import os
from hashlib import md5
import json
import pyperclip
PASSWORD_FILE, SESSION_FILE, DATABASE_FILE = None, None, None

path = lambda x : f'{os.path.dirname(os.path.abspath(__file__))}/{x}'
config = json.loads(helpers.read_file(path('config.json')))
PASSWORD_FILE = path(config['password'])
SESSION_FILE = path(config['session'])
DATABASE_FILE = path(config['database'])

session_password = None
if os.path.exists(SESSION_FILE):
	 session_password = helpers.read_file(SESSION_FILE)

# auth_status:
# 0: NO REGISTERED
# 1: LOGGED OUT
# 2: LOGGED IN

def check_auth_status():
	if not os.path.exists(PASSWORD_FILE):
		return 0
	elif session_password == None:
		return 1
	else:
		stored_password = helpers.read_file(PASSWORD_FILE)
		password_hash = md5(session_password.encode()).hexdigest()
		if password_hash == stored_password:
			return 2
		else:
			return 1

def configure_parser(parser):
	subparsers = parser.add_subparsers(dest='action')
	add_parser = subparsers.add_parser('add')
	add_parser.add_argument('-s', '--service', required=True)
	add_parser.add_argument('-e', '--email', default='-')
	add_parser.add_argument('-u', '--username', default='-')
	add_parser.add_argument('-p', '--password', required=True)

	update_parser = subparsers.add_parser('update')
	update_parser.add_argument('id', type=int)
	update_parser.add_argument('-s', '--service')
	update_parser.add_argument('-e', '--email')
	update_parser.add_argument('-u', '--username')
	update_parser.add_argument('-p', '--password')

	get_parser = subparsers.add_parser('get')
	get_parser.add_argument('search', nargs='?')

	delete_parser = subparsers.add_parser('delete')
	delete_parser.add_argument('id', type=int, nargs='*')

	details_parser = subparsers.add_parser('details')
	details_parser.add_argument('id', type=int)

	copy_parser = subparsers.add_parser('copy')
	copy_parser.add_argument('id', type=int)
	copy_parser.add_argument('field', choices=['password', 'email', 'username'])

	auth_parser = subparsers.add_parser('auth')
	auth_parser.add_argument('mode', choices=['login', 'register', 'logout', 'status'])
	auth_parser.add_argument('password', nargs='?', default='')

	return parser

def protected(func):
	def inner():
		db = Database()
		if auth_status != 2:
			helpers.print_error('You are not logged in')
			return
		status = db.connect(DATABASE_FILE, session_password)
		if issubclass(type(status), Exception):
			print('Error: ',db)
			return
		func(db)
	return inner

@protected
def add(db):
	result = db.create((
		args.service,
		args.email,
		args.username,
		args.password
	))
	if issubclass(type(result), Exception):
		helpers.print_error(result)
	else:
		helpers.print_successfull('Record added successfully')

@protected
def update(db):
	result = db.update(args.id, (
		args.service,
		args.email,
		args.username,
		args.password
	))
	if issubclass(type(result), Exception):
		helpers.print_error(result)
	elif result == 0:
		helpers.print_error('Set a valid ID')
	else:
		helpers.print_successfull('Record updated successfully')


@protected
def get(db):
	result = []
	if args.search == None:
		result = db.get_all()
	elif helpers.represents_int(args.search):
		result = db.get_one(int(args.search))
	else:
		result = db.search(args.search)

	if issubclass(type(result), Exception):
		helpers.print_error(result)
	elif len(result) == 0:
		helpers.print_error('Records not found')
	else:
		helpers.print_list(result)

@protected
def delete(db):
	result = db.delete(args.id)
	if issubclass(type(result), Exception):
		helpers.print_error(result)
	elif result == 0:
		helpers.print_error('Set a valid ID')
	else:
		helpers.print_successfull(f'{result} Record/s deleted successfully')

@protected
def details(db):
	result = db.get_one(args.id)

	if issubclass(type(result), Exception):
		helpers.print_error(result)
	elif len(result) == 0:
		helpers.print_error('Set a valid ID')
	else:
		helpers.print_details(result[0])

@protected
def copy(db):
	result = db.get_one(args.id)

	if issubclass(type(result), Exception):
		helpers.print_error(result)
	elif result == 0:
		helpers.print_error('Set a valid ID')
	else:
		to_copy = ""
		if args.field == 'password':
			to_copy = result[0][4]
		elif args.field == 'email':
			to_copy = result[0][2]
		elif args.field == 'username':
			to_copy = result[0][3]
		pyperclip.copy(to_copy)
		helpers.print_successfull(f'<{to_copy}> copied to clipboard successfully')

def auth():
	if args.mode == 'register':
		if auth_status == 1:
			helpers.print_error('You already have an account\nFor resetting your account and register again, you must to use <auth register> command being authenticated')
			return
		if auth_status == 2:
			helpers.print_error('[WARNING] You are already registered, if you continue the database will be deleted and will be created another')
			choice = input('Continue? (y/n): ')
			if choice == 'n':
				helpers.print_successfull('Action canceled')
				return
		if os.path.exists(DATABASE_FILE):
			os.remove(DATABASE_FILE)
		password_hash = md5(args.password.encode()).hexdigest()
		helpers.write_file(PASSWORD_FILE, password_hash)
		helpers.print_successfull('Registered successfully')

	if args.mode == 'login':
		if auth_status == 0:
			helpers.print_error('You are not registered')
			return
		if auth_status == 2:
			helpers.print_error('You are already logged in')
			return
		stored_password = helpers.read_file(PASSWORD_FILE)
		password_hash = md5(args.password.encode()).hexdigest()
		if stored_password == password_hash:
			helpers.write_file(SESSION_FILE, args.password)
			helpers.print_successfull('Logged in')
		else:
			helpers.print_error('Incorrect password')

	if args.mode == 'logout':
		if auth_status == 2:
			os.remove(SESSION_FILE)
			helpers.print_successfull('Logged out')
		else:
			helpers.print_error('You are not logged')

	if args.mode == 'status':
		if auth_status == 0:
			helpers.print_status('No registered')
		elif auth_status == 1:
			helpers.print_status('Logged out')
		elif auth_status == 2:
			helpers.print_status('Logged in')


auth_status = check_auth_status()
#print(auth_status)
parser = configure_parser(argparse.ArgumentParser())
args = parser.parse_args()

actions = {
	'add': add,
	'update': update,
	'get': get,
	'delete': delete,
	'details': details,
	'copy': copy,
	'auth': auth
}

actions.get(args.action, parser.print_help)()
