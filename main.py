from telethon import TelegramClient, events
import api_func
import re

# TELEGRAM API ID
API_ID = 0
# TELEGRAM API HASH
API_HASH = ''
#PHONE used for the account
phone = '+447--------'

#The Channel for dex screener
channel_id = -1001699399340  # replace with your actual channel id

#initalizing the telegram client
client = TelegramClient('session_name', API_ID, API_HASH)


# to find the token address for telegram message
def extract_token_address(message):
    match = re.search(r'Token address.*`(.*)`', message)
    if match:
        return match.group(1)  # group(1) refers to the first captured group - the token address
    return None


async def main():

    me = await client.get_me()
    #use the print below if you want to see different details about your telegram client
    #print(me.stringify())

    # You can print all the dialogs/conversations
    #async for dialog in client.iter_dialogs():
        #print(dialog.name, 'has ID', dialog.id)

    # If you want to send a message
    # await client.send_message('username', 'Hello! Talking to you from Telethon')

    # @client.on(events.NewMessage(chats=channel_id))
    # async def my_event_handler(event):
    #     ('New message:', event.message.text)
    #
    #     with open('add.txt', 'a', encoding='utf-8') as file:  # change 'w' to 'a'
    #         file.write(event.message.text + '\n')  # add a newline character for better readability
    #
    #         extract_and_save_token_address()

    #this is used to listen to the telegram messages and record any that are sent
    @client.on(events.NewMessage(chats=channel_id))
    async def my_event_handler(event):
        message_text = event.message.text
        print('New message:', message_text)

        #finds the address
        address = extract_token_address(event.message.text)
        #address = '0x263f7a91b2529B63c538aEFff69026c9Eac5b15B'
        if address:
            print(address)
            try:
                #checks if the api is real or just a rug pull
                score = api_func.get_token_sniffer_score(f'{address}')

                # if it gets passed the first check use go_secuity function to check if there are any more issues
                if score is not None and score >= 70:
                    go_security = api_func.send_to_go_plus(f'{address}')
                    # Replace 'CHAT_ID' with the actual ID of the chat

                    #where would you like to send the results to ?
                    await client.send_message('+44 70000000',
                                              f'{address}\nThe Token Sniffer score is {score}\n{go_security}\n'
                                              f'https://dexscreener.com/ethereum/{address}\n'
                                              f'')
                else:
                    print("Score wasn't high enough")
            except Exception as e:
                print(f"An error occurred when processing the address: {e}")
        else:
            try:
                print('Problem with address')
            except Exception as e:
                print(f"An error occurred when processing the address: {e}")


with client:
    client.loop.run_until_complete(main())
    client.run_until_disconnected()