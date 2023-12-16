"""
Copyright 2023 Vinny

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
print("Vinny's MultiTool is starting...\nGetting discord buildNumber")
from src import MultiTool, MPrint, Utility, scrape, global_variables, _captcha, DiscordSocket
import json
import threading
import random
import emoji
import asyncio
import os
from update import lookforupdates
from traceback import format_exc
from typing import Union
from colorama import Fore, Style
from tasksio import TaskPool
from multiprocessing.pool import ThreadPool
# VARIABLES
console = MPrint()
goodtokens = []
seen = {}
duplicates = 0
notjoined = 0
lockedtokens = 0
invalidTokens = 0

# SYNC functions
def clearConsole(): return os.system(
    'cls' if os.name in ('nt', 'dos') else 'clear')
def showMenu():
    print(f'{Style.BRIGHT}{Fore.MAGENTA}1: Check Tokens {Style.RESET_ALL}')
    print(f'{Style.BRIGHT}{Fore.MAGENTA}2: Join Server {Style.RESET_ALL}')
    print(f'{Style.BRIGHT}{Fore.MAGENTA}3: Server Spammer {Style.RESET_ALL}')
    print(f'{Style.BRIGHT}{Fore.MAGENTA}4: Server Leaver {Style.RESET_ALL}')
    print(
        f'{Style.BRIGHT}{Fore.MAGENTA}5: Format changer: [Email:Pass:Token] -> [Token] {Style.RESET_ALL}')
    print(f'{Style.BRIGHT}{Fore.MAGENTA}6: Single DM Spam {Style.RESET_ALL}')
    print(f'{Style.BRIGHT}{Fore.MAGENTA}7: Mass DM {Style.RESET_ALL}')
    print(
        f'{Style.BRIGHT}{Fore.MAGENTA}8: Username Changer [Email:Pass:Token] {Style.RESET_ALL}')
    print(
        f'{Style.BRIGHT}{Fore.MAGENTA}9: Bio Changer {Style.RESET_ALL}')
    print(
        f'{Style.BRIGHT}{Fore.MAGENTA}10: Friends Spammer {Style.RESET_ALL}')
    print(
        f'{Style.BRIGHT}{Fore.MAGENTA}11: Member scrapper {Style.RESET_ALL}')
    print(
        f'{Style.BRIGHT}{Fore.MAGENTA}12: VC spammer {Style.RESET_ALL}')
    print(
        f'{Style.BRIGHT}{Fore.MAGENTA}13: Exit {Style.RESET_ALL}')
def changeFormat(token: str):
    if ":" not in token or len(token.split(":")) == 2:
        token = token if ":" not in token else token.split(":")[1]
        console.f_print(
            f"{token} format is not [Email:Pass:Token]")
        return token
    newToken = token.split(":")[2]
    console.s_print(f"{token} -> {newToken}")
    return newToken
def setTitle(tokens: list): return os.system(
    f'title Vinnys MultiTool - Tokens: {len(tokens)} - Proxies: {len(open("input/proxies.txt").read().splitlines())} - By Vinny' if os.name == "nt" else f'echo -n -e "\033]0;Discord MultiTool | Tokens {len(tokens)} | Proxies {len(open("input/proxies.txt").read().splitlines())} | Captcha Balance: $ {_captcha.Captcha().getBalance()} - By Vinny\007"'
)

#ASYNC FUNCTIONS
async def scrapeMassMention(token, guildId, channelId):
    o = await buildMultiTool(token)
    res = await o.getGuild(guildId)
    if "name" not in res:
        return await scrapeMassMention(random.choice(open("input/tokens.txt").read().splitlines()), guildId, channelId)
    open("scraped/massmention.txt", "w").write("")
    console.s_print(f"Scraping in {guildId} with {token}")
    members = scrape(token, guildId, channelId)
    for member in members:
        console.s_print(f"Scraped {member}")
        open("scraped/massmention.txt", "a").write(member + "\n")
    console.s_print(f"Total Scrapped: {len(members)}")
    return True
def vcSpammer(token: str, guild: str, channelId: str):
    while True:
        sock = DiscordSocket(token)
        sock.run(channelId, guild)
        console.s_print(f"Joined vc: {token}")
async def usernameChanger(token: str, username: str):
    if ":" not in token:
        console.f_print(f"{token} is not [Email:Pass:Token]")
        return None
    spllited = token.split(":")
    password = spllited[1]
    token = spllited[2]
    m = await buildMultiTool(token)
    await m.usernameChange(username, password)

async def bioChanger(token: str, bio: str):
    m = await buildMultiTool(token)
    await m.bioChange(bio)

async def scrapeMembers(token, guildId, channelId):
    o = await buildMultiTool(token)
    res = await o.getGuild(guildId)
    if "name" not in res:
        return await scrapeMembers(random.choice(open("input/tokens.txt").read().splitlines()), guildId, channelId)
    open("scraped/massmention.txt", "w").write("")
    console.s_print(f"Scraping in {guildId} with {token}")
    members = scrape(token, guildId, channelId)
    for member in members:
        console.s_print(f"Scraped {member}")
        open("scraped/members.txt", "a").write(member + "\n")
    console.s_print(f"Total Scrapped: {len(members)}")
    return True

async def leave(token: str, guildId: str):
    o = await buildMultiTool(token)
    await o.leave(guildId)

async def buildMultiTool(token: str) -> MultiTool:
    try:
        m = MultiTool()
        await m._init(token)
        return m
    except Exception as e:
        console.f_print(f"Error while building Multitool Coroutine: {e}")
        return await buildMultiTool(token)

async def sendMessage(token: str, channelId: str, message: str, massMention: bool, massMentionSize: int):
    m = await buildMultiTool(token)
    if m == None:
        return None
    while True:
        await m.sendMessageInChannel(
            message, channelId, massMention, massMentionSize)
async def friendRequest(token: str, username: str, discrim: str):
    m = await buildMultiTool(token)
    await m.sendFriendRequest(username, discrim)

async def spamMessages(token: str, userId: str, message: str):
    m = await buildMultiTool(token)
    if not m:
        return None
    while True:
        _, _res = await m.sendDirectMessage(userId, message)
        if _:
            console.s_print(f"{token} successfully sent dm to {userId}")
        else:
            console.f_print(f"{token} failed to send dm to {userId}")

async def sendDm(token: str, userId: str, message: str):
    m = await buildMultiTool(token)
    _, _res = await m.sendDirectMessage(userId, message)
    if 'You are opening direct messages too fast' in _res.text:
        global_variables.qurantined_tokens.append(token)
        console.f_print(f"{token} got ratelimited. sleeping for 10 minutes.")
        threading.Thread(
            target=global_variables.removeFromQurantine, args=(token, ))
    elif 'Cannot send messages to this user' in _res.text:
        global_variables.blaclisted_users.append(userId)
    elif 'You need to verify your account in order to perform this action' in _res.text or '401: Unauthorized' in _res.text:
        global_variables.locked_tokens.append(token)
        global_variables.qurantined_tokens.append(token)
        console.f_print(f"{token} token got locked during mass dm")
    elif _:
        console.s_print(f"{token} successfully sent dm to {userId}")


async def checkToken(token: str):
    global lockedtokens
    global invalidTokens
    m = await buildMultiTool(token)
    if m == None:
        return None
    res, typee = await m.checkToken()
    if typee == "LOCKED":
        lockedtokens += 1
        return False
    if typee == "INVALID":
        invalidTokens += 1
    if res:
        goodtokens.append(token)
        return True


async def join(token: str, rawInvite: str, ctx: str, guildId: str, channelId: Union[str, None] = None, messageId: Union[str, None] = None):
    global notjoined
    m = await buildMultiTool(token)
    if m == None:
        return None
    res, req = await m.join(rawInvite, ctx)
    if not res:
        notjoined += 1
        return res
    if Utility().config["joiner"]["bypassMembershipScreening"] and "show_verification_form" in req.json():
        await m.bypassScreening(guildId, rawInvite)
    if Utility().config["joiner"]["bypassReactionVerification"] and channelId != None:
        emojiObj = await m.getReactions(messageId, channelId)
        if emojiObj["id"] == None:
            emojiOut = emoji.demojize(
                emojiObj["name"]
            )
        else:
            emojiOut = emojiObj["name"] + "%3A" + emojiObj["id"]
        if emojiOut[0] == ":" and emojiOut[len(emojiOut) - 1] == ":":
            emojiOut = emoji.emojize(emojiOut)
        await m.addReaction(messageId, channelId, emojiOut)
    return res
async def menu():
    global duplicates
    global notjoined
    global lockedtokens
    global invalidTokens
    try:
        tokens = open("input/tokens.txt").read().splitlines()
        setTitle(tokens)
        print("")
        showMenu()
        print("\n")
        choice = int(input(
            f"[>] {Fore.WHITE}{Style.BRIGHT}Enter your choice \n>> {Style.RESET_ALL}"))
        if choice == 1:
            console.s_print(f"Checking tokens...")
            async with TaskPool(10_000) as pool:
                for token in tokens:
                    if token in seen:
                        duplicates += 1
                        continue
                    seen[token] = True
                    await pool.put(checkToken(token))
            console.s_print(
                f"All tokens checked.\nDuplicates: {duplicates} | Valid: {len(goodtokens)} | Invalid: {invalidTokens} | Locked Tokens: {lockedtokens} | Total Bad Tokens(includes locked+invalid tokens): {invalidTokens + lockedtokens}")
            seen.clear()
            duplicates = 0
            lockedtokens = 0
            invalidTokens = 0
            if Utility().config["removeDeadTokens"]:
                open("input/tokens.txt", "w").write("")
                for goodtoken in goodtokens:
                    open("input/tokens.txt", "a").write(f"{goodtoken}\n")
            goodtokens.clear()
            return await menu()
        if choice == 2:
            console.s_print(f"Server Joiner...")
            rawInvite = input(f"[>] {Fore.GREEN}{Style.BRIGHT}Enter your invite: {Style.RESET_ALL}").split(
                "discord.gg/")[1]
            try:
              req1 = Utility().getInviteInfo(rawInvite)
              if req1 == {"message": "Unknown Invite", "code": 10006}:
                console.f_print(f"https://discord.gg/{rawInvite} is INVALID")
                return await menu()
            except:
                console.f_print("Failed to get invite info, You are probably ratelimited, try using a VPN")
                req1 = {"guild": { "id": None }, "channel": { "id": None }}
                if Utility().config.get("proxy")["proxyless"]: # if proxyless is true, redirect back to `menu` otherwise keep joining
                    return await menu()
            console.s_print(f"https://discord.gg/{rawInvite} is VALID")
            ctx = Utility().getContextProperties(
                req1["channel"]["id"], req1["guild"]["id"])
            deley = Utility().config["joiner"]["delay"]
            useDelay = Utility().config["joiner"]["useDelays"]
            channelId = None
            messageId = None
            if Utility().config["joiner"]["bypassReactionVerification"]:
                channelId = input(
                    f"{Fore.GREEN}{Style.BRIGHT}Reaction Verifier: Enter the channelId the message is on: {Style.RESET_ALL}")
                messageId = input(
                    f"{Fore.GREEN}{Style.BRIGHT}Reaction Verifier: Enter the messageId of the message the reaction is on: {Style.RESET_ALL}")
            async with TaskPool(10_000) as pool:
                for token in tokens:
                    if token in seen:
                        duplicates += 1
                        continue
                    seen[token] = True
                    await pool.put(join(token, rawInvite, ctx, req1["guild"]["id"], channelId, messageId))
                    if useDelay:
                        await asyncio.sleep(deley)
            console.s_print(
                f"Tokens successfully joined https://discord.gg/{rawInvite} \nDuplicate Tokens: {duplicates} | Joined Tokens: {len(tokens) - notjoined} | Not Joined: {notjoined}")
            seen.clear()
            duplicates = 0
            return await menu()
        if choice == 3:
            console.s_print(f"Server spammer...")
            massMention = True if input(
                f"{Fore.GREEN}{Style.BRIGHT}Do you want to use massmention? (y/n){Style.RESET_ALL}").lower() == "y" else None
            massMentionSize = None if massMention != True else int(input(
                f"{Fore.GREEN}{Style.BRIGHT}Enter the ammount of people you want to mention in one message: {Style.RESET_ALL}"))
            message = input(
                f"{Fore.GREEN}{Style.BRIGHT}Please type the message: {Style.RESET_ALL}")
            channelId = input(
                f"{Fore.GREEN}{Style.BRIGHT}Enter the channel Id you want to spam: {Style.RESET_ALL}")
            m = await buildMultiTool(random.choice(tokens))
            guildId = await m.getChannel(channelId)

            if massMention and input(f"{Fore.GREEN}{Style.BRIGHT}Do you want to use already scrapped members for massmention? (y/n) {Style.RESET_ALL}").lower() != "y":
                await scrapeMassMention(random.choice(tokens), guildId, channelId)
            async with TaskPool(10_000) as pool:
                for token in tokens:
                    await pool.put(sendMessage(token, channelId, message, massMention, massMentionSize))
        if choice == 4:
            console.s_print(f"Server leaver...")
            guildId = input(
                f"{Fore.GREEN}{Style.BRIGHT}Enter the server Id you want to leave: {Style.RESET_ALL}")
            async with TaskPool(10_000) as pool:
                for token in tokens:
                    await pool.put(leave(token, guildId))
            return await menu()
        if choice == 5:
            console.s_print(f"Format changer...")
            open("input/tokens.txt", "w").write("")
            for token in tokens:
                token = changeFormat(token)
                open("input/tokens.txt", "a").write(token + "\n")
            return await menu()
        if choice == 6:
            console.s_print(f"Single DM Spammer...")
            message = input(
                f"{Fore.GREEN}{Style.BRIGHT}Enter your message: {Style.RESET_ALL}")
            userId = input(
                f"{Fore.GREEN}{Style.BRIGHT}Enter the victim's userId: {Style.RESET_ALL}")
            async with TaskPool(10_000) as pool:
                for token in tokens:
                    await pool.put(spamMessages(token, userId, message))
            return await menu()
        if choice == 7:
            console.f_print(
                f"Hey Multitool user. We are sorry but mass dm is currently disabled")
            return await menu()
            console.s_print(f"Mass DM...")
            members = open("scraped/members.txt").read().splitlines()
            if len(members) == 0:
                channelId = input(
                    f"{Fore.GREEN}{Style.BRIGHT}Enter the channel Id you want to spam: {Style.RESET_ALL}")
                m = await buildMultiTool(random.choice(tokens))
                guildId = await m.getChannel(channelId)
                await scrapeMembers(random.choice(tokens), guildId, channelId)
                members = open("scraped/members.txt").read().splitlines()
            msg: str = json.loads(open("messages.json").read())["content"]
            async with TaskPool(10_000) as pool:
                for member in members:
                    variableReplaced = msg.replace("<@user>", f"<@{member}>")
                    await pool.put(sendDm(global_variables.getGoodToken(), member, variableReplaced))
            return await menu()
        if choice == 8:
            console.s_print(f"Username changer...")
            usernames = open("input/usernames.txt").read().splitlines()
            if len(usernames) == 0:
                console.f_print(
                    f"Please input some usernames before using this feature")
                input("Press enter to return to menu")
                return await menu()
            async with TaskPool(10_000) as pool:
                for token in tokens:
                    await pool.put(usernameChanger(token, random.choice(usernames)))
            return await menu()
        if choice == 9:
            console.s_print(f"Bio changer...")
            bios = open("input/bios.txt").read().splitlines()
            if len(usernames) == 0:
                console.f_print(
                    f"Please input some bios before using this feature")
                input("Press enter to return to menu")
                return await menu()
            async with TaskPool(10_000) as pool:
                for token in tokens:
                    await pool.put(bioChanger(token, random.choice(bios)))
            return await menu()
        if choice == 10:
            console.s_print(f"Friend spammer...")
            spllited = input(
                f"{Fore.GREEN}{Style.BRIGHT}Enter your username and tag: {Style.RESET_ALL}").split("#")
            username = spllited[0]
            discrim = spllited[1]
            async with TaskPool(10_000) as pool:
                for token in tokens:
                    await pool.put(friendRequest(token, username, discrim))
        if choice == 11:
            console.s_print("Member scrapper...")
            channelId = input(
                f"{Fore.GREEN}{Style.BRIGHT}Enter your channelId you want to scrape: {Style.RESET_ALL}")
            m = await buildMultiTool(random.choice(tokens))
            guildId = await m.getChannel(channelId)
            await scrapeMembers(random.choice(tokens), guildId, channelId)
            return await menu()
        if choice == 12:
            console.s_print("VC Spammer...")
            channelId = input(f"{Fore.GREEN}{Style.BRIGHT}Enter your Voice channelId you want to spam: {Style.RESET_ALL}")
            m = await buildMultiTool(random.choice(tokens)) # build the multitool coroutine
            guildId = await m.getChannel(channelId=channelId)
            pool = ThreadPool(10_000)
            for token in tokens:
                if token in seen:
                    continue
                seen[token] = True
                pool.apply_async(vcSpammer, (token, guildId, channelId, ))
            pool.join()
            return await menu()
        if choice == 13:
            exit()
        else:
            console.f_print("Invalid Choice")
            return await menu()
        
    except Exception as e:
        console.f_print(e)
        if Utility().config["traceback"]:
            print(format_exc())
        return await menu()
if __name__ == "__main__": 
    clearConsole()
    print(Fore.MAGENTA + Style.BRIGHT + """


██╗   ██╗██╗███╗   ██╗███╗   ██╗██╗   ██╗
██║   ██║██║████╗  ██║████╗  ██║╚██╗ ██╔╝
██║   ██║██║██╔██╗ ██║██╔██╗ ██║ ╚████╔╝ 
╚██╗ ██╔╝██║██║╚██╗██║██║╚██╗██║  ╚██╔╝  
 ╚████╔╝ ██║██║ ╚████║██║ ╚████║   ██║   
  ╚═══╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═══╝   ╚═╝   
                                         
                                                                                                                        P Y T H O N
""" + Style.RESET_ALL)
    print(f'{Style.BRIGHT}By Vinny\n\n')
    if len(open("input/tokens.txt").read().splitlines()) == 0:
        console.f_print("Input some tokens before restarting...")
        input("Press Enter To Exit\n")
        exit()
    console.w_print("Mass DM is disabled")
    console.w_print(
        "Before using any feature, please check your tokens, To avoid errors.")
    if Utility().config["proxy"]["proxyless"]:
        console.w_print(
            "Proxyless is on. Switch to proxies for best performance")
    asyncio.run(menu())
