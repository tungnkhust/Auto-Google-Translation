from src.utils import load_json, write_json
from math import floor
from src.drive import create_chrome_driver
from selenium.webdriver.support.ui import WebDriverWait
from src.goolge_translate import translate
import argparse
from multiprocessing.pool import ThreadPool

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input_file', default=None,
                    help='The input English SQuAD file', required=True)
parser.add_argument('-o', '--output_file', default=None,
                    help='The output SQuAD file that have been translated into Vietnamese', required=True)
parser.add_argument('-e', '--encoding', default="utf-8",
                    help='The default encoding of the input/output dataset', required=False)
parser.add_argument('-cp', '--chrome_path', default='driver/chromedriver',
                    help='The path to chrome driver')
parser.add_argument('-t', '--num_threads', default=4,
                    help='The number of threads used for translation', required=False)

args = parser.parse_args()


json_result = []
count_para = 0
count_ques = 0
count_error = 0
text_error = []


def load_data(input_file, num_threads=4, encoding='utf-8'):
    squad_json = load_json(input_file, encoding=encoding)
    squad_json = squad_json['data']

    # divide data into x parts
    div = floor(len(squad_json) / num_threads)
    divided_squad_json = [[squad_json[i] for i in range(div)]]
    for i in range(1, num_threads - 1):
        divided_squad_json.append([squad_json[j] for j in range(div * i, div * (i + 1))])
    divided_squad_json.append([squad_json[i] for i in range(div * (num_threads - 1), len(squad_json))])
    return divided_squad_json


def translate_squad_vie(squad_json):
    driver = create_chrome_driver(chrome_path=args.chrome_path)
    driver.get("https://translate.google.com/?hl=vi#view=home&op=translate&sl=en&tl=vi")
    wait = WebDriverWait(driver, 20)
    print("Thread job's start!!!")
    global count_para, count_ques
    for item in squad_json:
        paragraphs = item['paragraphs']
        for para in paragraphs:
            para['context'] = translate(driver, wait, para['context'])
            count_para = count_para + 1
            print("para: ", count_para)
            qas_list = para['qas']
            for qas in qas_list:
                count_ques = count_ques + 1
                print("ques: ", count_ques)
                qas['question'] = translate(driver, wait, qas['question'])

    global json_result
    json_result.extend(squad_json)
    driver.quit()
    print("Thread job's done!!!")


if __name__ == "__main__":
    ThreadPool(args.num_threads).map(translate_squad_vie,
                                     load_data(args.input_file, encoding=args.encoding))
    write_json(json_result, args.output_file, encoding=args.encoding)