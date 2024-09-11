from argparse import ArgumentParser
from subprocess import run, PIPE
from colorama import Fore, Style
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
if the user ask about a command returns just the command,
if the user ask you info about the command (just about commands)  add:
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
	output=result.stdout
	print(output)
	with open('memory.txt','a') as f:
		f.write(f'previous command: {command}\nprevious command output:\n{output}')
		f.close()

# huge prompts
def split_memory(max_lines=50000):
	memory=open('memory.txt','r').read()
	return [memory[i:i + max_lines] for i in range(0, len(memory), max_lines)]

# memory command arg
parser = ArgumentParser(description='Execute a command and capture its output.')
parser.add_argument('--memory-command',required=False,help='execute a command with output memory storage')
args = parser.parse_args()
if args.memory_command:
	memory_command(args.memory_command)
	exit(0)

# load key
try:
	key=open('openai_api_key.txt','r').read()
except:
	key=input('set your openai api key: ')
	with open('openai_api_key.txt','w') as f:
		f.write(key)
		f.close()

# run
msg=input(Fore.YELLOW+'input: '+Style.RESET_ALL)
memory_parts=1
try:
	_memory=open('memory.txt','r').read()
	memory=[_memory]
except:
	memory='''info: any memory yet

'''
if len(memory) > 50000:
	print(f'{Fore.BLUE}[info]{Style.RESET_ALL} huge prompt detected: spliting memory...')
	memory=split_memory()
	memory_parts=len(memory)
	print(f'{Fore.BLUE}[info]{Style.RESET_ALL} memory parts: {memory_parts}')
for part in range(memory_parts):
	reply=assisht(f'memory of conversation:\n{memory[part]}\n\nnew message: {msg}')
	reply=''.join(char for char in reply if not('\ud800' <= char <= '\udfff'))
	print(Fore.GREEN+'[assisht] '+Style.RESET_ALL+reply)
	with open('memory.txt','a') as f:
		f.write(f'input: {msg}\noutput: {reply}\n')
		f.close()
	sleep(1)
