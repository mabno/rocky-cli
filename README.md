# Rocky Password Manager CLI
**Rocky Password Manager** is a command-line interface for **password managment**. Actually, it's an account manager given that not only can **store password** but also store **usernames, and emails**. Also, this program has an **authentication system** and a **encrypted database** to protect the sensible information it contains

Written in<br>
<img width="80" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original-wordmark.svg" />


## Table of Contents
1. [Commands](#commands)
	- [auth](#commands_auth)
		- [register](#commands_auth_1)
		-  [login](#commands_auth_2)
		-  [logout](#commands_auth_3)
		-  [status](#commands_auth_4)
	- [add](#commands_add)
	- [update](#commands_update)
	- [delete](#commands_delete)
	- [get](#commands_get)
	- [details](#commands_details)
	- [copy](#commands_copy)
2. [Installation](#install)
3. [Configuration](#config)

<a name="commands"></a>
## Commands

<a name="commands_auth"></a>
### auth

Authentication system (register, login, logout and status)
<br>

<a name="commands_auth_1"></a>
**auth register**
Create an account to use Rocky.
Password is optional. If it's not provided, you can login without type a password

    $ rocky auth register [<password>]

   <a name="commands_auth_2"></a>
  **auth login**
Authenticate with the previously created account

    $ rocky auth login [<password>]

  <a name="commands_auth_3"></a>
**auth logout**
Finish the session

    $ rocky auth logout

<a name="commands_auth_4"></a>
   **auth status**
Check the current auth status.
Status can be: Logged In, Logged out, No registered

    $ rocky auth status
<br>

<a name="commands_add"></a>
### add
Store a new account

    $ rocky add -s <service> -p <password> [-e <email>] [-u <username>]
Usage example

    $ rocky add -s Github -p mypassword123
    $ rocky add -s Github2 -p mypassword321 -e john.doe@gmail.com -u mabno

<br>

<a name="commands_update"></a>
### update
Update an account

    $ rocky update [-s <service>] [-p <password>] [-e <email>] [-u <username>] <id>
Usage example

    $ rocky update -p thisismynewpassword 13
    $ rocky update -s Github0 -p mypassword321 -e new.email@gmail.com -u mabno2 1

<br>

<a name="commands_delete"></a>
### delete
Delete account/s by ID

    $ rocky delete [id [id ...]]
Usage example

    $ rocky delete 2
    $ rocky delete 4 7 12

<br>

<a name="commands_get"></a>
### get
Get all stored accounts or search by name/id

    $ rocky get [<name/id>]
Usage example

    $ rocky get
    $ rocky get Github
    $ rocky get 5

<br>

<a name="commands_details"></a>
### details
Get all information of an account and extra details like creation time and update time

    $ rocky details <id>
Usage example

    $ rocky details 4

<br>

<a name="commands_copy"></a>
### copy
Copy to clipboard specified information

    $ rocky copy <id> {password, email, username}
Usage example

    $ rocky copy 5 password
    $ rocky copy 32 email

<br>

<a name="installation"></a>
## Installation
Clone the repository

	 $ cd ~
	 $ git clone https://github.com/mabno/rocky-cli.git
	 $ cd rocky-cli

You can use the CLI as a python script

	$ ./rocky.py

But I recommend you add an alias (Linux)
Type this in `~/.bashrc`

	alias rocky="python $HOME/rocky-cli/rocky.py"


<a name="configuration"></a>
## Configuration
Open `config.json`file inside project folder and change the values according to your needs
The file looks like this:

    {
		"password": "./.password",
		"session": "./.session",
		"database": "./database.db"
	}
**password**
File where your *encrypted* password will be stored

**session**
File where your session will be stored

**database**
Path and filename of the *encrypted* database