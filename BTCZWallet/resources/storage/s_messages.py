
import sqlite3

from toga import App
from ...framework import Os



class StorageMessages:
    def __init__(self, app:App):
        super().__init__()

        self.app = app
        self.app_data = self.app.paths.data
        self.data = Os.Path.Combine(str(self.app_data), 'messages.dat')
        Os.FileStream(
            self.data,
            Os.FileMode.OpenOrCreate,
            Os.FileAccess.ReadWrite,
            Os.FileShare.ReadWrite
        )


    def is_exists(self):
        if not Os.File.Exists(self.data):
            return None
        return self.data


    def identity(self, category, username, address):
        self.create_identity_table()
        with sqlite3.connect(self.data) as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''
                INSERT INTO identity (category, username, address)
                VALUES (?, ?, ?)
                ''',
                (category, username, address)
            )


    def get_identity(self, option = None):
        try:
            with sqlite3.connect(self.data) as conn:
                cursor = conn.cursor()
                if option == "category":
                    cursor.execute(
                        "SELECT category FROM identity"
                    )
                    result = cursor.fetchone()
                elif option == "username":
                    cursor.execute(
                        "SELECT username FROM identity"
                    )
                    result = cursor.fetchone()
                elif option == "address":
                    cursor.execute(
                        "SELECT address FROM identity"
                    )
                    result = cursor.fetchone()
                elif option is None:
                    cursor.execute(
                        "SELECT category, username, address FROM identity"
                    )
                    result = cursor.fetchone()
                return result
        except sqlite3.OperationalError:
            return None


    def add_contact(self, category, id, contact_id, username, address):
        self.create_contacts_table()
        with sqlite3.connect(self.data) as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''
                INSERT INTO contacts (category, id, contact_id, username, address)
                VALUES (?, ?, ?, ?, ?)
                ''',
                (category, id, contact_id, username, address)
            )


    def add_pending(self, category, id, username, address):
        self.create_pending_table()
        with sqlite3.connect(self.data) as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''
                INSERT INTO pending (category, id, username, address)
                VALUES (?, ?, ?, ?)
                ''',
                (category, id, username, address)
            )

    def add_request(self, id, address):
        self.create_requests_table()
        with sqlite3.connect(self.data) as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''
                INSERT INTO requests (id, address)
                VALUES (?, ?)
                ''',
                (id, address)
            )

    def key(self, prv_key):
        self.create_key_table()
        with sqlite3.connect(self.data) as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''
                INSERT INTO key (prv_key)
                VALUES (?)
                ''',
                (prv_key,)
            )

    def message(self, id, author, message, amount, timestamp, edited=None, replied = None):
        self.create_messages_table()
        self.add_column('messages', 'edited', 'INTEGER')
        self.add_column('messages', 'replied', 'INTEGER')
        with sqlite3.connect(self.data) as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''
                INSERT INTO messages (id, author, message, amount, timestamp, edited, replied)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ''',
                (id, author, message, amount, timestamp, edited, replied)
            )


    def unread_message(self, id, author, message, amount, timestamp, edited=None, replied = None):
        self.create_unread_messages_table()
        self.add_column('unread_messages', 'edited', 'INTEGER')
        self.add_column('unread_messages', 'replied', 'INTEGER')
        with sqlite3.connect(self.data) as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''
                INSERT INTO unread_messages (id, author, message, amount, timestamp, edited, replied)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ''',
                (id, author, message, amount, timestamp, edited, replied)
            )


    def ban(self, address, username):
        self.create_banned_table()
        self.add_column('banned', 'username', 'TEXT')
        with sqlite3.connect(self.data) as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''
                INSERT INTO banned (address, username)
                VALUES (?, ?)
                ''',
                (address, username)
            )


    def tx(self, txid):
        self.create_txs_table()
        with sqlite3.connect(self.data) as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''
                INSERT INTO txs (txid)
                VALUES (?)
                ''',
                (txid,)
            )


    def insert_market(self, contact_id, hostname, secret):
        self.create_market_table()
        with sqlite3.connect(self.data) as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''
                INSERT INTO market (contact_id, hostname, secret_key)
                VALUES (?, ?, ?)
                ''',
                (contact_id, hostname, secret)
            )


    def get_hostname(self, contact_id):
        try:
            with sqlite3.connect(self.data) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'SELECT hostname, secret_key FROM market WHERE contact_id = ?',
                    (contact_id,)
                )
                data = cursor.fetchone()
                return data
        except sqlite3.OperationalError:
            return None


    def get_txs(self):
        try:
            with sqlite3.connect(self.data) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT txid FROM txs')
                txs = [row[0] for row in cursor.fetchall()]
                return txs
        except sqlite3.OperationalError:
            return []


    def get_contacts(self, option = None):
        try:
            with sqlite3.connect(self.data) as conn:
                cursor = conn.cursor()
                if option == "address":
                    cursor.execute('SELECT address FROM contacts')
                    contacts = [row[0] for row in cursor.fetchall()]
                elif option == "contact_id":
                    cursor.execute('SELECT contact_id FROM contacts')
                    contacts = [row[0] for row in cursor.fetchall()]
                elif option is None:
                    cursor.execute('SELECT * FROM contacts')
                    contacts = cursor.fetchall()
                return contacts
        except sqlite3.OperationalError:
            return []


    def get_contact(self, contact_id):
        try:
            with sqlite3.connect(self.data) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'SELECT * FROM contacts WHERE contact_id = ?',
                    (contact_id,)
                )
                contact = cursor.fetchone()
                return contact
        except sqlite3.OperationalError:
            return None


    def get_contact_username(self, contact_id):
        try:
            with sqlite3.connect(self.data) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'SELECT username FROM contacts WHERE contact_id = ?',
                    (contact_id,)
                )
                contact = cursor.fetchone()
                return contact
        except sqlite3.OperationalError:
            return None


    def get_contact_address(self, contact_id):
        try:
            with sqlite3.connect(self.data) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'SELECT address FROM contacts WHERE contact_id = ?',
                    (contact_id,)
                )
                contact = cursor.fetchone()
                return contact
        except sqlite3.OperationalError:
            return None


    def get_id_contact(self, contact_id):
        try:
            with sqlite3.connect(self.data) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'SELECT id FROM contacts WHERE contact_id = ?',
                    (contact_id,)
                )
                id = cursor.fetchone()
                return id
        except sqlite3.OperationalError:
            return None


    def get_ids_contacts(self):
        try:
            with sqlite3.connect(self.data) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT id FROM contacts')
                data = cursor.fetchall()
                return [row[0] for row in data]
        except sqlite3.OperationalError:
            return []


    def get_pending(self, option = None):
        try:
            with sqlite3.connect(self.data) as conn:
                cursor = conn.cursor()
                if option == "address":
                    cursor.execute("SELECT address FROM pending")
                    contacts = [row[0] for row in cursor.fetchall()]
                elif option is None:
                    cursor.execute('SELECT * FROM pending')
                    contacts = cursor.fetchall()
                return contacts
        except sqlite3.OperationalError:
            return []


    def get_pending_single(self, pending_id):
        try:
            with sqlite3.connect(self.data) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'SELECT * FROM pending WHERE id = ?',
                    (pending_id,)
                )
                data = cursor.fetchone()
                return data
        except sqlite3.OperationalError:
            return None


    def get_requests(self):
        try:
            with sqlite3.connect(self.data) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT address FROM requests')
                txs = [row[0] for row in cursor.fetchall()]
                return txs
        except sqlite3.OperationalError:
            return []


    def get_request(self, address):
        try:
            with sqlite3.connect(self.data) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'SELECT id FROM requests WHERE address = ?',
                    (address,)
                )
                request = cursor.fetchone()
                return request
        except sqlite3.OperationalError:
            return None


    def get_messages(self, contact_id = None):
        try:
            self.add_column('messages', 'edited', 'INTEGER')
            self.add_column('messages', 'replied', 'INTEGER')
            with sqlite3.connect(self.data) as conn:
                cursor = conn.cursor()
                if contact_id:
                    cursor.execute(
                        'SELECT author, message, amount, timestamp, edited, replied FROM messages WHERE id = ?',
                        (contact_id,)
                    )
                else:
                    cursor.execute('SELECT * FROM messages')
                messages = cursor.fetchall()
                return messages
        except sqlite3.OperationalError:
            return []


    def get_message(self, contact_id = None, timestamp=None):
        try:
            self.add_column('messages', 'edited', 'INTEGER')
            self.add_column('messages', 'replied', 'INTEGER')
            with sqlite3.connect(self.data) as conn:
                cursor = conn.cursor()
                if not contact_id:
                    cursor.execute(
                        'SELECT author, message FROM messages WHERE timestamp = ?',
                        (timestamp,)
                    )
                else:
                    cursor.execute(
                        'SELECT timestamp FROM messages WHERE id = ? AND timestamp = ?',
                        (contact_id, timestamp)
                    )
                data = cursor.fetchone()
                return data
        except sqlite3.OperationalError:
            return None


    def update_message(self, contact_id, message, timestamp, edit_timestamp):
        with sqlite3.connect(self.data) as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''
                UPDATE messages
                SET message = ?, edited = ?
                WHERE id = ? AND timestamp = ?
                ''', (message, edit_timestamp, contact_id, timestamp)
            )


    def get_unread_messages(self, contact_id=None):
        try:
            self.add_column('unread_messages', 'edited', 'INTEGER')
            self.add_column('unread_messages', 'replied', 'INTEGER')
            with sqlite3.connect(self.data) as conn:
                cursor = conn.cursor()
                if contact_id:
                    cursor.execute(
                        'SELECT author, message, amount, timestamp, edited, replied FROM unread_messages WHERE id = ?',
                        (contact_id,)
                    )
                else:
                    cursor.execute('SELECT * FROM unread_messages')
                messages = cursor.fetchall()
                return messages
        except sqlite3.OperationalError:
            return []


    def get_unread_message(self, contact_id=None, timestamp=None):
        try:
            self.add_column('unread_messages', 'edited', 'INTEGER')
            self.add_column('unread_messages', 'replied', 'INTEGER')
            with sqlite3.connect(self.data) as conn:
                cursor = conn.cursor()
                if not contact_id:
                    cursor.execute(
                        'SELECT author, message FROM unread_messages WHERE timestamp = ?',
                        (timestamp,)
                    )
                else:
                    cursor.execute(
                        'SELECT timestamp FROM unread_messages WHERE id = ? AND timestamp = ?',
                        (contact_id, timestamp)
                    )
                data = cursor.fetchone()
                return data
        except sqlite3.OperationalError:
            return None


    def update_unread_message(self, contact_id, message, timestamp, edit_timestamp):
        with sqlite3.connect(self.data) as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''
                UPDATE unread_messages
                SET message = ?, edited = ?
                WHERE id = ? AND timestamp = ?
                ''', (message, edit_timestamp, contact_id, timestamp)
            )


    def get_banned(self, option=None):
        try:
            self.add_column('banned', 'username', 'TEXT')
            with sqlite3.connect(self.data) as conn:
                cursor = conn.cursor()
                if option:
                    cursor.execute('SELECT address FROM banned')
                    data = [row[0] for row in cursor.fetchall()]
                else:
                    cursor.execute('SELECT * FROM banned')
                    data = cursor.fetchall()
                return data
        except sqlite3.OperationalError:
            return []


    def delete_pending(self, address):
        try:
            with sqlite3.connect(self.data) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    '''
                    DELETE FROM pending WHERE address = ?
                    ''',
                    (address,)
                )
        except sqlite3.OperationalError as e:
            print(f"Error deleting pending contact: {e}")


    def delete_contact(self, address):
        try:
            with sqlite3.connect(self.data) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    '''
                    DELETE FROM contacts WHERE address = ?
                    ''',
                    (address,)
                )
        except sqlite3.OperationalError as e:
            print(f"Error deleting contact: {e}")


    def delete_request(self, address):
        try:
            with sqlite3.connect(self.data) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    '''
                    DELETE FROM requests WHERE address = ?
                    ''',
                    (address,)
                )
        except sqlite3.OperationalError as e:
            print(f"Error deleting request: {e}")


    def delete_unread(self, contact_id=None):
        try:
            with sqlite3.connect(self.data) as conn:
                cursor = conn.cursor()
                if contact_id:
                    cursor.execute(
                        '''
                        DELETE FROM unread_messages WHERE id = ?
                        ''',
                        (contact_id,)
                    )
                else:
                    cursor.execute('DELETE FROM unread_messages')
        except sqlite3.OperationalError as e:
            print(f"Error deleting request: {e}")


    def delete_ban(self, address):
        try:
            with sqlite3.connect(self.data) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    '''
                    DELETE FROM banned WHERE address = ?
                    ''',
                    (address,)
                )
        except sqlite3.OperationalError as e:
            print(f"Error deleting banned contact: {e}")


    def create_identity_table(self):
        with sqlite3.connect(self.data) as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''
                CREATE TABLE IF NOT EXISTS identity (
                    category TEXT,
                    username TEXT,
                    address TEXT
                )
                '''
            )


    def edit_username(self, old_username, new_username):
        with sqlite3.connect(self.data) as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''
                UPDATE identity
                SET username = ?
                WHERE username = ?
                ''', (new_username, old_username)
            )


    def create_contacts_table(self):
        with sqlite3.connect(self.data) as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''
                CREATE TABLE IF NOT EXISTS contacts (
                    category TEXT,
                    id TEXT,
                    contact_id TEXT,
                    username TEXT,
                    address TEXT
                )
                '''
            )

    def update_contact_username(self, username, contact_id):
        with sqlite3.connect(self.data) as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''
                UPDATE contacts
                SET username = ?
                WHERE contact_id = ?
                ''', (username, contact_id)
            )

    def update_market(self, contact_id, hostname, secret):
        with sqlite3.connect(self.data) as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''
                UPDATE market
                SET hostname = ?, secret_key = ?
                WHERE contact_id = ?
                ''', (hostname, secret, contact_id)
            )

    def create_pending_table(self):
        with sqlite3.connect(self.data) as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''
                CREATE TABLE IF NOT EXISTS pending (
                    category TEXT,
                    id TEXT,
                    username TEXT,
                    address TEXT
                )
                '''
            )

    def create_messages_table(self):
        with sqlite3.connect(self.data) as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''
                CREATE TABLE IF NOT EXISTS messages (
                    id TEXT,
                    author TEXT,
                    message TEXT,
                    amount REAL,
                    timestamp INTEGER,
                    edited INTEGER,
                    replied INTEGER
                )
                '''
            )

    def create_unread_messages_table(self):
        with sqlite3.connect(self.data) as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''
                CREATE TABLE IF NOT EXISTS unread_messages (
                    id TEXT,
                    author TEXT,
                    message TEXT,
                    amount REAL,
                    timestamp INTEGER,
                    edited INTEGER,
                    replied INTEGER
                )
                '''
            )

    def create_txs_table(self):
        with sqlite3.connect(self.data) as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''
                CREATE TABLE IF NOT EXISTS txs (
                    txid TEXT
                )
                '''
            )

    def create_key_table(self):
        with sqlite3.connect(self.data) as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''
                CREATE TABLE IF NOT EXISTS key (
                    prv_key TEXT
                )
                '''
            )

    def create_requests_table(self):
        with sqlite3.connect(self.data) as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''
                CREATE TABLE IF NOT EXISTS requests (
                    id TEXT,
                    address TEXT
                )
                '''
            )

    def create_banned_table(self):
        with sqlite3.connect(self.data) as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''
                CREATE TABLE IF NOT EXISTS banned (
                    address TEXT,
                    username TEXT
                )
                '''
            )


    def create_market_table(self):
        with sqlite3.connect(self.data) as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''
                CREATE TABLE IF NOT EXISTS market (
                    contact_id TEXT,
                    hostname TEXT,
                    secret_key TEXT
                )
                '''
            )


    def add_column(self, table_name, column_name, column_type):
        with sqlite3.connect(self.data) as conn:
            cursor = conn.cursor()
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [row[1] for row in cursor.fetchall()]

            if column_name not in columns:
                cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}")
