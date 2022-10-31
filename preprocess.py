import os 
import json
import re
raw_data_path = "news_crawler/vietnamnet"

CATEGORIES = {
    'kinh-doanh': 'Kinh doanh',
    'khoa-hoc': 'Khoa học',
    'giai-tri': 'Giải trí',
    'the-thao': 'Thể thao',
    'phap-luat': 'Pháp luật',
    'giao-duc': 'Giáo dục',
    'suc-khoe': 'Sức khoẻ - Y tế',
    'doi-song': 'Đời sống',
    'du-lich': 'Du lịch'
}
def combine_data():
    for CATEGORY in CATEGORIES:
        folder_path = raw_data_path + "/" + CATEGORIES[CATEGORY]
        files = os.listdir(folder_path)
        data = list()
        for file in files:
            file_path = folder_path + "/" + file
            with open(file_path, 'r') as f:
                data.append(json.load(f))
        # print(data)
        with open(raw_data_path + "/" + CATEGORY + ".json", 'w') as f:
            json.dump(data, f)

def combine_all_data():
    data = []
    for CATEGORY in CATEGORIES:
        path = raw_data_path + "/" + CATEGORY + ".json"
        f = open(path,encoding = 'utf-8-sig')
        for item in json.load(f):
            data.append(item)
        f.close()
    with open(raw_data_path + "/" + 'data' + ".json", 'w') as f:
        json.dump(data, f)

def create_stopwords():
    with open("stopwords-origin.txt") as file_in:
        words = set()
        for line in file_in:
            line = line.rstrip('\n')
            line = line.split(" ")
            if len(line) == 1:
                words.add(line[0])
        words = list(words)
        words.sort()
        with open('stopwords.txt', 'w') as f:
            for word in words:
                f.write(f"{word}\n")

def get_data(path):
    f = open(path,encoding = 'utf-8-sig')
    data = json.load(f)
    X = [clean_text(choice_content(item)) for item in data]
    y = [list(CATEGORIES).index(item['label']) for item in data]
    f.close()
    return X, y

def clean_text(text):
    word_len_limit = 20
    f = open('stopwords.txt')
    stop_words = [stop_word for stop_word in f.read().split('\n')]
    f.close()
    # Clean (convert to lowercase and remove punctuations and characters and then strip)
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    # Remove number
    text = re.sub(r'\d', ' ', text)
    # Remove duplicate space
    text = re.sub(r' +', ' ', text)
    # Remove stopwords
    text = " ".join([word for word in text.split() if ((word not in stop_words) and (len(word) < word_len_limit))])
    return text
def choice_content(item):
    return item['title'] + ' ' + item['description'] + ' ' + item['content']
if __name__ == '__main__':
    # combine_data()
    # create_stopwords()
    # print(get_data("the-thao"))
    combine_all_data()
    # pass
