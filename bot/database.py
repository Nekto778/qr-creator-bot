import aiosqlite
from .config import DB_PATH


class Database:
    def __init__(self):
        self.db = None

    async def init(self):
        self.db = await aiosqlite.connect(DB_PATH)
        await self.db.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_blocked INTEGER DEFAULT 0
            );
            CREATE TABLE IF NOT EXISTS qr_codes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                qr_type TEXT,
                data TEXT,
                format TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS channels (
                channel_id INTEGER PRIMARY KEY,
                channel_title TEXT,
                invite_link TEXT,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS broadcasts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                admin_id INTEGER,
                text TEXT,
                sent_count INTEGER DEFAULT 0,
                failed_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        await self.db.commit()
        try:
            await self.db.execute("ALTER TABLE users ADD COLUMN language TEXT DEFAULT 'en'")
            await self.db.commit()
        except Exception:
            pass

    async def add_user(self, user_id, username, first_name, language="en"):
        await self.db.execute(
            "INSERT OR IGNORE INTO users (user_id, username, first_name, language) VALUES (?, ?, ?, ?)",
            (user_id, username, first_name, language),
        )
        await self.db.commit()

    async def get_user_lang(self, user_id) -> str:
        try:
            async with self.db.execute(
                "SELECT language FROM users WHERE user_id = ?", (user_id,)
            ) as cursor:
                row = await cursor.fetchone()
                return row[0] if row and row[0] else "en"
        except Exception:
            return "en"

    async def set_user_lang(self, user_id, language):
        await self.db.execute(
            "UPDATE users SET language = ? WHERE user_id = ?",
            (language, user_id),
        )
        await self.db.commit()

    async def user_exists(self, user_id) -> bool:
        async with self.db.execute(
            "SELECT 1 FROM users WHERE user_id = ?", (user_id,)
        ) as cursor:
            return await cursor.fetchone() is not None

    async def block_user(self, user_id, blocked=True):
        await self.db.execute(
            "UPDATE users SET is_blocked = ? WHERE user_id = ?",
            (1 if blocked else 0, user_id),
        )
        await self.db.commit()

    async def get_active_users(self):
        async with self.db.execute("SELECT user_id FROM users WHERE is_blocked = 0") as cursor:
            return await cursor.fetchall()

    async def get_user_count(self):
        async with self.db.execute("SELECT COUNT(*) FROM users") as cursor:
            row = await cursor.fetchone()
            return row[0]

    async def add_qr_code(self, user_id, qr_type, data, fmt):
        await self.db.execute(
            "INSERT INTO qr_codes (user_id, qr_type, data, format) VALUES (?, ?, ?, ?)",
            (user_id, qr_type, data, fmt),
        )
        await self.db.commit()

    async def get_qr_count(self):
        async with self.db.execute("SELECT COUNT(*) FROM qr_codes") as cursor:
            row = await cursor.fetchone()
            return row[0]

    async def get_user_qr_count(self, user_id):
        async with self.db.execute(
            "SELECT COUNT(*) FROM qr_codes WHERE user_id = ?", (user_id,)
        ) as cursor:
            row = await cursor.fetchone()
            return row[0]

    async def get_today_stats(self):
        import datetime
        today = datetime.date.today().isoformat()
        async with self.db.execute(
            "SELECT COUNT(*) FROM users WHERE DATE(joined_at) = ?", (today,)
        ) as cursor:
            new_users = (await cursor.fetchone())[0]
        async with self.db.execute(
            "SELECT COUNT(*) FROM qr_codes WHERE DATE(created_at) = ?", (today,)
        ) as cursor:
            today_qr = (await cursor.fetchone())[0]
        return new_users, today_qr

    async def add_channel(self, channel_id, channel_title, invite_link=""):
        await self.db.execute(
            "INSERT OR REPLACE INTO channels (channel_id, channel_title, invite_link) VALUES (?, ?, ?)",
            (channel_id, channel_title, invite_link),
        )
        await self.db.commit()

    async def remove_channel(self, channel_id):
        await self.db.execute("DELETE FROM channels WHERE channel_id = ?", (channel_id,))
        await self.db.commit()

    async def get_channels(self):
        async with self.db.execute("SELECT channel_id, channel_title, invite_link FROM channels") as cursor:
            return await cursor.fetchall()

    async def add_broadcast(self, admin_id, text, sent_count, failed_count):
        await self.db.execute(
            "INSERT INTO broadcasts (admin_id, text, sent_count, failed_count) VALUES (?, ?, ?, ?)",
            (admin_id, text, sent_count, failed_count),
        )
        await self.db.commit()

    async def close(self):
        if self.db:
            await self.db.close()


db = Database()
