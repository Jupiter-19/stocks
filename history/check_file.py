import os


def list_files_in_directory(path, start="", end=""):
    files = []
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        if not (filename.startswith(start) and filename.endswith(end)):
            continue
        if os.path.isfile(file_path):
            files.append(file_path)
    return files


def read_first_line(file_path):
    with open(file_path, 'r', encoding='gbk') as file:
        first_line = file.readline()
    return first_line.strip()  # 去掉行尾的换行符


def check_head(file):
    line = read_first_line(file)
    line = [tmp.strip() for tmp in line.split(",")]
    assert line == ['成交日期', '成交时间', '证券代码', '证券名称', '委托方向', '成交数量', '成交均价', '成交金额', '佣金', '印花税']


if __name__ == '__main__':
    csv_files = list_files_in_directory(path="./", end=".csv")
    for file in csv_files:
        check_head(file)
