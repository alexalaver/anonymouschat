import psycopg2

class Data:
    def __init__(self, host1, port1, data, user1, password1):
        self.connect = psycopg2.connect(
            host=host1,
            port=port1,
            database=data,
            user=user1,
            password=password1
        )
        self.cursor = self.connect.cursor()

    def add_user(self, id, user_id, first_name, username, gender, age):
        with self.connect:
            self.cursor.execute("INSERT INTO users(id, user_id, first_name, username, gender, age) VALUES(%s, %s, %s, %s, %s, %s)", (id, user_id, first_name, username, gender, age,))
            self.connect.commit()

    def check_user(self, id):
        with self.connect:
            self.cursor.execute("SELECT user_id FROM users WHERE user_id=%s", (id,))
            return bool(len(self.cursor.fetchall()))

    def check_numbers_id(self):
        with self.connect:
            self.cursor.execute("SELECT id FROM users ORDER BY id DESC LIMIT 1;")
            a = self.cursor.fetchone()
            if a is None:
                return 0
            else:
                return a[0]

    def check_queue(self, id):
        with self.connect:
            self.cursor.execute("SELECT user_id FROM queue WHERE user_id=%s", (id,))
            return bool(len(self.cursor.fetchall()))

    def get_active_chat(self, user_id):
        with self.connect:
            self.cursor.execute("SELECT id FROM chats WHERE user_first=%s OR user_second=%s", (user_id, user_id,))
            return bool(len(self.cursor.fetchall()))

    def add_queue_all(self, id, user_id):
        with self.connect:
            self.cursor.execute("INSERT INTO queue(id, user_id) VALUES(%s, %s)", (id, user_id,))
            self.connect.commit()

    def check_numbers_id_queue(self):
        with self.connect:
            self.cursor.execute("SELECT id FROM queue ORDER BY id DESC LIMIT 1;")
            a = self.cursor.fetchone()
            if a is None:
                return 0
            else:
                return a[0]


    def get_user_queue(self):
        with self.connect:
            self.cursor.execute("SELECT user_id FROM queue")
            user = self.cursor.fetchone()
            if user is not None and bool(len(user)):
                return user[0]
            else:
                return False

    def create_chat_all(self, id, user_first, user_second):
        with self.connect:
            if user_first != 0:
                self.cursor.execute("DELETE FROM queue WHERE user_id=%s", (user_second,))
                self.cursor.execute("INSERT INTO chats(id, user_first, user_second) VALUES(%s, %s)", (id, user_first, user_second,))
                self.connect.commit()
                return True
            else:
                return False

    def check_numbers_id_chat(self):
        with self.connect:
            self.cursor.execute("SELECT id FROM chats ORDER BY id DESC LIMIT 1;")
            a = self.cursor.fetchone()
            if a is None:
                return 0
            else:
                return a[0]