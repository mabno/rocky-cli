from termcolor import colored

def represents_int(string):
	try:
		int(string)
		return True
	except ValueError:
		return False

def read_file(path):
	with open(path, 'r') as file:
		return file.read()

def write_file(path, content):
	with open(path, 'w') as file:
		file.write(content)

def hspace(string, char_number):
	if len(string) > char_number:
		string = string[slice(char_number)]
	else:
		string = string+(' '*(char_number-len(string)))
	return string

def print_list(list):
	table_head = colored(hspace('ID', 4)+hspace('Service', 21)+hspace('Email', 31)+hspace('Password', 31), "blue")
	print(table_head)
	for record in list:
		id = colored(hspace(str(record[0]), 3), 'white')
		service = colored(hspace(record[1], 20), 'cyan')
		email = colored(hspace(record[2], 30), 'white')
		password = colored(hspace(record[4], 30), 'cyan')
		print(f'{id} {service} {email} {password}')

def print_details(record):
	print(f'{colored("ID", "cyan")} {record[0]}')
	print(f'{colored("Service", "cyan")} {record[1]}')
	print(f'{colored("Email", "cyan")} {record[2]}')
	print(f'{colored("Username", "cyan")} {record[3]}')
	print(f'{colored("Password", "cyan")} {record[4]}')
	print(f'{colored("Created at", "cyan")} {record[5]}')
	print(f'{colored("Updated at", "cyan")} {record[6]}')

def print_successfull(string):
	print(colored(string, 'green'))

def print_error(string):
	print(colored(string, 'red'))

def print_status(status):
	print(f'{colored("STATUS", "cyan")} {status}')
