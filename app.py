from flask import Flask, render_template, request, jsonify
from sudoku import create_sudoku
import random

app = Flask(__name__)


# 生成一个随机的四位数，所有位数不同
def generate_number():
    digits = random.sample(range(10), 4)
    return ''.join(map(str, digits))


# 初始化游戏数据
secret_number = generate_number()
attempts = []


# 计算 A 和 B 的数量
def evaluate_guess(secret, guess):
    A = sum(1 for x, y in zip(secret, guess) if x == y)
    B = sum(1 for x in guess if x in secret) - A
    return f"{A}A{B}B"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/guess-number')
def guess_number():
    return render_template('guess_number.html')


@app.route('/guess', methods=['POST'])
def guess():
    global secret_number, attempts
    guess = request.form['guess']

    # 验证输入是一个不重复的四位数字
    if len(guess) != 4 or not guess.isdigit() or len(set(guess)) != 4:
        return jsonify({'error': '请输入一个各位不重复的四位数！'})

    result = evaluate_guess(secret_number, guess)
    attempts.append({'guess': guess, 'result': result})

    # 如果猜对了，返回游戏结束提示
    if result == '4A0B':
        return jsonify({'attempts': attempts, 'message': "恭喜你猜对了！是否重新开始？", 'game_over': True})

    return jsonify({'attempts': attempts, 'message': None, 'game_over': False})


@app.route('/reset', methods=['POST'])
def reset():
    global secret_number, attempts
    secret_number = generate_number()  # 重新生成数字
    attempts = []  # 清空历史记录
    return jsonify({'message': '游戏已重置，请重新开始！'})


@app.route('/sudoku')
def sudoku_page():
    return render_template('sudoku.html')


@app.route('/new-sudoku')
def new_sudoku():
    difficulty = request.args.get('difficulty', 'medium')
    puzzle = create_sudoku.generate_sudoku(difficulty)
    return jsonify({'puzzle': puzzle})


if __name__ == '__main__':
    app.run(debug=True)
