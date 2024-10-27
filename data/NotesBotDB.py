import asyncio
import aiosqlite

async def createDB():
    async with aiosqlite.connect('data/NotesBotDB') as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS users (
                         user_id TEXT PRIMARY KEY NOT NULL UNIQUE,
                         username TEXT,
                         first_name TEXT,
                         last_name TEXT,
                         user_timezone TEXT
                         )''')
        await db.commit()

async def createNotesDB():
    async with aiosqlite.connect('data/NotesBotDB') as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS notes (
                         note_id INTEGER PRIMARY KEY AUTOINCREMENT,
                         user_id TEXT,
                         note_text TEXT,
                         note_description TEXT,
                         note_notification TEXT,
                         UNIQUE(user_id, note_text)                   
                         )''')
        await db.commit()


async def addUserDB(user_id, username, first_name, last_name):
    async with aiosqlite.connect('data/NotesBotDB') as db:
        cursor = await db.execute('SELECT * FROM users WHERE user_id=?', (user_id,))
        if not await cursor.fetchone():
            await db.execute('INSERT INTO users (user_id, username, first_name, last_name) VALUES (?,?,?,?)', (user_id, username, first_name, last_name))
        await db.commit()

async def addNoteDB(user_id, note_text, note_description):
    async with aiosqlite.connect('data/NotesBotDB') as db:
        await db.execute('INSERT INTO notes (user_id, note_text, note_description) VALUES (?,?,?)', (user_id, note_text, note_description))
        await db.commit()


async def selectNotesDB(user_id):
    async with aiosqlite.connect('data/NotesBotDB') as db:
        cursor = await db.execute('SELECT note_text FROM notes WHERE user_id=?', (user_id,))
        return [n[0] for n in await cursor.fetchall()]

async def selectNoteDB(user_id, note_text):
    async with aiosqlite.connect('data/NotesBotDB') as db:
        cursor = await db.execute('SELECT note_text, note_description, note_notification FROM notes WHERE user_id=? AND note_text=?', (user_id, note_text))
        return await cursor.fetchone()

async def deleteNoteDB(user_id, note_text):
    async with aiosqlite.connect('data/NotesBotDB') as db:
        await db.execute('DELETE FROM notes WHERE user_id=? AND note_text=?', (user_id, note_text))
        await db.commit()
    
async def editNoteDB(user_id, note_text, new_note_text=0, new_note_description=0, new_note_notification=0):
    async with aiosqlite.connect('data/NotesBotDB') as db:
        if new_note_text:
            await db.execute('UPDATE notes SET note_text=? WHERE user_id=? AND note_text=?', (new_note_text, user_id, note_text))
        elif new_note_description:
            await db.execute('UPDATE notes SET note_description=? WHERE user_id=? AND note_text=?', (new_note_description, user_id, note_text))
        elif new_note_notification:
            await db.execute('UPDATE notes SET note_notification=? WHERE user_id=? AND note_text=?', (new_note_notification, user_id, note_text))
        await db.commit()


async def getUserTimezone(user_id):
    async with aiosqlite.connect('data/NotesBotDB') as db:
        cursor = await db.execute('SELECT user_timezone FROM users WHERE user_id=?', (user_id,))
        result = await cursor.fetchone()
        if result:
            return result[0]
        else:
            return None
    
async def setUserTimezone(user_id, user_timezone):
    async with aiosqlite.connect('data/NotesBotDB') as db:
        await db.execute('UPDATE users SET user_timezone=? WHERE user_id=?', (user_timezone, user_id))
        await db.commit()


async def getNotification():
    async with aiosqlite.connect('data/NotesBotDB') as db:
        cursor = await db.execute('SELECT user_id, note_text, note_notification FROM notes')
        return await cursor.fetchall()
    
async def deleteNotification(user_id, note_text):
    async with aiosqlite.connect('data/NotesBotDB') as db:
        await db.execute('UPDATE notes SET note_notification=NULL WHERE user_id=? AND note_text=?', (user_id, note_text))
        await db.commit()


if __name__ == "__main__":
    asyncio.run(createDB())
    asyncio.run(createNotesDB())