from models import User
import argparse
from clcrypto import check_password
from database import get_connection, get_cursor

parser = argparse.ArgumentParser(description="Opis naszej aplikacji")
parser.add_argument('-u', '--user', type=str, help="Pomoc komendy. Użycie -u login")
parser.add_argument('-p', '--password', type=str, help="Pomoc komendy. Użycie -p hasło")
parser.add_argument('-a', '--aaa', type=str, help="Pomoc komendy. Użycie -a adres email")
parser.add_argument('-n', '--newpassword', type=str, help="Pomoc komendy. Użycie -n nowe hasło")
parser.add_argument('-e', '--edit', type=str, help="Pomoc komendy. Uzycie -e login użytkownika do modyfikacji")
parser.add_argument('-l', '--list', type=str, help="Pomoc komendy. Użycie -l listowanie wszystkich użytkowników", required=False, default="")
parser.add_argument('-d', '--delete', type=str, help="Pomoc komendy. Użycie -d login użytkownika do usunięcia")

args = parser.parse_args()

if __name__ == '__main__':
    connection = get_connection()
    cursor = get_cursor(connection)


    if args.list:
        print('Wyświetlam listę zarejestrowanych użytkowników')

        loaded_users = User.load_all_users(cursor)
        for user in loaded_users:
            print(user.username, user.email)


    elif args.user and args.password:
        print(f"Podany login: {args.user}, podany mail: {args.aaa} a podane hasło to: {args.password}")

        loaded_user = User.load_user_by_username(cursor, args.user)

        if args.edit:
            loaded_user = User.load_user_by_username(cursor, args.edit)

            if check_password(args.password, loaded_user.hashed_password):
                print("Popawne hasło")
                loaded_user.set_password(args.newpassword)
                loaded_user.save_to_db(cursor)
                print('Zmieniono hasło')
            else:
                print("Błędne hasło")

        elif args.delete:
            print(f"Usunięto użytkownika o loginie: {args.delete}")

            loaded_user = User.load_user_by_username(cursor, args.delete)
            if loaded_user and check_password(args.password, loaded_user.hashed_password):
                loaded_user.delete(cursor)
                print('Done')


        elif loaded_user and check_password(args.password, loaded_user.hashed_password):
            print("Poprawne dane")
        else:
            print("Błędne dane")
        if not loaded_user:
            user = User()
            user.username = args.user
            user.email = args.aaa
            user.set_password(args.password)
            user.save_to_db(cursor)
            print('Zapisano użykwnika do bazy danych')





    connection.close()
