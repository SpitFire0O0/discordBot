#======================================================================================================
#                                                                                                      
#   Bot NAME: Matcyouka                                                                  
#                                                                                                          
#                                                                             [bot for: discord server]
#===============================================IMPORTS===============================================

import random 
import json 
import os
import io
import nekos 
import time
import datetime
import discord
from discord.ext import commands
from discord.utils import get 
import requests
from PIL import Image, ImageFont, ImageDraw 

#==============================================MASSIVES================================================
#
bad_words = [] # Filter listg
queue = [] # CD List  
#
#======================================================================================================

intents = discord.Intents.all()

with open('data/settings.json', 'r') as f:
	dataSetPrefix = json.load(f)

PREFIX = dataSetPrefix['prefix']
client = commands.Bot(command_prefix = PREFIX, intents = intents) #
client.remove_command('help') # Удаление команды help

@client.event
async def on_ready():
	print('BOT connected...') # Проверка на подключение 

	await client.change_presence(status = discord.Status.online, activity = discord.Game(f'{PREFIX}help')) # Статус бота

#==============================================NEW USERS==============================================

@client.event
async def on_member_join(member):
	channelsadg = client.get_channel(844136766901321738)  # id чата (welcome)

	emb = discord.Embed(color = 0x44ff33, description = f':raised_hand: Добро пожаловать на сервер, {member.mention}! :tada:')
	await channelsadg.send(embed = emb)

#======================================================================================================

@client.event 
async def on_message(message):
	await client.process_commands(message)

# ERRORS
@client.event
async def on_command_error(ctx, error):
	pass

#=============================================MOD COMMANDS=============================================

#       MODER_COMMAND:
# 
# CLEAR
@client.command(aliases = ['clr', 'cl', 'c'])
@commands.has_permissions(administrator = True)
async def clear(ctx, amount : int):
	await ctx.channel.purge(limit = amount)
	await ctx.send(embed = discord.Embed(description = f':white_check_mark: Удалено {amount} сообщений.', color = 0x00ff00))

# MUTE
@client.command(aliases = ['mt', 'm'])
@commands.has_permissions(administrator = True)
async def mute(ctx, member: discord.Member, time : int, reason):
	if ctx.channel.id == 843947523982229505:
		await ctx.channel.purge(limit = 1)
		muterole = discord.utils.get(ctx.guild.roles, id = 844139122502402071)
		await ctx.send(embed = discord.Embed(description = f':white_check_mark: Модератор: {ctx.author.mention}, дал мут участнику: {member.mention}, на **{time}** мин. :mute:', color = 0x00ff00))
		await member.send(f'{member.mention}, вы получили мут на сервере, модератором: {ctx.author.mention}, на {time} мин!')
		await member.add_roles(muterole)
		await asyncio.sleep(time * 60)
		await member.remove_roles(muterole) 
	else:
		await ctx.author.send(embed = discord.Embed(description = f'Эту команду можно использовать только в канале - #**console**', color = 0x00ff00)) 

# UNMUTE
@client.command(aliases = ['um', 'umt'])
@commands.has_permissions(administrator = True)
async def unmute(ctx, member: discord.Member):
	if ctx.channel.id == 843947523982229505:
		await ctx.channel.purge(limit = 1)
		muterole = discord.utils.get(ctx.guild.roles, id = 844139122502402071)
		await ctx.send(embed = discord.Embed(description = f':white_check_mark: Модератор: {ctx.author.mention}, снял мут с участника сервера: {member.mention}', color = 0x00ff00))
		await member.send(f'{member.mention}, с вас успешно снят мут, модератором: {ctx.author.mention}!')
		await member.remove_roles(muterole)
	else:
		await ctx.author.send(embed = discord.Embed(description = f'Эту команду можно использовать только в канале - #**console**', color = 0x00ff00)) 

# KICK
@client.command(aliases = ['kc', 'k'])
@commands.has_permissions(administrator = True)
async def kick(ctx, member: discord.Member, *, reason = None):
	if ctx.channel.id == 843947523982229505:
		await ctx.channel.purge(limit = 1)
		await member.kick(reason = reason)
		await ctx.send(embed = discord.Embed(description = f':white_check_mark: Участник: {member.mention} успешно раззабанен на сервере, модератором {ctx.author.mention}!', color = 0x00ff00))
		await member.send(f'{member.mention}, вас исключил с сервера: {ctx.author.mention}!') 
	else:
		await ctx.author.send(embed = discord.Embed(description = f'Эту команду можно использовать только в канале - #**console**', color = 0x00ff00)) 

# BAN
@client.command(aliases = ['b'])
@commands.has_permissions(administrator = True)
async def ban(ctx, member: discord.Member, *, reason = None):
	if ctx.channel.id == 843947523982229505:
		await ctx.channel.purge(limit = 1)
		await member.ban(reason = reason)
		await ctx.send(embed = discord.Embed(description = f':white_check_mark: Участник: {member.mention} успешно забанен на сервере, модератором {ctx.author.mention}!', color = 0xff0000))
		await member.send(f'{member.mention}, вас забанил на сервере: {ctx.author.mention}!') 
	else:
		await ctx.author.send(embed = discord.Embed(description = f'Эту команду можно использовать только в канале - #**console**', color = 0x00ff00)) 

# UNBAN
@client.command(aliases = ['unb', 'ub'])
@commands.has_permissions(administrator=True)
async def unban(ctx, *, member):
	if ctx.channel.id == 843947523982229505:
		banned_users = await ctx.guild.bans()
		await ctx.channel.purge(limit=1)
		for ban_entry in banned_users:
			user = ban_entry.user
			await ctx.guild.unban(user)
			await ctx.send(embed = discord.Embed(description = f':white_check_mark: Участник: {member.mention} успешно раззбанен на сервере, модератором {ctx.author.mention}!', color = 0xff0000))
			await member.send(f'{member.mention}, вас разбанил на сервере: {ctx.author.mention}!')
	else:
		await ctx.author.send(embed = discord.Embed(description = f'Эту команду можно использовать только в канале - #**console**', color = 0x00ff00)) 
#
#       GIVEN_MODS         
#
# VIP
@client.command(aliases = ['gv', 'gvip'])
@commands.has_permissions(administrator = True)
async def vip(ctx, member: discord.Member):
	await ctx.channel.purge(limit = 1)
	if ctx.channel.id == 843947523982229505:
		modrole = discord.utils.get(ctx.guild.roles, id = 843963582013112323)
		emb = discord.Embed(title = 'VIP            :white_check_mark:', color = 0x00ff00)
		emb.add_field(name = 'Уастника:', value = member.mention, inline = False)
		emb.add_field(name = 'Модератором: ', value = ctx.message.author.mention, inline = False)
		await member.send(f'{member.mention}, выдана vip-роль, участником: {ctx.author.mention}!')
		await member.add_roles(modrole)
		await ctx.send(embed = emb)
	else:
		await ctx.author.send(embed = discord.Embed(description = f'Эту команду можно использовать только в канале - #**console**', color = 0x00ff00)) 

# DeVIP
@client.command()
@commands.has_permissions(administrator = True)
async def devip(ctx, member: discord.Member):
	await ctx.channel.purge(limit = 1)
	if ctx.channel.id == 843947523982229505:
		modrole = discord.utils.get(ctx.guild.roles, id = 843963582013112323)
		emb = discord.Embed(title = 'De VIP     :white_check_mark:', color = 0xff0000)
		emb.add_field(name = 'Уастника:', value = member.mention, inline = False)
		emb.add_field(name = 'Модератором: ', value = ctx.message.author.mention, inline = False)
		await member.send(f'{member.mention}, забрана выдана vip-роль, участником: {ctx.author.mention}!')
		await member.remove_roles(modrole)
		await ctx.send(embed = emb) 
	else:
		await ctx.author.send(embed = discord.Embed(description = f'Эту команду можно использовать только в канале - #**console**', color = 0x00ff00)) 

# MOD
@client.command(aliases = ['gm', 'gmod'])
@commands.has_permissions(administrator = True)
async def mod(ctx, member: discord.Member):
	await ctx.channel.purge(limit = 1)
	if ctx.channel.id == 843947523982229505:
		modrole = discord.utils.get(ctx.guild.roles, id = 843963704693096470)
		emb = discord.Embed(title = 'MOD            :white_check_mark:', color = 0x00ff00)
		emb.add_field(name = 'Уастника:', value = member.mention, inline = False)
		emb.add_field(name = 'Модератором: ', value = ctx.message.author.mention, inline = False)
		await member.send(f'{member.mention}, выданы права модератора, участником: {ctx.author.mention}!')
		await member.add_roles(modrole)
		await ctx.send(embed = emb)
	else:
		await ctx.author.send(embed = discord.Embed(description = f'Эту команду можно использовать только в канале - #**console**', color = 0x00ff00)) 

# DeMOD
@client.command()
@commands.has_permissions(administrator = True)
async def demod(ctx, member: discord.Member):
	await ctx.channel.purge(limit = 1)
	if ctx.channel.id == 843947523982229505:
		modrole = discord.utils.get(ctx.guild.roles, id = 843963704693096470)
		emb = discord.Embed(title = 'De MOD     :white_check_mark:', color = 0xff0000)
		emb.add_field(name = 'Уастника:', value = member.mention, inline = False)
		emb.add_field(name = 'Модератором: ', value = ctx.message.author.mention, inline = False)
		await member.send(f'{member.mention}, забраны права модератора, участником: {ctx.author.mention}!')
		await member.remove_roles(modrole)
		await ctx.send(embed = emb) 
	else:
		await ctx.author.send(embed = discord.Embed(description = f'Эту команду можно использовать только в канале - #**console**', color = 0x00ff00)) 

# OP
@client.command(aliases = ['go', 'gop'])
@commands.has_permissions(administrator = True)
async def op(ctx, member: discord.Member):
	await ctx.channel.purge(limit = 1)
	if ctx.channel.id == 843947523982229505:
		modrole = discord.utils.get(ctx.guild.roles, id = 843963752071430165)
		emb = discord.Embed(title = 'OP                 :white_check_mark:', color = 0xffd700)
		emb.add_field(name = 'Уастника:', value = member.mention, inline = False)
		emb.add_field(name = 'Модератором: ', value = ctx.message.author.mention, inline = False)
		await member.send(f'{member.mention}, выданы права администратора, участником: {ctx.author.mention}!')
		await member.add_roles(modrole)
		await ctx.send(embed = emb)
	else:
		await ctx.author.send(embed = discord.Embed(description = f'Эту команду можно использовать только в канале - #**console**', color = 0x00ff00)) 

# DeOP
@client.command()
@commands.has_permissions(administrator = True)
async def deop(ctx, member: discord.Member):
	await ctx.channel.purge(limit = 1)
	if ctx.channel.id == 843947523982229505:
		modrole = discord.utils.get(ctx.guild.roles, id = 843963752071430165)
		emb = discord.Embed(title = 'De OP          :white_check_mark:', color = 0xff0000)
		emb.add_field(name = 'Уастника:', value = member.mention, inline = False)
		emb.add_field(name = 'Модератором: ', value = ctx.message.author.mention, inline = False)
		await member.send(f'{member.mention}, забраны права администратора, участником: {ctx.author.mention}!')
		await member.remove_roles(modrole)
		await ctx.send(embed = emb)
	else:
		await ctx.author.send(embed = discord.Embed(description = f'Эту команду можно использовать только в канале - #**console**', color = 0x00ff00)) 

# Given Role
@client.command(aliases = ['gr'])
@commands.has_permissions(administrator = True)
async def givenrole(ctx, member: discord.Member, role: discord.Role):
	if ctx.channel.id == 843947523982229505:
		await member.add_roles(role)
		await ctx.send(embed = discord.Embed(description = f':white_check_mark: Участнику **{member.name}**, была выдана роль **{role}**, модератором {ctx.author.mention}', color = 0x00ff00))
	else:
		await ctx.author.send(embed = discord.Embed(description = f'Эту команду можно использовать только в канале - #**console**', color = 0x00ff00)) 

#============================================USR COMMANDS============================================

# HELP
@client.command(aliases = ['h'])
async def help(ctx):
	await ctx.message.delete() # auto-delete usr message

	emb = discord.Embed(title = 'Информация по командам бота', color = 0x00ff00, description = f'{ctx.author.mention}')  
	emb.add_field(name = f'{PREFIX}helpoth  :diamond_shape_with_a_dot_inside:', value = 'Список прочих команд')
	emb.add_field(name = f'{PREFIX}helpmod  :tools:', value = 'Список всех команд для модераторов.')
	emb.add_field(name = f'{PREFIX}helpset  :gear:', value = 'Список всех команд управления сервера')
	emb.add_field(name = f'{PREFIX}helpeconomy  :scales:', value = 'Список всех команд экономики')
	emb.add_field(name = f'{PREFIX}helpcalc  :desktop:', value = 'Список всех команд калькулятора')

	await ctx.author.send(embed = emb)

# HELP Other
@client.command(aliases = ['ho', 'helpo'])
async def helpoth(ctx):
	await ctx.message.delete()

	emb = discord.Embed(title = 'Список прочих команд сервера', color = 0x00ff00, description = f'{ctx.author.mention}') 
	emb.add_field(name = f'{PREFIX}help', value = 'Информация по командам бота')
	emb.add_field(name = f'{PREFIX}helpoth', value = 'Список **прочих** команд')
	emb.add_field(name = f'{PREFIX}helpmod', value = 'Список всех команд для **модераторов**')
	emb.add_field(name = f'{PREFIX}helpeconomy', value = 'Список всех команд **экономики**')
	emb.add_field(name = f'{PREFIX}helpcalc', value = 'Список всех команд **калькулятора**')

	emb.add_field(name = f'{PREFIX}usercard @user', value = 'Личная карта участника сервера') 
	emb.add_field(name = f'{PREFIX}time', value = 'Узнать время')
	emb.add_field(name = f'{PREFIX}msgusr @user str', value = 'Личное сообщение пользователю через бота')
	emb.add_field(name = f'{PREFIX}say str', value = 'Личное сообщение пользователю через бота')
	emb.add_field(name = f'{PREFIX}coin value int ', value = 'Личное сообщение пользователю через бота; value: орёл/решка')

	emb.add_field(name = f'{PREFIX}shop', value = 'Магазин сервера')
	emb.add_field(name = f'{PREFIX}buy @role', value = 'Купить роль')
	emb.add_field(name = f'{PREFIX}work', value = 'Работать')
	emb.add_field(name = f'{PREFIX}crime @user', value = 'Украсть деньги у участника')
	emb.add_field(name = f'{PREFIX}givemoney @user', value = 'Перечислить кредиты участнику сервера')
	emb.add_field(name = f'{PREFIX}balance @user', value = 'Узнать баланс')
	#emb.footer(text = '@role - тег участника; @role - тег роли; int - число; str - сообщение/текст')

	await ctx.author.send(embed = emb)

# HELP Set
@client.command(aliases = ['hs', 'helps'])
async def helpset(ctx):
	await ctx.message.delete()

	emb = discord.Embed(title = 'Список всех команд управления сервера', color = 0x00ff00, description = f'{ctx.author.mention}') 
	emb.add_field(name = f'{PREFIX}setprefix str [MOD]', value = 'Удаление последних сообщений')
	emb.add_field(name = f'{PREFIX}minwork int [MOD]', value = 'Установка минимальной выдачи кредитов за работу')
	emb.add_field(name = f'{PREFIX}maxwork int [MOD]', value = 'Установка максимальной выдачи кредитов за работу')
	emb.add_field(name = f'{PREFIX}mincrime int [MOD]', value = 'Установка минимальной выдачи кредитов за кражу')
	emb.add_field(name = f'{PREFIX}maxcrime int [MOD]', value = 'Установка максимальной выдачи кредитов за кражу')
	emb.add_field(name = f'{PREFIX}mincoin int [MOD]', value = 'Установка минимальной ставки на монетку')
	emb.add_field(name = f'{PREFIX}maxcoin int [MOD]', value = 'Установка максимальной ставки на монетку')
	emb.add_field(name = f'{PREFIX}setgivenexp int [MOD]', value = 'Установка выдаваемой exp за сообщение (float ~ 0.n)')
	emb.add_field(name = f'{PREFIX}setkdwork int [MOD]', value = 'Установка КД между **работой** (мин)')
	emb.add_field(name = f'{PREFIX}setkdcoin int [MOD]', value = 'Установка КД между **COIN** (мин)')
	emb.add_field(name = f'{PREFIX}setcrimeprc int [MOD]', value = 'Установка успешного шанса кражи в %')
	emb.add_field(name = f'{PREFIX}setcrimecf int [MOD]', value = 'Установка наказания за кражу')
	#emb.footer(text = 'int - число; str - сообщение/текст')

	await ctx.author.send(embed = emb)

# HELP Mod
@client.command(aliases = ['hm', 'helpm'])
async def helpmod(ctx):
	await ctx.message.delete()

	emb = discord.Embed(title = 'Список всех команд модераторов', color = 0x00ff00, description = f'{ctx.author.mention}') 
	emb.add_field(name = f'{PREFIX}clear int [MOD]', value = 'Удаление последних сообщений')
	emb.add_field(name = f'{PREFIX}kick @user [MOD]', value = 'Исключения участника с сервера')
	emb.add_field(name = f'{PREFIX}ban @user [MOD]', value = 'Выдача бана участнику')
	emb.add_field(name = f'{PREFIX}unban @user [MOD]', value = 'Разбан участника сервера')
	emb.add_field(name = f'{PREFIX}mute @user [MOD]', value = 'Выдача мута участнику сервера')
	emb.add_field(name = f'{PREFIX}unmute @user [MOD]', value = 'Размут участника сервера')

	emb.add_field(name = f'{PREFIX}givenrole @user @role [MOD]', value = 'Выдача роли участнику сервера')
	emb.add_field(name = f'{PREFIX}mod @user [MOD]', value = 'Выдача прав **модератора** участнику сервера')
	emb.add_field(name = f'{PREFIX}unmod @user [MOD]', value = 'Удаление прав **модератора** у участника сервера')
	emb.add_field(name = f'{PREFIX}op @user [MOD]', value = 'Выдача прав **администратора** участнику сервера')
	emb.add_field(name = f'{PREFIX}deop @user [MOD]', value = 'Удаление прав **администратора** у участника сервера')
	emb.add_field(name = f'{PREFIX}vip @user [MOD]', value = 'Выдача прав **vip** участнику сервера')
	emb.add_field(name = f'{PREFIX}devip @user [MOD]', value = 'Удаление прав **vip** у участника сервера')

	emb.add_field(name = f'{PREFIX}addshop @role int [MOD]', value = 'Добавление роли в магазин')
	emb.add_field(name = f'{PREFIX}removeshop @role [MOD]', value = 'Удаление роли из магазина') 
	emb.add_field(name = f'{PREFIX}addbalance @user int [MOD]', value = 'Добавить участнику кредитов') 
	emb.add_field(name = f'{PREFIX}removebalance @user int [MOD]', value = 'Забрать у участника кредиты') 
	emb.add_field(name = f'{PREFIX}enterbalance @user int [MOD]', value = 'Установить участнику кредиты')
	#emb.footer(text = '@role - тег участника; @role - тег роли; int - число; str - сообщение/текст')

	await ctx.author.send(embed = emb)

# HELP Calc
@client.command(aliases = ['hc', 'helpc'])
async def helpcalc(ctx):
	await ctx.message.delete()

	emb = discord.Embed(title = 'Список всех команд калькулятора', colour = discord.Color.orange(), description = f'{ctx.author.mention}') 
	emb.add_field(name = f'{PREFIX}add a b', value = 'Сложение')
	emb.add_field(name = f'{PREFIX}sub a b', value = 'Вычитание')
	emb.add_field(name = f'{PREFIX}mlt a b', value = 'Умножение')
	emb.add_field(name = f'{PREFIX}stp a b', value = 'Степень')
	emb.add_field(name = f'{PREFIX}divn a b', value = 'Деление')
	emb.add_field(name = f'{PREFIX}div a b', value = 'Целочисленное деление')
	emb.add_field(name = f'{PREFIX}dev a b', value = 'Остаток от деления')
	#emb.footer(text = 'a, b - число')

	await ctx.author.send(embed = emb) 

# HELP Economic
@client.command(aliases = ['he', 'helpe'])
async def helpeconomy(ctx):
	await ctx.message.delete()

	emb = discord.Embed(title = 'Список всех команд экономики', color = 0x00ff00, description = f'{ctx.author.mention}') 
	emb.add_field(name = f'{PREFIX}addshop @role int [MOD]', value = 'Добавление роли в магазин')
	emb.add_field(name = f'{PREFIX}removeshop @role [MOD]', value = 'Удаление роли из магазина') 
	emb.add_field(name = f'{PREFIX}addbalance @user int [MOD]', value = 'Добавить участнику кредитов') 
	emb.add_field(name = f'{PREFIX}removebalance @user int [MOD]', value = 'Забрать у участника кредиты') 
	emb.add_field(name = f'{PREFIX}enterbalance @user int [MOD]', value = 'Установить участнику кредиты')  
	emb.add_field(name = f'{PREFIX}givemoney @user int', value = 'Перечислить участнику свои кредиты')
	emb.add_field(name = f'{PREFIX}work', value = 'Работать')
	emb.add_field(name = f'{PREFIX}crime @user', value = 'Попытаться обокрасть участника сервера')
	emb.add_field(name = f'{PREFIX}balance @user', value = 'Посмотреть баланс участника сервера')
	emb.add_field(name = f'{PREFIX}shop', value = 'Список всех ролей магазина')
	emb.add_field(name = f'{PREFIX}buy', value = 'Купить роль')
	emb.footer(text = '@role - тег участника; @role - тег роли; int - число')

	await ctx.author.send(embed = emb)

# Calculator
def calculator():
	@client.command() 
	async def add(ctx, *nums): # Сложение
		if ctx.channel.id == 843947523982229505:
			oper = " + ".join(nums)
			emb = discord.Embed(title = f'{oper} = {eval(oper)}', color = 0x483D8B, description = f'{ctx.author.mention}')
			await ctx.send(embed = emb)
		else:
			await ctx.author.send(embed = discord.Embed(description = f'Эту команду можно использовать только в канале - #**console**', color = 0x00ff00)) 
	@client.command() 
	async def sub(ctx, *nums): # Вычитание
		if ctx.channel.id == 843947523982229505:
			oper = " - ".join(nums)
			emb = discord.Embed(title = f'{oper} = {eval(oper)}', color = 0x483D8B, description = f'{ctx.author.mention}')
			await ctx.send(embed = emb)
		else:
			await ctx.author.send(embed = discord.Embed(description = f'Эту команду можно использовать только в канале - #**console**', color = 0x00ff00)) 
	@client.command() 
	async def mlt(ctx, *nums): # Умножение
		if ctx.channel.id == 843947523982229505:
			oper = " * ".join(nums)
			emb = discord.Embed(title = f'{oper} = {eval(oper)}', color = 0x483D8B, description = f'{ctx.author.mention}')
			await ctx.send(embed = emb)
		else:
			await ctx.author.send(embed = discord.Embed(description = f'Эту команду можно использовать только в канале - #**console**', color = 0x00ff00)) 
	@client.command() 
	async def stp(ctx, *nums): # Умножение
		if ctx.channel.id == 843947523982229505:
			oper = " ** ".join(nums)
			emb = discord.Embed(title = f'{oper} = {eval(oper)}', color = 0x483D8B, description = f'{ctx.author.mention}')
			await ctx.send(embed = emb)
		else:
			await ctx.author.send(embed = discord.Embed(description = f'Эту команду можно использовать только в канале - #**console**', color = 0x00ff00)) 
	@client.command() 
	async def divn(ctx, *nums): # Деление
		if ctx.channel.id == 843947523982229505:
			oper = " / ".join(nums)
			emb = discord.Embed(title = f'{oper} = {eval(oper)}', color = 0x483D8B, description = f'{ctx.author.mention}')
			await ctx.send(embed = emb)
		else:
			await ctx.author.send(embed = discord.Embed(description = f'Эту команду можно использовать только в канале - #**console**', color = 0x00ff00)) 
	@client.command() 
	async def div(ctx, *nums): # Целочисленное деление
		if ctx.channel.id == 843947523982229505:
			oper = " // ".join(nums)
			emb = discord.Embed(title = f'{oper} = {eval(oper)}', color = 0x483D8B, description = f'{ctx.author.mention}')
			await ctx.send(embed = emb)
		else:
			await ctx.author.send(embed = discord.Embed(description = f'Эту команду можно использовать только в канале - #**console**', color = 0x00ff00)) 
	@client.command() 
	async def dev(ctx, *nums): # Остаток от деления
		if ctx.channel.id == 843947523982229505:
			oper = " % ".join(nums)
			emb = discord.Embed(title = f'{oper} = {eval(oper)}', color = 0x483D8B, description = f'{ctx.author.mention}')
			await ctx.send(embed = emb)
		else:
			await ctx.author.send(embed = discord.Embed(description = f'Эту команду можно использовать только в канале - #**console**', color = 0x00ff00)) 

calculator()

# Coin
@client.command()
async def coin(ctx, arg, credite):
	if ctx.channel.id == 843947523982229505:
		with open('data/economy.json', 'r') as f:
			data = json.load(f)
		with open('data/settings.json', 'r') as f:
				dataSet = json.load(f)
		MinCoin = dataSet['mincoin']
		MaxCoin = dataSet['maxcoin']
		coin_massive = ['решка', 'орёл']
		if (int(credite) < MinCoin) or (int(credite) > MaxCoin):
			await ctx.send(embed = discord.Embed(description = f':no_entry_sign: Ошибка! Ставка должна быть не менее **{MinCoin}** и не более **{MaxCoin}**', color = 0xff0000))
		else:
			bal = data[str(ctx.author.id)]['money']
			if int(credite) < int(bal):
				coin_result = random.choice(coin_massive)
				if arg == coin_result:
					await ctx.send(embed = discord.Embed(description = f'Вам выпал(а): **{coin_result}** :coin:, ты победили и получил на счёт **{str(credite)}** :dollar: !!! :tada:', color = 0x00ff00))  
					data[str(ctx.author.id)]['money'] += int(credite)
					with open('data/economy.json', 'w') as f:
						json.dump(data, f, sort_keys = True, indent = 4)
				else:
					await ctx.send(embed = discord.Embed(description = f'Вам выпал(а): **{coin_result}** :coin:, ты проиграл! С твоего счёта снято **{str(credite)}** :dollar: ... :man_shrugging: ЛУУУУУЗЕР...', color = 0xff0000))
					data[str(ctx.author.id)]['money'] -= int(credite)
					with open('data/economy.json', 'w') as f:
						json.dump(data, f, sort_keys = True, indent = 4)
			else:
				await ctx.send(embed = discord.Embed(description = f':no_entry_sign: Ошибка! У вас недостаточно кредитов, ваш баланс состовляет {bal} :dollar:', color = 0xff0000))
	else:
		await ctx.author.send(embed = discord.Embed(description = f'Эту команду можно использовать только в канале - #**console**', color = 0x00ff00)) 

# Time
@client.command(aliases = ['t'])
async def time(ctx):
	await ctx.message.delete()
	if ctx.channel.id == 843947523982229505:
		now_date = datetime.datetime.now()
		emb = discord.Embed(title = 'Время: ', description = '{}'.format(now_date)[:16],color = 0x00ff00)
		emb.set_author(name = client.user.name, icon_url = client.user.avatar_url)
		await ctx.send(embed = emb)
	else:
		await ctx.author.send(embed = discord.Embed(description = f'Эту команду можно использовать только в канале - #**console**', color = 0x00ff00)) 

# Message for user
@client.command(aliases = ['msgusr', 'msgu', 'mu'])
async def msgUsr(ctx, member: discord.Member, arg):
	await ctx.message.delete()
	await member.send(f'{member.mention}, {ctx.author.name} пишет вам: {arg}') 

# Crad user
@client.command(aliases = ['uc', 'ucard', 'usrc', 'cardusr', 'cu', 'cardu', 'cusr'])
async def usrcard(ctx, member: discord.Member = None, guild: discord.Guild = None):
	await ctx.message.delete()
	if ctx.channel.id == 843947523982229505:
		if member == None:
			emb = discord.Embed(title = f'Карта участника {ctx.message.author.name}', color = 0x44ff33)
			emb.add_field(name = 'Аккаунт создан:', value = '{}'.format(ctx.message.author.created_at)[:16], inline = False)
			emb.add_field(name = 'Присоеденился: ', value = '{}'.format(ctx.message.author.joined_at)[:16], inline = False)
			emb.add_field(name = 'Активность:', value = ctx.message.author.activity, inline = True)
			emb.add_field(name = 'Статус:', value = ctx.message.author.status, inline = True)
			emb.add_field(name = 'Имя: ', value = ctx.message.author.display_name, inline = True)
			emb.add_field(name = 'Айди: ', value = ctx.message.author.id, inline = True)
			emb.add_field(name = 'Тег: ', value = ctx.message.author.mention, inline = True)
			emb.set_thumbnail(url = ctx.message.author.avatar_url)
			await ctx.send(embed = emb)
		else:
			emb = discord.Embed(title = f'Карта участника {member.name}', color = 0x44ff33)
			emb.add_field(name = 'Аккаунт создан:', value = '{}'.format(member.created_at)[:16], inline = False)
			emb.add_field(name = 'Присоеденился: ', value = '{}'.format(member.joined_at)[:16], inline = False)
			emb.add_field(name = 'Активность:', value = member.activity, inline = True)
			emb.add_field(name = 'Статус:', value = member.status, inline = True)
			emb.add_field(name = 'Имя: ', value = member.display_name, inline = True)
			emb.add_field(name = 'Айди: ', value = member.id, inline = True)
			emb.add_field(name = 'Тег: ', value = member.mention, inline = True)
			emb.set_thumbnail(url = member.avatar_url)
			await ctx.send(embed = emb)
	else:
		await ctx.author.send(embed = discord.Embed(description = f'Эту команду можно использовать только в канале - #**console**', color = 0x00ff00)) 

# Games
@client.command()
async def games(ctx):
	await ctx.message.delete()
	if ctx.channel.id == 843947523982229505:
		message = await ctx.send(embed = discord.Embed(description = f'Выберите игровую роль, нажав на реакцию под сообщением', color = 0x00ff00)) 
		await message.add_reaction('🔪')
		await message.add_reaction('🔫')
		await message.add_reaction('⚔️')
	else:
		await ctx.author.send(embed = discord.Embed(description = f'Эту команду можно использовать только в канале - #**console**', color = 0x00ff00))  

# Say-say
@client.command()
async def say(ctx, arg):
	await ctx.send(arg)  
 
#==============================================ECONOMICE==============================================

# Work
@client.command()
async def work(ctx):
	await ctx.message.delete()
	if ctx.channel.id == 843947523982229505:
		with open('data/economy.json', 'r') as f:
			data = json.load(f)
		if not str(ctx.message.author.id) in data:
			data[str(ctx.author.id)] = {}
			data[str(ctx.author.id)]['money'] = 0
			data[str(ctx.author.id)]['crystal'] = 0
			data[str(ctx.author.id)]['name'] = ctx.author.name 

		if not str(ctx.author.id) in queue:
			with open('data/settings.json', 'r') as f:
				dataSet = json.load(f)
			money_work = random.randint(dataSet['minwork'], dataSet['maxwork'])
			emb = discord.Embed(description = f'**{ctx.author.name}** Вы получили {money_work} :dollar:', color = 0x00ff00)
			await ctx.send(embed = emb)
			data[str(ctx.author.id)]['money'] += money_work
			queue.append(str(ctx.author.id))
			with open('data/economy.json', 'w') as f:
				json.dump(data, f, sort_keys = True, indent = 4)
			await asyncio.sleep(dataSet['kd_work'] * 60)
			queue.remove(str(ctx.author.id))
		if str(ctx.author.id) in queue:
			emb = discord.Embed(description = f'**{ctx.author.name}** Вы уже получили свою награду.', color = 0xff0000) 
			await ctx.send(embed = emb) 
	else:
		await ctx.author.send(embed = discord.Embed(description = f'Эту команду можно использовать только в канале - #**work**', color = 0x00ff00)) 
				
# Crime 
@client.command()
async def crime(ctx, member: discord.Member = None):
	await ctx.message.delete()
	if ctx.channel.id == 843947523982229505:
		with open('data/economy.json', 'r') as f:
			data = json.load(f)
		if (member == None) or (ctx.message.author.id == member.id): 
			await ctx.send(embed = discord.Embed(description = f':no_entry_sign: **{ctx.message.author.name}**, вы не можете ограбить самого себя!', color = 0xff0000))
		else:
			with open('data/settings.json', 'r') as f:
				dataSet = json.load(f)    
			money_crime = random.randint(dataSet['mincrime'], dataSet['maxcrime'])
			if random.randint(0, 100) > dataSet['crimeprc']:
				await ctx.send(embed = discord.Embed(description = f'**{ctx.author.name}** Вы попались на краже, у вас сняли: {str(money_crime)} :dollar:', color = 0xff0000)) 
				data[str(ctx.author.id)]['money'] -= int(money_crime) * dataSet['cf_crime']
				with open('data/economy.json', 'w') as f:
					json.dump(data, f, sort_keys = True, indent = 4)
			else: 
				await ctx.send(embed = discord.Embed(description = f'**{ctx.author.name}** Вы успешно сбежали с места преступления и украли: {str(money_crime)} :dollar: , у юзера **{member.name}**!', color = 0x00ff00)) 
				data[str(ctx.author.id)]['money'] += int(money_crime)
				data[str(member.id)]['money'] -= int(money_crime)
				with open('data/economy.json', 'w') as f:
					json.dump(data, f, sort_keys = True, indent = 4)
	else:
		await ctx.author.send(embed = discord.Embed(description = f'Эту команду можно использовать только в канале - #**console**', color = 0x00ff00)) 

# Balance
@client.command(aliases = ['bal'])
async def balance(ctx, member: discord.Member = None):
	await ctx.message.delete()
	if ctx.channel.id == 843947523982229505:
		with open('data/economy.json', 'r') as f:
			data = json.load(f) 
		if member == None: 
			emb = discord.Embed(description = f'Баланс **{ctx.author.name}**: {data[str(ctx.author.id)]["money"]} :dollar:', color = 0x00ff00)
			await ctx.send(embed = emb)
		else: 
			emb = discord.Embed(description = f'Баланс **{member.name}**: {data[str(member.id)]["money"]} :dollar:', color = 0x00ff00)
			await ctx.send(embed = emb) 
	else:
		await ctx.author.send(embed = discord.Embed(description = f'Эту команду можно использовать только в канале - #**console**', color = 0x00ff00)) 
 
# GiveMoney 
@client.command(aliases = ['gmoney', 'givem'])
async def givemoney(ctx, member: discord.Member, credite):
	await ctx.message.delete()
	if ctx.channel.id == 843947523982229505:
		with open('data/economy.json', 'r') as f:
			data = json.load(f)
		bal = data[str(ctx.author.id)]['money']
		if int(credite) < int(bal):
			await ctx.send(embed = discord.Embed(description = f':white_check_mark: **{ctx.author.name}**, вы перевели **{member.name}** {credite} :dollar:', color = 0x00ff00)) 
			data[str(ctx.author.id)]['money'] -= int(credite)
			data[str(member.id)]['money'] += int(credite)
		else:
			await ctx.send(embed = discord.Embed(description = f':no_entry_sign: Ошибка! У вас недостаточно кредитов, ваш баланс состовляет {credite} :dollar:', color = 0xff0000))
		with open('data/economy.json', 'w') as f:
			json.dump(data, f, sort_keys = True, indent = 4) 
	else:
		await ctx.author.send(embed = discord.Embed(description = f'Эту команду можно использовать только в канале - #**console**', color = 0x00ff00)) 

# AddBalance
@client.command(aliases = ['addbal', 'addb', 'ab'])
@commands.has_permissions(administrator = True)
async def addbalance(ctx, member: discord.Member, credite: int):
	await ctx.message.delete()
	if ctx.channel.id == 843947523982229505:
		with open('data/economy.json', 'r') as f:
			data = json.load(f)
		data[str(member.id)]['money'] += int(credite)
		await ctx.send(embed = discord.Embed(description = f':white_check_mark: Участнику **{member.name}**, выдано {credite} :dollar: , модератором {ctx.author.mention}', color = 0x00ff00))
		with open('data/economy.json', 'w') as f:
			json.dump(data, f, sort_keys = True, indent = 4)
	else:
		await ctx.author.send(embed = discord.Embed(description = f'Эту команду можно использовать только в канале - #**console**', color = 0x00ff00)) 

# RemoveBalance
@client.command(aliases = ['rmbal', 'rmb'])
@commands.has_permissions(administrator = True)
async def removebalance(ctx, member: discord.Member, credite: int):
	await ctx.message.delete()
	if ctx.channel.id == 843947523982229505:
		with open('data/economy.json', 'r') as f:
			data = json.load(f)
		data[str(member.id)]['money'] -= int(credite)
		await ctx.send(embed = discord.Embed(description = f':white_check_mark: У участника **{member.name}**, было снято {credite} :dollar: , модератором {ctx.author.mention}', color = 0x00ff00))
		with open('data/economy.json', 'w') as f:
			json.dump(data, f, sort_keys = True, indent = 4)
	else:
		await ctx.author.send(embed = discord.Embed(description = f'Эту команду можно использовать только в канале - #**console**', color = 0x00ff00)) 

# EnterBalance
@client.command(aliases = ['entbal', 'ebal', 'entb'])
@commands.has_permissions(administrator = True)
async def enterbalance(ctx, member: discord.Member, credite: int):
	await ctx.message.delete()
	if ctx.channel.id == 843947523982229505:
		with open('data/economy.json', 'r') as f:
			data = json.load(f)
		data[str(member.id)]['money'] = int(credite)
		await ctx.send(embed = discord.Embed(description = f':white_check_mark: Участнику **{member.name}**, было установленно {credite} :dollar: , модератором {ctx.author.mention}', color = 0x00ff00))
		with open('data/economy.json', 'w') as f:
			json.dump(data, f, sort_keys = True, indent = 4) 
	else:
		await ctx.author.send(embed = discord.Embed(description = f'Эту команду можно использовать только в канале - #**console**', color = 0x00ff00)) 

# AddShop 
@client.command(aliases = ['adds', 'ashop', 'as'])
@commands.has_permissions(administrator = True)
async def addshop(ctx, role: discord.Role, cost: int):
	if ctx.channel.id == 843947523982229505:
		with open('data/economy.json', 'r') as f:
			data = json.load(f)
		if str(role.id) in data['shop']:
			await ctx.send(embed = discord.Embed(description = f':no_entry_sign: {ctx.message.author.name}. Эта роль уже есть в магазине!', color = 0xff0000)) 
		if not str(role.id) in data['shop']:
			data['shop'][str(role.id)] = {}
			data['shop'][str(role.id)]['cost'] = cost
			await ctx.send(embed = discord.Embed(description = f':white_check_mark: {ctx.message.author.name}. Роль добавлена в магазин!', color = 0x00ff00)) 
		with open('data/economy.json', 'w') as f:
			json.dump(data, f, sort_keys = True, indent = 4)
	else:
		await ctx.author.send(embed = discord.Embed(description = f'Эту команду можно использовать только в канале - #**console**', color = 0x00ff00)) 

# RemoveShop
@client.command(aliases = ['rms', 'rmshop'])
@commands.has_permissions(administrator = True)
async def removeshop(ctx, role: discord.Role): 
	if ctx.channel.id == 843947523982229505:
		with open('data/economy.json', 'r') as f:
			data = json.load(f)
		if str(role.id) in data['shop']:
			await ctx.send(f":white_check_mark: {ctx.message.author.name}. Роль удалена из магазина!")
			del data['shop'][str(role.id)] 
		if not str(role.id) in data['shop']: 
			await ctx.send(f":no_entry_sign: {ctx.message.author.name}. Этой роли нет в магазине!") 
		with open('data/economy.json', 'w') as f:
			json.dump(data, f) 
	else:
		await ctx.author.send(embed = discord.Embed(description = f'Эту команду можно использовать только в канале - #**console**', color = 0x00ff00)) 

# Buy
@client.command()
async def buy(ctx, role: discord.Role): 
	if ctx.channel.id == 843947523982229505:
		with open('data/economy.json', 'r') as f:
			data = json.load(f)
		if str(role.id) in data['shop']:
			if data['shop'][str(role.id)]['cost'] <= data[str(ctx.author.id)]['money']:
				if not role in ctx.author.roles:
					await ctx.send(embed = discord.Embed(description = f":white_check_mark: **{ctx.message.author.name}**. Вы купили роль!", color = 0x00ff00))
					for i in data['shop']:
						if i == str(role.id):
							buy = discord.utils.get(ctx.guild.roles, id = int(i))
							await ctx.author.add_roles(buy)
							data[str(ctx.author.id)]['money'] -= data['shop'][str(role.id)]['cost']
				else:
					await ctx.send('У вас уже есть эта роль')
		with open('data/economy.json', 'w') as f:
			json.dump(data, f, sort_keys = True, indent = 4) 
	else:
		await ctx.author.send(embed = discord.Embed(description = f'Эту команду можно использовать только в канале - #**console**', color = 0x00ff00)) 

# SHOP
@client.command()
async def shop(ctx):
	await ctx.message.delete()
	if ctx.channel.id == 843947523982229505:
		with open('data/economy.json', 'r') as f:
			data = json.load(f)
		emb = discord.Embed(title = 'Магазин        :moneybag:', description = '/buy @role', color = 0xffd700)
		for role in data['shop']:
			emb.add_field(name = f'Цена: {data["shop"][role]["cost"]} :dollar:', value = f'**Роль: ** <@&{role}>', inline = False)
		await ctx.send(embed = emb)
	else:
		await ctx.author.send(embed = discord.Embed(description = f'Эту команду можно использовать только в канале - #**console**', color = 0x00ff00)) 

#==============================================SETTINGS==============================================
#
# Set min work
@client.command()
@commands.has_permissions(administrator = True)
async def minwork(ctx, arg: int):
	await ctx.message.delete()
	if ctx.channel.id == 843947523982229505:
		with open('data/settings.json', 'r') as f:
			dataSet = json.load(f)
		dataSet['minwork'] = arg 
		await ctx.send(embed = discord.Embed(description = f':white_check_mark: **{ctx.author.name}** установил **минимальную** выдоваемую сумму кредитов за **работу** на **{arg}** :dollar:', color = 0x00ff00))
		with open('data/settings.json', 'w') as f:
			json.dump(dataSet, f, sort_keys = True, indent = 4)
	else:
		await ctx.author.send(embed = discord.Embed(description = f'Эту команду можно использовать только в канале - #**console**', color = 0x00ff00)) 

# Set max work
@client.command()
@commands.has_permissions(administrator = True)
async def maxwork(ctx, arg: int):
	await ctx.message.delete()
	if ctx.channel.id == 843947523982229505:
		with open('data/settings.json', 'r') as f:
			dataSet = json.load(f)
		dataSet['maxwork'] = arg 
		await ctx.send(embed = discord.Embed(description = f':white_check_mark: **{ctx.author.name}** установил **максимальную** выдоваемую сумму кредитов за **работу** на **{arg}** :dollar:', color = 0x00ff00))
		with open('data/settings.json', 'w') as f:
			json.dump(dataSet, f, sort_keys = True, indent = 4)
	else:
		await ctx.author.send(embed = discord.Embed(description = f'Эту команду можно использовать только в канале - #**console**', color = 0x00ff00)) 

# Set min crime
@client.command()
@commands.has_permissions(administrator = True)
async def mincrime(ctx, arg: int):
	await ctx.message.delete()
	if ctx.channel.id == 843947523982229505:
		with open('data/settings.json', 'r') as f:
			dataSet = json.load(f)
		dataSet['mincrime'] = arg 
		await ctx.send(embed = discord.Embed(description = f':white_check_mark: **{ctx.author.name}** установил **минимальную** выдоваемую сумму кредитов за **кражу** на **{arg}** :dollar:', color = 0x00ff00))
		with open('data/settings.json', 'w') as f:
			json.dump(dataSet, f, sort_keys = True, indent = 4)
	else:
		await ctx.author.send(embed = discord.Embed(description = f'Эту команду можно использовать только в канале - #**console**', color = 0x00ff00)) 

# Set max crime
@client.command()
@commands.has_permissions(administrator = True)
async def maxcrime(ctx, arg: int):
	await ctx.message.delete()
	if ctx.channel.id == 843947523982229505:
		with open('data/settings.json', 'r') as f:
			dataSet = json.load(f)
		dataSet['maxcrime'] = arg 
		await ctx.send(embed = discord.Embed(description = f':white_check_mark: **{ctx.author.name}** установил **максимальную** выдоваемую сумму кредитов за **кражу** на **{arg}** :dollar:', color = 0x00ff00))
		with open('data/settings.json', 'w') as f:
			json.dump(dataSet, f, sort_keys = True, indent = 4)
	else:
		await ctx.author.send(embed = discord.Embed(description = f'Эту команду можно использовать только в канале - #**console**', color = 0x00ff00)) 

# Set prefix
@client.command()
@commands.has_permissions(administrator = True)
async def setprefix(ctx, arg: str):
	await ctx.message.delete()
	if ctx.channel.id == 843947523982229505:
		with open('data/settings.json', 'r') as f:
			dataSet = json.load(f)
		dataSet['prefix'] = arg 
		await ctx.send(embed = discord.Embed(description = f':white_check_mark: **{ctx.author.name}** установил префикс: **{arg}**', color = 0x00ff00))
		with open('data/settings.json', 'w') as f:
			json.dump(dataSet, f, sort_keys = True, indent = 4)
	else:
		await ctx.author.send(embed = discord.Embed(description = f'Эту команду можно использовать только в канале - #**console**', color = 0x00ff00)) 

# Set min coin
@client.command()
@commands.has_permissions(administrator = True)
async def mincoin(ctx, arg: int):
	await ctx.message.delete()
	if ctx.channel.id == 843947523982229505:
		with open('data/settings.json', 'r') as f:
			dataSet = json.load(f)
		dataSet['mincoin'] = arg 
		await ctx.send(embed = discord.Embed(description = f':white_check_mark: **{ctx.author.name}** установил **минимальную** ставку минигры **coin** на: **{arg}** :dollar:', color = 0x00ff00))
		with open('data/settings.json', 'w') as f:
			json.dump(dataSet, f, sort_keys = True, indent = 4)
	else:
		await ctx.author.send(embed = discord.Embed(description = f'Эту команду можно использовать только в канале - #**console**', color = 0x00ff00)) 

# Set max coin
@client.command()
@commands.has_permissions(administrator = True)
async def maxcoin(ctx, arg: int):
	await ctx.message.delete()
	if ctx.channel.id == 843947523982229505:
		with open('data/settings.json', 'r') as f:
			dataSet = json.load(f)
		dataSet['maxcoin'] = arg 
		await ctx.send(embed = discord.Embed(description = f':white_check_mark: **{ctx.author.name}** установил **максимальную** ставку минигры **coin** на: **{arg}** :dollar:', color = 0x00ff00))
		with open('data/settings.json', 'w') as f:
			json.dump(dataSet, f, sort_keys = True, indent = 4)
	else:
		await ctx.author.send(embed = discord.Embed(description = f'Эту команду можно использовать только в канале - #**console**', color = 0x00ff00)) 

# Set given exp
@client.command()
@commands.has_permissions(administrator = True)
async def setgivenexp(ctx, arg: float):
	await ctx.message.delete()
	if ctx.channel.id == 843947523982229505:
		with open('data/settings.json', 'r') as f:
			dataSet = json.load(f)
		dataSet['givenexp'] = arg 
		await ctx.send(embed = discord.Embed(description = f':white_check_mark: **{ctx.author.name}** установил выдаваемый **опыт** за сообщение на: **{arg}** exp', color = 0x00ff00))
		with open('data/settings.json', 'w') as f:
			json.dump(dataSet, f, sort_keys = True, indent = 4)
	else:
		await ctx.author.send(embed = discord.Embed(description = f'Эту команду можно использовать только в канале - #**console**', color = 0x00ff00)) 

# KD Work
@client.command()
@commands.has_permissions(administrator = True)
async def setkdwork(ctx, arg: int):
	await ctx.message.delete()
	if ctx.channel.id == 843947523982229505:
		with open('data/settings.json', 'r') as f:
			dataSet = json.load(f)
		dataSet['kd_work'] = arg 
		await ctx.send(embed = discord.Embed(description = f':white_check_mark: **{ctx.author.name}** установил **КД** между **работой** на: **{arg}** мин.', color = 0x00ff00))
		with open('data/settings.json', 'w') as f:
			json.dump(dataSet, f, sort_keys = True, indent = 4)
	else:
		await ctx.author.send(embed = discord.Embed(description = f'Эту команду можно использовать только в канале - #**console**', color = 0x00ff00)) 


# KD Work
@client.command()
@commands.has_permissions(administrator = True)
async def setkdcoin(ctx, arg: int):
	await ctx.message.delete()
	if ctx.channel.id == 843947523982229505:
		with open('data/settings.json', 'r') as f:
			dataSet = json.load(f)
		dataSet['kd_coin'] = arg 
		await ctx.send(embed = discord.Embed(description = f':white_check_mark: **{ctx.author.name}** установил **КД** между **COIN** на: **{arg}** мин.', color = 0x00ff00))
		with open('data/settings.json', 'w') as f:
			json.dump(dataSet, f, sort_keys = True, indent = 4)
	else:
		await ctx.author.send(embed = discord.Embed(description = f'Эту команду можно использовать только в канале - #**console**', color = 0x00ff00)) 

# Crime Prc
@client.command()
@commands.has_permissions(administrator = True)
async def setcrimeprc(ctx, arg: int):
	await ctx.message.delete()
	if ctx.channel.id == 843947523982229505:
		with open('data/settings.json', 'r') as f:
			dataSet = json.load(f)
		dataSet['crimeprc'] = arg 
		await ctx.send(embed = discord.Embed(description = f':white_check_mark: **{ctx.author.name}** установил процент успешной кражи на: **{arg}**%', color = 0x00ff00))
		with open('data/settings.json', 'w') as f:
			json.dump(dataSet, f, sort_keys = True, indent = 4)
	else:
		await ctx.author.send(embed = discord.Embed(description = f'Эту команду можно использовать только в канале - #**console**', color = 0x00ff00)) 

# Crime CF
@client.command()
@commands.has_permissions(administrator = True)
async def setcrimecf(ctx, arg: float):
	await ctx.message.delete()
	if ctx.channel.id == 843947523982229505:
		with open('data/settings.json', 'r') as f:
			dataSet = json.load(f)
		dataSet['cf_crime'] = arg 
		await ctx.send(embed = discord.Embed(description = f':white_check_mark: **{ctx.author.name}** установил процент наказания за кражу на: **{arg}**%', color = 0x00ff00))
		with open('data/settings.json', 'w') as f:
			json.dump(dataSet, f, sort_keys = True, indent = 4)
	else:
		await ctx.author.send(embed = discord.Embed(description = f'Эту команду можно использовать только в канале - #**console**', color = 0x00ff00)) 

#========================================CMD ERRORS======================================== 

# Clear 
@clear.error 
async def clear_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send(f':no_entry_sign: {ctx.author.mention}, обязаельно укажите аргумент!')
	if isinstance(error, commands.MissingPermissions):
		await ctx.send(f':no_entry_sign: {ctx.author.mention}, у вас недостаточно прав на команду **clear**!')
# Kick
@kick.error
async def clear_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send(f':no_entry_sign: {ctx.author.mention}, обязаельно укажите пользователя, которого хотите исключить!')
	if isinstance(error, commands.MissingPermissions):
		await ctx.send(f':no_entry_sign: {ctx.author.mention}, у вас недостаточно прав на команду **kick**!')
# Ban
@ban.error
async def clear_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send(f':no_entry_sign: {ctx.author.mention}, обязаельно укажите пользователя, которого хотите забанить!')
	if isinstance(error, commands.MissingPermissions):
		await ctx.send(f':no_entry_sign: {ctx.author.mention}, у вас недостаточно прав на команду **ban**!')
# Unban
@unban.error
async def clear_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send(f':no_entry_sign: {ctx.author.mention}, обязаельно укажите пользователя, которого хотите разбанить!')
	if isinstance(error, commands.MissingPermissions):
		await ctx.send(f':no_entry_sign: {ctx.author.mention}, у вас недостаточно прав на команду **unban**!')
# Mute
@mute.error
async def clear_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send(f':no_entry_sign: {ctx.author.mention}, обязаельно укажите пользователя, которого хотите замутить!')
	if isinstance(error, commands.MissingPermissions):
		await ctx.send(f':no_entry_sign: {ctx.author.mention}, у вас недостаточно прав на команду **mute**!')
# Unmute
@unmute.error
async def clear_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send(f':no_entry_sign: {ctx.author.mention}, обязаельно укажите пользователя, которого хотите размутить!')
	if isinstance(error, commands.MissingPermissions):
		await ctx.send(f':no_entry_sign: {ctx.author.mention}, у вас недостаточно прав на команду **unmute**!')
# Vip
@vip.error
async def clear_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send(f':no_entry_sign: {ctx.author.mention}, обязаельно укажите пользователя, которому хотите выдать VIP-роль!')
	if isinstance(error, commands.MissingPermissions):
		await ctx.send(f':no_entry_sign: {ctx.author.mention}, у вас недостаточно прав на команду **vip**!')
# DeVip
@devip.error
async def clear_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send(f':no_entry_sign: {ctx.author.mention}, обязаельно укажите пользователя, у которого хотите забрать VIP-роль!')
	if isinstance(error, commands.MissingPermissions):
		await ctx.send(f':no_entry_sign: {ctx.author.mention}, у вас недостаточно прав на команду **devip**!')
# Mod
@mod.error
async def clear_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send(f':no_entry_sign: {ctx.author.mention}, обязаельно укажите пользователя, которому хотите выдать права модератора!')
	if isinstance(error, commands.MissingPermissions):
		await ctx.send(f':no_entry_sign: {ctx.author.mention}, у вас недостаточно прав на команду **mod**!')
# DeMod
@demod.error
async def clear_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send(f':no_entry_sign: {ctx.author.mention}, обязаельно укажите пользователя, у которого хотите забрать права модератора!')
	if isinstance(error, commands.MissingPermissions):
		await ctx.send(f':no_entry_sign: {ctx.author.mention}, у вас недостаточно прав на команду **demod**!')
# Op
@op.error
async def clear_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send(f':no_entry_sign: {ctx.author.mention}, обязаельно укажите пользователя, которому хотите выдать права администратора!')
	if isinstance(error, commands.MissingPermissions):
		await ctx.send(f':no_entry_sign: {ctx.author.mention}, у вас недостаточно прав на команду **op**!')
# DeOp
@deop.error
async def clear_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send(f':no_entry_sign: {ctx.author.mention}, обязаельно укажите пользователя, у которого хотите забрать права администратора!')
	if isinstance(error, commands.MissingPermissions):
		await ctx.send(f':no_entry_sign: {ctx.author.mention}, у вас недостаточно прав на команду **deop**!')
# Say
@say.error
async def clear_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send(f':no_entry_sign: {ctx.author.mention}, обязаельно укажите сообщение, которое хотите повторить!')
# Coin
@coin.error
async def clear_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send(f':no_entry_sign: {ctx.author.mention}, обязаельно укажите **орёл** или **решка**, а так же обязательно укажите **ставку**!')
# Crime
@crime.error
async def clear_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send(f':no_entry_sign: {ctx.author.mention}, обязаельно укажите участника сервера, у которого хотите попытаться украсть!')
# GiveMoney
@givemoney.error
async def clear_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send(f':no_entry_sign: {ctx.author.mention}, обязаельно укажите участника и желаемую сумму!')
# AddBalance
@addbalance.error
async def clear_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send(f':no_entry_sign: {ctx.author.mention}, обязаельно укажите участника и желаемую сумму!')
# RemoveBalance
@removebalance.error
async def clear_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send(f':no_entry_sign: {ctx.author.mention}, обязаельно укажите участника и желаемую сумму!')
# EnterBalance
@enterbalance.error
async def clear_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send(f':no_entry_sign: {ctx.author.mention}, обязаельно укажите участника и желаемую сумму!')
# MinWork
@minwork.error
async def clear_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send(f':no_entry_sign: {ctx.author.mention}, обязаельно укажите желаемую сумму!')
# MaxWork
@maxwork.error
async def clear_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send(f':no_entry_sign: {ctx.author.mention}, обязаельно укажите желаемую сумму!')
# MinCoin
@mincoin.error
async def clear_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send(f':no_entry_sign: {ctx.author.mention}, обязаельно укажите желаемую сумму!')
# MaxCoin
@maxcoin.error
async def clear_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send(f':no_entry_sign: {ctx.author.mention}, обязаельно укажите желаемую сумму!')
# MinCrime
@mincrime.error
async def clear_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send(f':no_entry_sign: {ctx.author.mention}, обязаельно укажите желаемую сумму!')
# MaxCrime
@maxcrime.error
async def clear_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send(f':no_entry_sign: {ctx.author.mention}, обязаельно укажите желаемую сумму!')
# SetPrefix
@setprefix.error
async def clear_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send(f':no_entry_sign: {ctx.author.mention}, обязаельно укажите аргумент!')
# SetGivenExp
@setgivenexp.error
async def clear_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send(f':no_entry_sign: {ctx.author.mention}, обязаельно укажите аргумент!')
# SetKDWork
@setkdwork.error
async def clear_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send(f':no_entry_sign: {ctx.author.mention}, обязаельно укажите аргумент!') 
# SetKDCoin
@setkdcoin.error
async def clear_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send(f':no_entry_sign: {ctx.author.mention}, обязаельно укажите аргумент!')
# SetCrimePrc
@setcrimeprc.error
async def clear_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send(f':no_entry_sign: {ctx.author.mention}, обязаельно укажите аргумент!') 
# SetCrimeCF
@setcrimecf.error
async def clear_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send(f':no_entry_sign: {ctx.author.mention}, обязаельно укажите аргумент!')
# GivenRole
@givenrole.error
async def clear_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send(f':no_entry_sign: {ctx.author.mention}, обязаельно укажите **участника** и **роль**!')
 
#============================================VOICE CREATED============================================  

@client.event  
async def on_voice_state_update(member, before, after):

	if before.channel is None and after.channel is not None:
		if after.channel.id == 843957696822640640:
			for guild in client.guilds:
				maincategory = discord.utils.get(guild.categories, id = 843957479992983592)
				channel2 = await guild.create_voice_channel(name = f'Канал {member.display_name}', category = maincategory)
				await channel2.set_permissions(member, connect = True, mute_members = True, move_members = True, manage_channels = True)
				await member.move_to(channel2)
				def check(x, y, z):
					return len(channel2.members) == 0
				await client.wait_for('voice_state_update', check = check)
				await channel2.delete()  

#===================================================================================================== 

with open('data/bot-info.json', 'r') as f:
	dataBot = json.load(f)
client.run(dataBot['token']) # Running token 