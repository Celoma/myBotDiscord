import discord
from discord.ext import commands
import ast
import function
import asyncio
import random

idToken = 'MTE4MjQyOTE5NTA4MzcxNDYzMQ.GgwGzc.UPu6HWyhgJXR1i4AtVeqAv79ucPyrY0JAc4onw'
prefix = '?'
intents = discord.Intents().all()
intents.message_content = True

client = commands.Bot(command_prefix=prefix, intents=intents)
blocked_users = {}

@client.command(name='classement')
async def classement(ctx):
    participant = []
    list_of_ids = [member.id for member in ctx.message.guild.members]
    with open("BotCisco/logQuiz.txt", "r") as f:
        jeu = f.readlines()
        for joueur in jeu:
            dataJoueur = ast.literal_eval(joueur)
            if dataJoueur['idAuthor'] in list_of_ids and dataJoueur['totalAns'] > 0:
                participant.append(dataJoueur)
    title = f"Classement Cisco"
    embed = discord.Embed(title=title, colour=discord.Colour.blue())
    max = 1
    participant = sorted(participant, key= lambda x: x['correctAns']/x['totalAns'], reverse=True)
    for joueur in participant:
        if max < 11:
            embed.add_field(name="Position " + str(max), value=f"`{client.get_user(joueur['idAuthor']).global_name}` avec :{joueur['correctAns']}/{joueur['totalAns']}  soit {(joueur['correctAns'] / joueur['totalAns']) *100}%", inline=max==1)
        max += 1
    embed.set_image(url = "https://newsroom.ibm.com/image/Cisco+Banner_1920x720.jpg")
    await ctx.reply(embed=embed)
            
            
@client.command(name='show')
async def show(ctx):
    with open("BotCisco/logQuiz.txt", "a+") as f:
        find = False
        f.seek(0)
        lines = f.readlines()
        for line in lines:
            d = ast.literal_eval(line)
            if d['idAuthor'] == ctx.author.id:
                find = True
                break
        if not find:
            d = {'idAuthor': ctx.author.id,
                 'correctAns': 0,
                 'totalAns': 0,
                 'currentQuestion': 0}
            f.write(str(d) + '\n')
    title = f"Certification Cisco"
    message_content = f"Voici ton score actuel : {d['correctAns']}/{d['totalAns']} soit {(d['correctAns'] / d['totalAns']) *100}%"
    embed = discord.Embed(title=title, description=message_content, colour=discord.Colour.blue())
    await ctx.reply(embed=embed)  
        
@client.command(name='reset')
async def reset(ctx):
       	d = {'idAuthor': ctx.author.id,
                 'correctAns': 0,
                 'totalAns': 0,
                 'currentQuestion': 0}
        with open("BotCisco/logQuiz.txt", "r+") as f:
            lines = f.readlines()
            f.seek(0)
            for i, line in enumerate(lines):
                saved_data = ast.literal_eval(line)
                if saved_data['idAuthor'] == ctx.author.id:
                    saved_data.update(d)
                    line = str(saved_data) + '\n'
                    lines[i] = line
                    break
            f.writelines(lines)
        await ctx.invoke(client.get_command('quiz'))
        
@client.command(name='quiz')
async def quiz(ctx, start = None):
    if ctx.author.id in blocked_users and blocked_users[ctx.author.id] > asyncio.get_event_loop().time():
        await ctx.reply("Tu dois attendre un peu avant de créer un autre canal privé.", mention_author=False)
        return
    blocked_users[ctx.author.id] = asyncio.get_event_loop().time() + 8
    category_name = 'train-cisco'
    category = discord.utils.get(ctx.guild.categories, name=category_name)
    existing_channel = discord.utils.find(lambda c: c.category == category and str(c.topic) == str(ctx.author.id), ctx.guild.text_channels)

    if existing_channel:
        await existing_channel.delete()
    
    if not category:
        category = await ctx.guild.create_category(category_name)

    overwrites = {
        ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
        ctx.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        ctx.author: discord.PermissionOverwrite(read_messages=True, send_messages=True),
    }
    
    channel = await ctx.guild.create_text_channel(f'Quiz Cisco de {ctx.author.display_name}', overwrites=overwrites, category=category, topic=str(ctx.author.id))
    await channel.send(f"Création de ton canal privé ! " + ctx.author.mention)
    
    with open("BotCisco/logQuiz.txt", "a+") as f:
        find = False
        f.seek(0)
        lines = f.readlines()
        for line in lines:
            d = ast.literal_eval(line)
            if d['idAuthor'] == ctx.author.id:
                find = True
                break
        if not find:
            d = {'idAuthor': ctx.author.id,
                 'correctAns': 0,
                 'totalAns': 0,
                 'currentQuestion': 0}
            f.write(str(d) + '\n')


    data = function.questionCisco()
    try:
        d['currentQuestion'] = int(start) % len(data)
    except:
        pass
    while True:
        current_question = data[d['currentQuestion']]
        message_content = f"**{current_question[0]}**\n\n"
        bonneReponse = []
        title = f"Certification Cisco : Score actuel {d['correctAns']}/{d['totalAns']}"
		
        if isinstance(current_question[-1], dict):
            v = current_question[1:-1]
            random.shuffle(v)
            current_question = [current_question[0]] + v + [current_question[-1]]
            for i in range(1, len(current_question) - 1):
                if 'Correct' in current_question[i][2:]:
                    bonneReponse.append(i)
                    message_content += f"{i}\u20e3 . {current_question[i][2:].split('(Correct)')[0]}\n"
                else:
                    message_content += f"{i}\u20e3 . {current_question[i][2:]}\n"
            embed = discord.Embed(title=title, description=message_content, colour=discord.Colour.blue())
            embed.set_image(url=current_question[-1]['URL'])
        elif d['currentQuestion'] == 24:
                v = current_question[1:]
                random.shuffle(v)
                current_question = [current_question[0]] + v
                for i in range(1, len(current_question)):
                    if 'Correct' in current_question[i][2:]:
                        bonneReponse.append(i)
                        message_content += f"{i}\u20e3 . {current_question[i][2:].split('(Correct)')[0]}\n"
                    else:
                        message_content += f"{i}\u20e3 . {current_question[i][2:]}\n"
                d['currentQuestion'] += 1
                message_content += f"\n**{data[d['currentQuestion']][0][9:]}**\n\n"
                for i in range(1, len(data[d['currentQuestion']])):
                    message_content += f"{i}\u20e3 . {data[d['currentQuestion']][i][2:]}\n"
                embed = discord.Embed(title=title, description=message_content, colour=discord.Colour.blue())
        elif d['currentQuestion'] == 107:
            bonneReponse.append(3)
            correctValue = [1, 3, 5, 6]
            for i in range(4):
                message_content += f"{i + 1}\u20e3 . {current_question[correctValue[i]][2:]}\n"
            embed = discord.Embed(title=title, description=message_content, colour=discord.Colour.blue())
            i += 1
       	else:
            v = current_question[1:]
            random.shuffle(v)
            current_question = [current_question[0]] + v
            for i in range(1, len(current_question)):
                if 'Correct' in current_question[i][2:]:
                    bonneReponse.append(i)
                    message_content += f"{i}\u20e3 . {current_question[i][2:].split('(Correct)')[0]}\n"
                else:
                    message_content += f"{i}\u20e3 . {current_question[i][2:]}\n"

            embed = discord.Embed(title=title, description=message_content, colour=discord.Colour.blue())

        message = await channel.send(embed=embed)
        optionReaction = ['❌','➡️']
        
        question_end = False
        Lreactions = []                
        async def react():
            for number in range(i):
                optionReaction.append(f"{number + 1}\u20e3")
                await message.add_reaction(f"{number + 1}\u20e3")
            await message.add_reaction("❌")
            await message.add_reaction("➡️")
        await react()
        while not question_end:
                    def check(reaction, user):
                        check1 = user == ctx.author
                        check2 = reaction.message.channel == channel
                        check3 = reaction.emoji in optionReaction
                        return (check1 and check2 and check3)
                    reaction, user = await client.wait_for('reaction_add', check=check)
                    if reaction.emoji == '❌':
                        await channel.delete()
                    elif reaction.emoji == '➡️':
                        question_end = True
                        d['currentQuestion'] = (d['currentQuestion'] + 1) % len(data)
                    else:
                        Lreactions.append(int(reaction.emoji[0]))
                        if len(Lreactions) == len(bonneReponse):
                            question_end = True
                            mauvaiseReponse = 0
                            show = []
                            plotTwist = ""
                            d['currentQuestion'] = (d['currentQuestion'] + 1) % len(data)

                            for correct in bonneReponse:
                                d['totalAns'] += 1
                                if correct in Lreactions:
                                    d['correctAns'] += 1
                                    plotTwist += current_question[correct][3:-9] + "\n"
                                else:
                                    if mauvaiseReponse == 0:
                                        title = "Incorrect ! :disappointed_relieved:"
                                        message_content = "**Voici les réponses qu'il te manquaient :**\n\n"
                                    mauvaiseReponse += 1
                                    message_content += current_question[correct][3:-9] + "\n"

                            if mauvaiseReponse == 0:
                                title = "Correct ! :tada:"
                                message_content = ""
                            elif mauvaiseReponse < len(bonneReponse):
                                message_content += "\n**Tu avais quand même trouvé :**\n\n" + plotTwist

                            embed = discord.Embed(title=title, description=message_content, colour=discord.Colour.blue())
                            await channel.send(embed=embed)
                
        with open("BotCisco/logQuiz.txt", "r+") as f:
            lines = f.readlines()
            f.seek(0)
            for i, line in enumerate(lines):
                saved_data = ast.literal_eval(line)
                if saved_data['idAuthor'] == ctx.author.id:
                    saved_data.update(d)
                    line = str(saved_data) + '\n'
                    lines[i] = line
                    break
            f.writelines(lines)
client.run(idToken)
