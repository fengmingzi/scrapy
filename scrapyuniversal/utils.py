from os.path import realpath, dirname
import json


def get_config(name):
    # 获取抽离出来的json配置文件中的数据，TODO 这里我们也可以写成调用api接口来获取数据
    path = dirname(realpath(__file__)) + '/configs/' + name + '.json'
    with open(path, 'r', encoding='utf-8') as f:
        return json.loads(f.read())