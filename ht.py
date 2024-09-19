#!/usr/bin/env python3
from argparse import ArgumentParser
from subprocess import run, PIPE
from colorama import Fore, Style
from datetime import datetime
from requests import post
from time import sleep
from sys import exit

# openai
def assisht(msg):
	headers={"Authorization": f"Bearer {key}"}
	url="https://api.openai.com/v1/chat/completions"
	data={
		"model": "gpt-4o-mini",
 		"messages": [
		{
			"role": "system",
			"content": '''you should always analyze the memory of the conversation before answering, the answers have to make sense in terms of the memory of the conversation, as they may ask you or mention something that has been mentioned before in the next conversation.
always return just simple plane text in lowercase without characters not accepted in utf-8, also do not use any type of markdown that returns results with symbols such as *  or other symbols used in markdowns.
you are assisht: a powerfull cybersecurity ai assistant for ish terminal (linux emulation for ios), your creator is azuk4r and his github is https://github.com/azuk4r (your project repository is https://github.com/azuk4r/assisht).
you will always take into consideration the limitations of the ish environment in your answers.
i insist: remember not to use any kind of markdown like ** for bold, not even in lists that you can provide.

remember that ish uses apk add for installations (not apt install or others).
ish uses adduser and deluser to create and delete users.
in ish several commands such as ifconfig, ip a or iproute, among others, may not work. 
for this reason, your creator azuk4r, has created a toolkit called ish-toolkil, which contains tools to find solutions to the lack of some of them (this is not part of the default ish environment and must be downloaded from the azuk4r's github in the https://github.com/azuk4r/ish-toolkit repository using git clone because is not available with apk add). 
the toolkit currently contains: 
- ht (asissht: artificial intelligence assistant for the ish environment), available possible args (not required): -i (--input) -mc (--memory-command) -cl (--clean-memory).
about -i: user input prompt.
about -mc: saves the output of the specified command in memory.
about -cl: clean the memory file.
about args combo: all arguments work well together, example: ht -i 'list all files with a short description' -mc 'ls /etc' -cl 0 (this will first clear the memory, then store in memory the output of the command result and finally send the input to get the result).
about no args: by default, if run without arguments only ht will prompt you for input afterwards. 
about config: the first run will ask you for the openai key.
- getip (command to obtain local and public ip, you can use getip to get your ips and also you can specify a url as an argument to get its ip, example: getip example.com).
- paypy (command to run payload server), the port and path of the payload must be specified, example: paypy 22 /payload/path.
never recommend the use of ish-toolkit without first checking that there is indeed a solution for that particular problem.

if the user ask you specificaly about a command returns just the command (don't make assumptions about this, the user must have explicitly asked you for a command).
if the user ask you specificaly about extra info from a command add:
command_here
- description:
- general uses:
- powerful commands combo:
- combo description:
- bad ideas:
- recommendations:
the above info will always be adapted to the language from the user's current input. this means, for example, that if the user speak to you in english, you will use recomendations, but in spanish you will use recomendaciones (same thing for each previous point).
you should consider only the language of the current input, ignoring the previous memory only for this particular task and nothing else.

about your codestyle:
do not use double quotation marks ", always single quotation marks ' except in string strings where we will use " inside ' ' to avoid conflicts.
you will only import the functions to be used from each module, example: from time import sleep.
always use tabs, not normal spaces.
if you add comments, they will be technical and to the point.
no matter in which language they communicate or have communicated with you, the code will always be in english. that rule is only used if the user ask you code.
i insist: even if they speak to you in another language, spanish for example, you will always give all the code in english, including variables, comments or any part of the code, always obligatory the code in english.
the last rule affects only code, even if you deliver code in english you will still communicate in the language of the conversation.'''
		},
		{
			"role": "user",
 			"content": msg
 		}
		]
	}
	res=post(url,headers=headers,json=data).json()
	try:
		return res['choices'][0]['message']['content']
	except:
		print('output: '+res['error']['message'])
		exit(0)

# output command memory storing
def memory_command(command):
	result=run(command,shell=True,stdout=PIPE,stderr=PIPE,text=True)
	output=result.stdout+result.stderr
	print(output)
	with open('/etc/assisht/memory.txt','a') as f:
		f.write(f'[{datetime.now()}]\nprevious command: {command}\nprevious command output:\n{output}\n')
		f.close()

# huge prompts
def split_memory(max_lines=50000):
	memory=open('/etc/assisht/memory.txt','r').read()
	return [memory[i:i + max_lines] for i in range(0, len(memory), max_lines)]

# new memo
def clean_memory():
	with open('/etc/assisht/memory.txt','w') as f:
		f.write('')
		f.close()
	print(f'{Fore.BLUE}[info]{Style.RESET_ALL} successful memory file cleanup')

# args
parser = ArgumentParser(description='assisht: ai assistant for ish')
parser.add_argument('--input','-i',required=False,help='prompt input to chat with asissht')
parser.add_argument('--memory-command','-mc',required=False,help='execute a command with output memory storage')
parser.add_argument('--memory-cleanup','-cl',required=False,help='clean the memory file (that delete all the previous conversations in memory')
args = parser.parse_args()
if args.memory_cleanup:
	clean_memory()
	if not args.input:
		exit(0)
if args.memory_command:
        memory_command(args.memory_command)
        if not args.input:
                exit(0)

# load key
try:
	key=open('/etc/assisht/openai_api_key.txt','r').read()
except:
	key=input('set your openai api key: ')
	with open('/etc/assisht/openai_api_key.txt','w') as f:
		f.write(key)
		f.close()

# input
if args.input:
	msg=args.input
	print(f'{Fore.YELLOW}[input]{Style.RESET_ALL} {msg}')
else:
	msg=input(f'{Fore.YELLOW}input:{Style.RESET_ALL} ')

# memory load
memory_parts=1
no_memory='''info: any memory yet

'''
try:
	_memory=open('/etc/assisht/memory.txt','r').read()
	memory=[_memory]
except:
	memory=no_memory

# memory checkpoint
if len(memory[0]) > 50000:
	print(f'{Fore.MAGENTA}[checkpoint]{Style.RESET_ALL} warning: huge prompt detected')
	exiting=False
	while not exiting:
		checkpoint=input(f'{Fore.MAGENTA}[checkpoint]{Style.RESET_ALL} wanna clean the memory? (y/n): ')
		if checkpoint=='y':
			clean_memory()
			exiting=True
			if not args.memory_command:
				memory=no_memory 
			else:
				memory_command(args.memory_command)
				_memory=open('/etc/assisht/memory.txt','r').read()
				memory=[_memory]
		if checkpoint=='n':	
			print(f'{Fore.BLUE}[info]{Style.RESET_ALL} splitting memory into batchs...')
			memory=split_memory()
			memory_parts=len(memory)
			print(f'{Fore.BLUE}[info]{Style.RESET_ALL} memory parts: {memory_parts}')
			exiting=True
		elif not exiting:
			print(f'{Fore.RED}[error]{Style.RESET_ALL} wrong answer, try again')

# replys 
for part in range(memory_parts):
	reply=assisht(f'memory of conversation:\n{memory[part]}\n\nnew message: {msg}')
	reply=''.join(char for char in reply if not('\ud800' <= char <= '\udfff'))
	print(Fore.GREEN+'[assisht] '+Style.RESET_ALL+reply)
	with open('/etc/assisht/memory.txt','a') as f:
		f.write(f'[{datetime.now()}]\ninput: {msg}\nassisht: {reply}\n\n')
		f.close()
	sleep(1)
