import sys
sys.path.append('.')
sys.path.append('src')

from utils.config import TransferConfig
from utils.log import ScheduleLog
from transfer import select_bot, transfer

def main(config_path: str):
    config = TransferConfig(config_path)
                     
    bot = select_bot(config.prompt, 
        config.retrieval_type, config.retrieval_path)


    sLog = ScheduleLog()
    while True:
        sentence = input("input:\t")
        if sentence == "exit":
            break
        
        sLog.mark()

        # the type of return value is dict
        output = transfer(bot, sentence)
        take_time = sLog.take_time

        output_result = {
            'prompt': '\n' + output['prompt'],
            'result': output['result'],
            'time': "%.3fs"%take_time
        }

        for (key, value) in output_result.items():
            print('-' * 30)
            print("{}:\t{}".format(key, value))
        print('=' * 30)

if __name__ == '__main__':
    config_path = ''
    main(config_path)