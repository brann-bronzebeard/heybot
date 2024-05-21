import discord
from discord.ext import commands
import requests
from openai import OpenAI


# vars go here


# client = OpenAI()
localClient = OpenAI(base_url=LM_STUDIO_API_URL, api_key="lm-studio")

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())


message_history = []

#a simpler 'ask gpt3' for simpler commands
def askGpt3(prompt, context=None):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Your responses should be concise, relevant to the conversation, and at the right times, and have a subtly cynical jaded attitude"
            },
            {"role": "user", "content": f'''acting as the ai in this conversation, generate your next response:
            {context} {prompt}'''}
            #the 

        ]
    )
    return completion.choices[0].message.content


def askGpt4(prompt, context=None):
    completion = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": """You are an AI assistant in a Discord server. Your responses should be concise, relevant to the conversation. Your responses should be no more than one or two sentences, unless necessary."""
            },
            {"role": "user", "content": f'''acting as the ai in this conversation, generate your next response:
            {context} {prompt}'''}
            #the 

        ]
    )
    return completion.choices[0].message.content

def getBoolResponse(prompt):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": """You are an AI assistant in a Discord server, and in this instance, responding with ONLY 'True' or 'False' given the prompt."""
            },
            {"role": "user", "content": f'''prompt: {prompt}'''}
            #the 

        ]
    )
    return completion.choices[0].message.content



#bots
async def callLocalLLM(prompt):
    #call the local LM Studio server at http://localhost:1234/v1/chat/completion, just as you would with open ai
    # Example: reuse your existing OpenAI setup
    completion = localClient.chat.completions.create(
        model="model-identifier",
        messages=[
            # {"role": "system", "content": "Always answer in rhymes."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
    )
    return completion.choices[0].message.content


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    channel = bot.get_channel(CHANNEL_ID)
    return

@bot.event
async def on_message(after):
    message_history.append(f'{after.author.name}: {after.content}')
    if len(message_history) > 100:
        message_history.pop(0)

    # if after.author == bot.user:
    #     return

    # lowercase first 20 chars of message
    firstchars = after.content[:20].lower()


    if 'hey bot' in firstchars or 'heybot' in firstchars or 'heyboy' in firstchars or 'hey computer' in firstchars:
        async with after.channel.typing():

            # response = askGpt3(after.content, message_history)
            # response = askGpt4(after.content, message_history)
            # response = getBoolResponse(after.content)
            response = await callLocalLLM(after.content)

            #convert the response to a boolean
            # response = response.lower().strip() == 'true'
            await after.channel.send(response)


bot.run(TOKEN)