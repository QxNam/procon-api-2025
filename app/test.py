from services.judge import *
from utils.file_tool import load_json_file, save_json_file

def load_board(file_path):
    data = load_json_file(file_path)
    problem = data.get("problem", {}).get("field", {})
    return problem

def load_answer(file_path):
    data = load_json_file(file_path)
    answer = data.get("ops", [])
    return answer

def transform():
    problem = load_board("./test/sample/question.json")
    ops = load_answer("./test/sample/answer.json")
    result = judge(problem, ops)
    return result


result = transform()
save_json_file("./test/sample/result.json", result)
print("Transformation complete. Result saved to ./test/sample/result.json")
