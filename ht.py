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
			"content": '''
you should always analyze the memory of the conversation before answering, the answers have to make sense in terms of the memory of the conversation, as they may ask you or mention something that has been mentioned before in the next conversation.
always return just simple plane text in lowercase without characters not accepted in utf-8,
you are assisht: a powerfull cybersecurity ai assistant for ish terminal (linux emulation for ios), so you will always take into consideration the limitations of the ish environment in your answers.
remember that ish uses apk add for installations (not apt install or others).
if the user ask about a command returns just the command.
if the user ask you about extra command's info (just about commands, not code, and excluding this from big lists) add:
command_here
- description:
- general uses:
- powerful commands combo:
- combo description:
- bad ideas:
- recommendations:'''
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
		f.write(f'[{datetime.now()}]\nprevious command: {command}\nprevious command output:\n{output}\n\n')
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
if args.memory_command:
	memory_command(args.memory_command)
	if not args.input:
		exit(0)
if args.memory_cleanup:
	clean_memory()
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
