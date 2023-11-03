import json
import os


def update_record(record_file, username, bankname, accuracy, new_errors):
    if not os.path.exists(record_file):
        with open(record_file, 'w', encoding='utf-8') as file:
            json.dump([], file)

    try:
        with open(record_file, 'r', encoding='utf-8') as file:
            records = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        records = []

    record_found = False
    for record in records:
        if record['user'] == username and record['bank'] == bankname:
            record['times'] += 1
            record['accuracy'] = accuracy

            for question_type in ['单选', '判断']:
                if question_type not in record['error']:
                    record['error'][question_type] = []
                for error in new_errors.get(question_type, []):
                    if error not in record['error'][question_type]:
                        record['error'][question_type].append(error)

            record_found = True
            break

    if not record_found:
        new_record = {
            "user": username,
            "bank": bankname,
            "times": 1,
            "accuracy": accuracy,
            "error": new_errors
        }
        records.append(new_record)

    with open(record_file, 'w', encoding='utf-8') as file:
        json.dump(records, file, ensure_ascii=False, indent=4)



def get_error_question_numbers(username, bankname):
    try:
        with open('record.json', 'r', encoding='utf-8') as file:
            records = json.load(file)

        for record in records:
            if record['user'] == username and record['bank'] == bankname:
                error_dict = record['error']
                # 确保每种题型都有一个错误列表，即使列表可能为空
                error_dict.setdefault('单选', [])
                error_dict.setdefault('判断', [])
                return error_dict

    except (FileNotFoundError, json.JSONDecodeError):
        pass

    # 如果没有找到匹配的记录，返回包含空列表的字典
    return {'单选': [], '判断': []}

# 使用函数示例
# 如果需要测试此函数，可以取消注释以下代码
# if __name__ == "__main__":
#     update_record('record.json', 'xxx', 'example.xls', '80%', [1, 3, 5])
