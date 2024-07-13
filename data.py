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

    def check_queue_male(self, id):
        with self.connect:
            self.cursor.execute("SELECT user_id FROM queue_male WHERE user_id=%s", (id,))
            return bool(len(self.cursor.fetchall()))

    def check_queue_female(self, id):
        with self.connect:
            self.cursor.execute("SELECT user_id FROM queue_female WHERE user_id=%s", (id,))
            return bool(len(self.cursor.fetchall()))

    def delete_queue_all(self, id):
        with self.connect:
            self.cursor.execute("DELETE FROM queue WHERE user_id=%s", (id,))
            self.cursor.execute("DELETE FROM queue_male WHERE user_id=%s", (id,))
            self.cursor.execute("DELETE FROM queue_female WHERE user_id=%s", (id,))
            self.connect.commit()

    def get_active_chat(self, user_id):
        with self.connect:
            self.cursor.execute("SELECT id FROM chats WHERE user_first=%s OR user_second=%s", (user_id, user_id,))
            return bool(len(self.cursor.fetchall()))

    def add_queue_all(self, user_id):
        with self.connect:
            self.cursor.execute("INSERT INTO queue(user_id) VALUES(%s)", (user_id,))
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

    def get_user_queue_male(self):
        with self.connect:
            self.cursor.execute("SELECT user_id FROM queue_male")
            user = self.cursor.fetchone()
            if user is not None and bool(len(user)):
                return user[0]
            else:
                return False

    def get_user_queue_female(self):
        with self.connect:
            self.cursor.execute("SELECT user_id FROM queue_female")
            user = self.cursor.fetchone()
            if user is not None and bool(len(user)):
                return user[0]
            else:
                return False

    def create_chat_all(self, id, user_first, user_second, search_gender_first, search_gender_second):
        with self.connect:
            if user_first != 0:
                self.cursor.execute("INSERT INTO chats(id, user_first, user_second, search_gender_first, search_gender_second) VALUES(%s, %s, %s, %s, %s)", (id, user_first, user_second, search_gender_first, search_gender_second,))
                self.connect.commit()
                return True
            else:
                return False

    def delete_queue(self, user_second):
        with self.connect:
            self.cursor.execute("DELETE FROM queue WHERE user_id=%s", (user_second,))
            self.connect.commit()

    def delete_queue_male(self, user_second):
        with self.connect:
            self.cursor.execute("DELETE FROM queue_male WHERE user_id=%s", (user_second,))
            self.connect.commit()

    def delete_queue_female(self, user_second):
        with self.connect:
            self.cursor.execute("DELETE FROM queue_female WHERE user_id=%s", (user_second,))
            self.connect.commit()

    def check_numbers_id_chat(self):
        with self.connect:
            self.cursor.execute("SELECT id FROM chats ORDER BY id DESC LIMIT 1;")
            a = self.cursor.fetchone()
            if a is None:
                return 0
            else:
                return a[0]

    def get_active_chat_second(self, user_id):
        with self.connect:
            self.cursor.execute("SELECT * FROM chats WHERE user_first=%s OR user_second=%s", (user_id, user_id,))
            users = self.cursor.fetchone()
            if users is not None:
                if users[1] == user_id:
                    return users[2]
                elif users[2] == user_id:
                    return users[1]
            else:
                return False

    def delete_chats(self, user_id):
        with self.connect:
            self.cursor.execute("DELETE FROM chats WHERE user_first=%s OR user_second=%s", (user_id, user_id,))
            self.connect.commit()


    def select_gender_users(self, user_id):
        with self.connect:
            self.cursor.execute("SELECT gender FROM users WHERE user_id=%s", (user_id,))
            gender = self.cursor.fetchone()
            if gender is not None:
                return gender[0]
            else:
                return False

    def select_search_gender(self, user_id):
        with self.connect:
            self.cursor.execute("SELECT id FROM chats WHERE user_first=%s", (user_id,))
            first = self.cursor.fetchone()
            print(f"{first} FIRST")
            if first is None:
                self.cursor.execute("SELECT id FROM chats WHERE user_second=%s", (user_id,))
                second = self.cursor.fetchone()
                print(f"{second} SECOND")
                if second is None:
                    return None
                else:
                    self.cursor.execute("SELECT search_gender_second FROM chats WHERE id=%s", (second[0]))
                    print(f"RIGHT {self.cursor.fetchone()[0]}")
                    return self.cursor.fetchone()[0]
            else:
                self.cursor.execute("SELECT search_gender_first FROM chats WHERE id=%s", (first[0]))
                print(f"RIGHT 2 {self.cursor.fetchone()[0]}")
                return self.cursor.fetchone()[0]

    def get_full_chats_info(self, user_id):
        with self.connect:
            self.cursor.execute("SELECT * FROM chats WHERE user_first=%s OR user_second=%s", (user_id, user_id,))
            result = self.cursor.fetchall()[0]
            result = [item for item in result]
            return result

    def add_queue_female(self, user_id):
        with self.connect:
            self.cursor.execute("INSERT INTO queue_female(user_id) VALUES(%s)", (user_id,))
            self.connect.commit()

    def add_queue_male(self, user_id):
        with self.connect:
            self.cursor.execute("INSERT INTO queue_male(user_id) VALUES(%s)", (user_id,))
            self.connect.commit()

    def select_tarife(self, user_id):
        with self.connect:
            self.cursor.execute("SELECT tarife FROM users WHERE user_id=%s", (user_id,))
            tarife = self.cursor.fetchone()
            if tarife is None:
                return None
            else:
                return tarife[0]

    def update_tarife(self, user_id, tarife):
        with self.connect:
            self.cursor.execute("UPDATE users SET tarife=%s WHERE user_id=%s", (tarife, user_id,))
            self.connect.commit()

    def select_channels(self):
        with self.connect:
            self.cursor.execute("SELECT channel FROM channels")
            channel = self.cursor.fetchone()
            if channel is None:
                return None
            else:
                return channel[0]

    def update_channels(self, channel):
        with self.connect:
            self.cursor.execute("UPDATE channels SET channel=%s", (channel,))
            self.connect.commit()

    def add_channels(self, channel):
        with self.connect:
            self.cursor.execute("INSERT INTO channels(channel) VALUES(%s)", (channel,))
            self.connect.commit()

    def select_adminka(self, user_id):
        with self.connect:
            self.cursor.execute("SELECT adminka FROM users WHERE user_id=%s", (user_id,))
            return self.cursor.fetchone()[0]

    def select_all_id(self):
        with self.connect:
            self.cursor.execute("SELECT user_id FROM users")
            users = self.cursor.fetchall()
            users = [i[0] for i in users]
            return users