import sys
sys.path.append('.')

from src.bot import Bot

def main():
    bot = Bot()

    while True:
        query = input("input: ")
        if query == 'exit':
            break

        answer = bot.ask(query)
        print("bot:", answer)    


if __name__ == '__main__':
    main()