import random
from collections import defaultdict

FILE_NAME = "input_melody2.txt" # メロディのファイル名

# メロディを読み込み
def load_melody(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        # 空白で分けてリスト型でいれる。改行で列が変わる。
        return [line.strip().split() for line in f.readlines()] 

# 遷移辞書を作成
def build_markov_chain(melody_data):
    # 二次元の辞書を作成
    chain = defaultdict(lambda: defaultdict(int)) # dafaultdictは存在しないキーには0を入れる
    # melody_dataから
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

# 遷移確率から新しいメロディを生成
def generate_melody(chain, measures=8, notes_per_measure=4):
    melody = []
    # 辞書に登録されている(曲に出てくる)音符をリストにする
    all_notes = list(chain.keys())

    # 初期音設定
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
                # 遷移先がない場合は全体からランダムに選択
                current_note = random.choice(all_notes)

        melody.append(measure)  # 小節を追加

    return melody

# メロディを保存
def save_melody(melody, filename="generated_melody.txt"):
    with open(filename, 'w', encoding='utf-8') as f:
        for measure in melody:
            f.write(' '.join(measure) + '\n')  # 小節ごとに改行して保存

if __name__ == "__main__":
    melody_data = load_melody(FILE_NAME)

    markov_chain = build_markov_chain(melody_data)

    # 新しいメロディを生成（8小節、4音符）
    generated_melody = generate_melody(markov_chain, measures=8, notes_per_measure=4)

    save_melody(generated_melody)
