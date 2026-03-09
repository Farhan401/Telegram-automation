import asyncio
import os

from telethon import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.errors import FloodWaitError

from config import API_ID, API_HASH, JOIN_DELAY


ACCOUNTS_FOLDER = "accounts"


def load_accounts():
    sessions = []

    for file in os.listdir(ACCOUNTS_FOLDER):

        if file.endswith(".session"):
            name = file.replace(".session", "")
            sessions.append(f"{ACCOUNTS_FOLDER}/{name}")

    return sessions


def load_links():

    with open("data/links.txt") as f:
        return [i.strip() for i in f.readlines() if i.strip()]


async def process_account(session, links):

    client = TelegramClient(session, API_ID, API_HASH)

    await client.start()

    print(f"Running: {session}")

    for link in links:

        try:

            username = link.split("/")[-1]

            if "bot" in username.lower():

                await client.send_message(username, "/start")
                print(f"{session} started bot {username}")

            else:

                await client(JoinChannelRequest(username))
                print(f"{session} joined {username}")

            await asyncio.sleep(JOIN_DELAY)

        except FloodWaitError as e:

            print(f"Flood wait {e.seconds}")
            await asyncio.sleep(e.seconds)

        except Exception as e:

            print("Error:", e)

    await client.disconnect()


async def main():

    sessions = load_accounts()
    links = load_links()

    tasks = []

    for session in sessions:
        tasks.append(process_account(session, links))

    await asyncio.gather(*tasks)


asyncio.run(main())
