from datetime import timedelta
from asyncio import sleep 
import pytz
import datetime, time
from info import ADMINS, USERNAME, LOG_CHANNEL
from Script import script 
from utils import get_seconds, get_status, temp
from database.users_chats_db import db 
from pyrogram import Client, filters 
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong

@Client.on_message(filters.command("remove_premium") & filters.user(ADMINS))
async def remove_premium(client, message):
    if len(message.command) == 2:
        user_id = int(message.command[1])
        user = await client.get_users(user_id)
        if await db.remove_premium_access(user_id):
            await message.reply_text("<b>sᴜᴄᴄᴇssꜰᴜʟʟʏ ʀᴇᴍᴏᴠᴇᴅ ✅</b>")
            await client.send_message(
                chat_id=user_id,
                text=f"<b>ʜᴇʏ {user.mention},\n\n⚠️ ʏᴏᴜʀ ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇss ʜᴀs ʙᴇᴇɴ ʀᴇᴍᴏᴠᴇᴅ 🚫</b>"
            )
        else:
            await message.reply_text("<b>👀 ᴜɴᴀʙʟᴇ ᴛᴏ ʀᴇᴍᴏᴠᴇ, ᴀʀᴇ ʏᴏᴜ sᴜʀᴇ ɪᴛ ᴡᴀs ᴀ ᴘʀᴇᴍɪᴜᴍ ᴜsᴇʀ ɪᴅ??</b>")
    else:
        await message.reply_text("Usage: <code>/remove_premium user_id</code>")

@Client.on_message(filters.command("myplan"))
async def myplan(client, message):
    status = get_status()
    user = message.from_user.mention
    user_id = message.from_user.id
    data = await db.get_user(message.from_user.id)
    if data and data.get("expiry_time"):
        #expiry_time = datetime.datetime.now() + datetime.timedelta(seconds=data)
        expiry = data.get("expiry_time") 
        expiry_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata"))
        expiry_str_in_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%d-%m-%Y  ⏰: %I:%M:%S %p")            
        # Calculate time difference
        current_time = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
        time_left = expiry_ist - current_time
            
        # Calculate days, hours, and minutes
        days = time_left.days
        hours, remainder = divmod(time_left.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
            
        # Format time left as a string
        time_left_str = f"{days} days, {hours} hours, {minutes} minutes"
        await message.reply_text(f"<b>ʏᴏᴜʀ ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇss ɪɴꜰᴏ -\n\nᴜsᴇʀ - {user}\n\nɪᴅ - <code>{user_id}</code>\n\nᴛɪᴍᴇ ʟᴇꜰᴛ - {time_left_str}\n\nᴇxᴘ ᴛɪᴍᴇ - {expiry_str_in_ist}.")   
    else:
        await message.reply_text(f"<b>ʜᴇʏ {user} {status},\n\nʏᴏᴜ ᴅᴏ ɴᴏᴛ ʜᴀᴠᴇ ᴀɴʏ ᴀᴄᴛɪᴠᴇ ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴs, ɪꜰ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴛᴀᴋᴇ ᴘʀᴇᴍɪᴜᴍ ᴛʜᴇɴ ᴄʟɪᴄᴋ ᴏɴ /plan ᴛᴏ ᴋɴᴏᴡ ᴀʙᴏᴜᴛ ᴛʜᴇ ᴘʟᴀɴs...</b>")
	    
@Client.on_message(filters.command("add_premium") & filters.user(ADMINS))
async def give_premium_cmd_handler(client, message):
    if len(message.command) == 4:
        time_zone = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
        current_time = time_zone.strftime("%d-%m-%Y  ⏰: %I:%M:%S %p") 
        user_id = int(message.command[1])  # Convert the user_id to integer
        user = await client.get_users(user_id)
        time = message.command[2]+" "+message.command[3]
        seconds = await get_seconds(time)
        if seconds > 0:
            expiry_time = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
            user_data = {"id": user_id, "expiry_time": expiry_time}  # Using "id" instead of "user_id"  
            await db.update_user(user_data)  # Use the update_user method to update or insert user data
            data = await db.get_user(user_id)
            expiry = data.get("expiry_time")   
            expiry_str_in_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%d-%m-%Y  :  %I:%M:%S %p")         
            await message.reply_text(f"Premium access added to the user\n\n👤 User: {user.mention}\n\n🪙 user id: <code>{user_id}</code>\n\n⏰ premium access: {time}\n\n🎩 Joining : {current_time}\n\n⌛️ Expiry: {expiry_str_in_ist}.", disable_web_page_preview=True)
            await client.send_message(
                chat_id=user_id,
                text=f"<b>ʜɪɪ {user.mention},\n\nᴘʀᴇᴍɪᴜᴍ ᴀᴅᴅᴇᴅ ᴛᴏ ʏᴏᴜʀ ᴀᴄᴄᴏᴜɴᴛ ᴇɴᴊᴏʏ 💥\n\nᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇss - {time}\n\nᴊᴏɪɴɪɴɢ - {current_time}\n\nᴇxᴘɪʀᴇ ɪɴ - {expiry_str_in_ist}</b>", disable_web_page_preview=True              
            )    
            await client.send_message(LOG_CHANNEL, text=f"#Added_Premium\n\n👤 User - {user.mention}\n\n🪙 Id - <code>{user_id}</code>\n\n⏰ Premium access - {time}\n\n🎩 Joining - {current_time}\n\n⌛️ Expiry - {expiry_str_in_ist}", disable_web_page_preview=True)                
        else:
            await message.reply_text("Invalid time format. Please use '1 day for days', '1 hour for hours', or '1 min for minutes', or '1 month for months' or '1 year for year'")
    else:
        await message.reply_text("Usage: /add_premium user_id time (e.g., '1 day for days', '1 hour for hours', or '1 min for minutes', or '1 month for months' or '1 year for year')")

@Client.on_message(filters.command("premium_user") & filters.user(ADMINS))
async def premium_user(client, message):
    aa = await message.reply_text("Fetching ...")
    new = f"Paid Users - \n\n"
    
    # Counter to keep track of the premium users
    user_counter = 1

    users = await db.get_all_users()
    async for user in users:
        data = await db.get_user(user['id'])
        if data and data.get("expiry_time"):
            expiry = data.get("expiry_time") 
            expiry_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata"))
            expiry_str_in_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%d-%m-%Y %I:%M:%S %p")            
            current_time = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
            time_left = expiry_ist - current_time
            days = time_left.days
            hours, remainder = divmod(time_left.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            time_left_str = f"{days} days, {hours} hours, {minutes} minutes"	 
            new += f"{user_counter}. User ID: {user['id']}\nName: {(await client.get_users(user['id'])).mention}\nExpiry Date: {expiry_str_in_ist}\nExpiry Time: {time_left_str}\n\n"
            user_counter += 1
        else:
            pass
    try:    
        await aa.edit_text(new)
    except MessageTooLong:
        with open('usersplan.txt', 'w+') as outfile:
            outfile.write(new)
        await message.reply_document('usersplan.txt', caption="Paid Users:")

@Client.on_message(filters.command('plan') & filters.incoming)
async def plan(client, message):
    user_id = message.from_user.id
    if message.from_user.username:
        user_info = f"@{message.from_user.username}"
    else:
        user_info = f"{message.from_user.mention}"
    log_message = f"<b><u>🎃 ᴛʜɪs ᴜsᴇʀs ᴛʀʏ ᴛᴏ ᴄʜᴇᴄᴋ /plan ᴄᴏᴍᴍᴀɴᴅ</u>\n\n- ɪᴅ - `{user_id}`\n- ɴᴀᴍᴇ - {user_info}\n\n{temp.B_LINK}</b>"
    await client.send_message(LOG_CHANNEL, log_message)  
    users = message.from_user.mention 
    btn = [[
        InlineKeyboardButton("📸 sᴇɴᴅ sᴄʀᴇᴇɴsʜᴏᴛ 📸", url=USERNAME),
    ],[
        InlineKeyboardButton("🗑 ᴄʟᴏsᴇ 🗑", callback_data="close_data")
    ]]
    await message.reply_text(text=script.PREMIUM_TEXT.format(message.from_user.mention), reply_markup=InlineKeyboardMarkup(btn))

@Client.on_message(filters.command("check_plan") & filters.user(ADMINS))
async def check_plan(client, message):
    if len(message.text.split()) == 1:
        await message.reply_text("use this command with user id... like\n\n /check_plan user_id")
        return
    user_id = int(message.text.split(' ')[1])
    user_data = await db.get_user(user_id)

    if user_data and user_data.get("expiry_time"):
        expiry = user_data.get("expiry_time")
        expiry_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata"))
        expiry_str_in_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%d-%m-%Y %I:%M:%S %p")
        current_time = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
        time_left = expiry_ist - current_time
        days = time_left.days
        hours, remainder = divmod(time_left.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        time_left_str = f"{days} days, {hours} hours, {minutes} minutes"
        response = (
            f"User ID: {user_id}\n"
            f"Name: {(await client.get_users(user_id)).mention}\n"
            f"Expiry Date: {expiry_str_in_ist}\n"
            f"Expiry Time: {time_left_str}"
        )
    else:
        response = "User have not a premium..."
    await message.reply_text(response)
