# Multitool auto updater
# This file will look for updates and if there is any it will automatically install it.
# Please avoid changing anything in this file.
from colorama import Fore, Style
import httpx
from src import getVersion
APP_VERSION = getVersion()
APP_NAME = "Vinny's Multitool (discord)"

BASE_URL = "http://localhost:3001"


def lookforupdates():
    req = httpx.post(f"{BASE_URL}/api/v2/update", json={
        "v": APP_VERSION
    }, timeout=30).json()
    if req["current"] == True:
        print(f"{Fore.GREEN}{Style.BRIGHT}You are up to date!{Style.RESET_ALL}")
        if "message" in req:
            print(
                f"{Fore.YELLOW}{Style.BRIGHT}The api returned a message as well while looking for updates: \n{Style.RESET_ALL}{Style.BRIGHT}{Fore.GREEN}{req['message']}{Style.RESET_ALL}\n")
    else:
        try:

        except:
            print(
                f"{Fore.RED}Failed to install update, please install it manually.{Style.RESET_ALL}")
