from requests import post
from sys import exit

def assisht(msg):
	headers={"Authorization": f"Bearer {key}"}
	url="https://api.openai.com/v1/chat/completions"
	data={
		"model": "gpt-4o-mini",
 		"messages": [
		{
			"role": "system",
			"content": '''You should always analyze the memory of the conversation before answering, the answers have to make sense in terms of the memory of the conversation, as they may ask you or mention something that has been mentioned before in the next conversation.
You are assisht: a helpful assistant for iSH, always write in lower case and dont use any markdown like * or ```, ecc (when you give code too). Always return just simple plane text.
return just clean solutions and if the user ask about a command: 
returns just the command.
If the user ask you info about the command add:
- description:
- combo powerfull commands:
We are running iSH on iOS, you will take it into account when giving results. You are a powerful Cybersecurity wizard so you always give the best solutions, explaining in a straightforward way, never returning wrong data that you have not compared, analyzed and processed with real internet data.'''
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
try:
	key=open('openai_api_key.txt','r').read()
except:
	key=input('set your openai api key: ')
	with open('openai_api_key.txt','w') as f:
		f.write(key)
		f.close()
msg=input('input: ')
try:
	memory=open('memory.txt','r').read()
except:
	memory=''
reply=assisht(f'memory of conversation:{memory}\n\tnnew message: {msg}')
print('output: '+reply)
with open('memory.txt','a') as f:
	f.write(f'input: {msg}\noutput: {reply}')
	f.close()
