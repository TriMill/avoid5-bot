#!/usr/bin/python3

import discord

fifthglyphs = set([c for c in 
"EeÆÈÉÊËæèéêëĒēĔĕĖėĘęĚěŒœƎƏƐǝȄȅȆȇȨȩɆɇɘəɛɜɝɞΕεϵ϶ЄЕЭеэєᴇᴈᴱᴲᵉᵋᵌᶒᶓᶔᶟḔḕḖḗḘḙḚḛḜḝẸẹẺẻẼẽẾếỀềỂểỄễỆệ€ℭ℮ℯℰⅇ∃∈∉∊∋∌∍⋲⋳⋴⋵⋶⋷⋸⋹⋺⋻⋼⋽⋾⋿⍷⒠ⒺⱸⱻⲈⲉꞫꬲ𐌄𐌴𐤄𝐄𝐞𝐸𝑒𝑬𝒆𝓔𝓮𝔈𝔢𝔼𝕖𝕰𝖊𝖤𝖾𝗘𝗲𝘌𝘦𝙀𝙚𝙴𝚎𝚬𝛆𝛦𝜀𝜠𝜺𝝚𝝴𝞔𝞮🇪"
])

class MyClient(discord.Client):
    def __init__(self, whitelist):
        self.allowed = whitelist
        super().__init__()

    async def on_ready(self):
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='avoid5!aid'))
        print("Running.")

    async def do_command(self, message):
        if message.content == "avoid5!aid":
            await message.channel.send("Avoid5 stops you from using any fifthglyphs (that glyph amid 'D' and 'F'). If a fifthglyph is found in a transmission, this bot will cut it. Administrators can run `avoid5!allow [#division]` to allow this bot to act on a division (that thing starting with a `#` mark), or `avoid5!disallow [#division]` to disallow it.")
        elif message.content.startswith("avoid5!allow"):
            if message.author.guild_permissions.administrator:
                channels = message.channel_mentions
                if len(channels) >= 1:
                    for ch in channels:
                        self.allowed.add(ch.id)
                    await message.channel.send("Bot now watching said division(s).")
                    return True
                else:
                    await message.channel.send("You must follow that writing with a division (that thing starting with a `#` mark).")
            else:
                await message.channel.send("Only administrators can run this command.")
        elif message.content.startswith("avoid5!disallow"):
            if message.author.guild_permissions.administrator:
                channels = message.channel_mentions
                if len(channels) >= 1:
                    for ch in channels:
                        self.allowed.remove(ch.id)
                    await message.channel.send("Bot now ignoring said division(s).")
                    return True
                else:
                    await message.channel.send("You must follow that writing with a division (that thing starting with a `#` mark).")
            else:
                await message.channel.send("Only administrators can run this command.")
        return False

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith("avoid5!"):
            if await self.do_command(message):
                with open("whitelist", "w") as whitelistfile:
                    whitelistfile.write("\n".join([str(x) for x in self.allowed]) + "\n")
                
        if message.channel.id in self.allowed:
            
            for c in message.content:
                if c in fifthglyphs:
                    await message.delete()
                    break


with open("whitelist") as whitelistfile:
    whitelist = set([int(x) for x in whitelistfile.read().split("\n") if len(x) > 0])

with open("token") as tokenfile:
    token = tokenfile.read()

client = MyClient(whitelist)
client.run(token)
