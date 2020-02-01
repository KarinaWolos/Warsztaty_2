from models import Message, User
import argparse
from database import get_connection, get_cursor
from clcrypto import check_password
import datetime



parser = argparse.ArgumentParser(description="Opis naszej aplikacji")
parser.add_argument('-u', '--user', type=str, help="Pomoc komendy. Użycie -u login użytkownika")
parser.add_argument('-p', '--password', type=str, help="Pomoc komendy. Użycie -p hasło")
parser.add_argument('-l', '--list', help="Pomoc komendy. Użycie -l listowanie wszystkich komunikatów", required=False, default="")
parser.add_argument('-t', '--to', type=str, help="Pomoc komendy. Użycie -t login użytkownika do którego chcemy nadać komunikat")
parser.add_argument('-s', '--send', help="Pomoc komendy. Uzycie -s treść komunikatu")

args = parser.parse_args()

if __name__ == '__main__':
    connection = get_connection()
    cursor = get_cursor(connection)


    if args.user and args.password:
        print(f"Podany login: {args.user}, podane hasło to: {args.password}")

        from_user = User.load_user_by_username(cursor, args.user)
        if check_password(args.password, from_user.hashed_password):
            print("Popawne hasło")
            if args.to:
                to_user = User.load_user_by_username(cursor, args.to)
                print('Adresat znajduje sie w bazie danych')
                if to_user and args.send:
                    message = Message()
                    message.from_id = from_user.id
                    message.to_id = to_user.id
                    message.text = args.send
                    message.creation_date = datetime.datetime.today()
                    message.save_to_db(cursor)
                    print(f'Wysłano wiadomość do użytkownika {args.to}')
                if not to_user:
                    print('Niepoprawny login adresata')
                if not args.send:
                    print('Komunikat musi zawierać treśc')

            elif args.list:
                loaded_user = User.load_user_by_username(cursor, args.user)
                messages = Message.load_all_messages_for_user(cursor, loaded_user.id)
                print("ID: \t Od: \t Treść: \t Data:")
                for message in messages:
                    print(message.id, '\t', message.from_id, '\t', message.text, '\t', message.creation_date)

        else:
            print('Niepoprawne hasło')



    connection.close()