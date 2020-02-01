import sys

sys.path.append("..")

# CREATE TABLE Message
# (
#     id            serial NOT NULL,
#     from_id       int    NOT NULL,
#     to_id         int    NOT NULL,
#     text          text,
#     creation_date timestamp,
#     PRIMARY KEY (id),
#     FOREIGN KEY (from_id) REFERENCES users (id),
#     FOREIGN KEY (to_id) REFERENCES users (id)
# );


class Message:
    __id = None
    from_id = None
    to_id = None
    text = None
    creation_date = None

    def __init__(self):
        self.__id = -1
        self.from_id = ""
        self.to_id = ""
        self.creation_date = ""

    @property
    def message_id(self):
        return self.__id

    @staticmethod
    def load_message_by_id(cursor, message_id):
        sql = "SELECT id, from_id, to_id, text, creation_date FROM message WHERE id=%s"
        cursor.execute(sql, (message_id,))
        data = cursor.fetchone()
        if data:
            loaded_message = Message()
            loaded_message.__id = data['id']
            loaded_message.from_id = data['from_id']
            loaded_message.to_id = data['to_id']
            loaded_message.text = data['text']
            loaded_message.creation_date = data['creation_date']
            return loaded_message
        else:
            return None

    @staticmethod
    def load_all_messages(cursor):
        sql = """SELECT * FROM message ORDER BY creation_date DESC;"""
        cursor.execute(sql)
        messages = []
        for message in cursor.fetchall():
            loaded_message = Message()
            loaded_message.__id = message['id']
            loaded_message.from_id = message['from_id']
            loaded_message.to_id = message['to_id']
            loaded_message.text = message['text']
            loaded_message.creation_date = message['creation_date']
            messages.append(loaded_message)
        return messages

    def save_to_db(self, cursor):
        if self.__id == -1:
            sql = """INSERT INTO message(from_id, to_id, text, creation_date)
                     VALUES(%s, %s, %s, %s) RETURNING id"""
            values = (self.from_id, self.to_id, self.text, self.creation_date)
            cursor.execute(sql, values)
            self.__id = cursor.fetchone()['id']
            return True
        else:
            sql = """UPDATE message SET from_id=%s, to_id=%s, text=%s, creation_date=%s  WHERE id=%s"""
            values = (self.from_id, self.to_id, self.text, self.creation_date, self.__id)
            cursor.execute(sql, values)
            return True

    @staticmethod
    def load_all_messages_for_user(cursor, to_id):
        sql = "SELECT id, from_id, text, creation_date FROM message WHERE to_id=%s"
        cursor.execute(sql, (to_id,))
        messages = []
        for message in cursor.fetchall():
            loaded_message = Message()
            loaded_message.__id = message['id']
            cursor.execute(f"SELECT email FROM users WHERE id={message['from_id']}")
            loaded_message.email = cursor.fetchone()['email']
            loaded_message.text = message['text']
            loaded_message.creation_date = message['creation_date']
            messages.append(loaded_message)
        return messages



