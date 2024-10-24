import random
from collections import defaultdict

FILE_NAME = "input_melody2.txt" # メロディのファイル名

# テキストファイルからメロディを読み込み
def load_melody(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return [line.strip().split() for line in f.readlines()]

# 遷移辞書を作成
def build_markov_chain(melody_data):
    chain = defaultdict(lambda: defaultdict(int)) # dafaultdictは存在しないキーには0が入る
    # 
    for measure in melody_data:
        for i in range(len(measure) - 1):
            current = measure[i]
            next_note = measure[i + 1]
            chain[current][next_note] += 1
    # 遷移確率を計算
    for current, transitions in chain.items():
        total = sum(transitions.values())
        for next_note in transitions:
            transitions[next_note] /= total
    return chain

# 遷移確率に基づき新しいメロディを生成
def generate_melody(chain, measures=8, notes_per_measure=4):
    melody = []
    all_notes = list(chain.keys())  # すべての音符のリスト

    # 現在の音符をランダムに選ぶ
    current_note = 'ド'

    for _ in range(measures):
        measure = []
        for _ in range(notes_per_measure):
            measure.append(current_note)

            # 次の音符を取得
            next_notes = list(chain[current_note].keys())
            probabilities = list(chain[current_note].values())

            if next_notes:
                # 遷移先がある場合はその中から選ぶ
                current_note = random.choices(next_notes, probabilities)[0]
            else:
                # 遷移先がない場合は全体からランダムに選ぶ
                current_note = random.choice(all_notes)

        melody.append(measure)  # 小節を追加

    return melody

# メロディをテキスト形式で保存する関数
def save_melody(melody, filename="generated_melody.txt"):
    with open(filename, 'w', encoding='utf-8') as f:
        for measure in melody:
            f.write(' '.join(measure) + '\n')  # 小節ごとに改行して保存

# メイン処理
if __name__ == "__main__":
    # 入力ファイルの読み込み
    melody_data = load_melody(FILE_NAME)

    # マルコフ連鎖の遷移辞書を作成
    markov_chain = build_markov_chain(melody_data)

    # 新しいメロディを生成（8小節、4音符/小節）
    generated_melody = generate_melody(markov_chain, measures=8, notes_per_measure=4)

    # 生成したメロディを保存
    save_melody(generated_melody)
