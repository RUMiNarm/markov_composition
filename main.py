import random
from collections import defaultdict

FILE_NAME = "input_melody.txt" # メロディのファイル名
MEASURE_SPLIT = '\n'
NOTE_SPLIT = ' '

# 生成したい曲の長さの設定
gen_measures = 8 # 小節数
gen_notes_per_measure = 4 # 1小節あたりの音符数


# メロディを読み込み
def load_melody(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        # 空白で分けてリスト型でいれる。改行で列が変わる(小節)。
        return [line.strip().split() for line in f.readlines()] 


# 遷移辞書を作成
def build_markov_chain_by_position(melody_data):
    chains = {
        'start': defaultdict(lambda: defaultdict(int)),
        'middle': defaultdict(lambda: defaultdict(int)),
        'end': defaultdict(lambda: defaultdict(int)),
    }

    for measure in melody_data:
        if len(measure) < 2:
            continue  # 音符が少なすぎる小節はスキップ

        # 小節の最初の音符 -> 2つ目の音符
        chains['start'][measure[0]][measure[1]] += 1

        # 小節の途中の音符遷移
        for i in range(1, len(measure) - 1):
            chains['middle'][measure[i]][measure[i + 1]] += 1

        # 小節の最後の音符
        chains['end'][measure[-2]][measure[-1]] += 1

    # 確率を計算
    for chain in chains.values():
        for current, transitions in chain.items():
            total = sum(transitions.values())
            for next_note in transitions:
                transitions[next_note] /= total

    return chains


# 遷移確率から新しいメロディを生成
def generate_melody_with_position(chain, measures, notes_per_measure):
    melody = []
    all_notes = list(chain['middle'].keys())  # 全体の音符リスト

    for _ in range(measures):
        measure = []

        # 小節の最初の音符
        current_note = random.choice(all_notes)
        measure.append(current_note)

        for i in range(1, notes_per_measure):
            if i == notes_per_measure - 1:
                # 小節の最後の音符
                next_chain = chain['end']
            else:
                # 小節の途中の音符
                next_chain = chain['middle']

            # 次の音符を選択
            next_notes = list(next_chain[current_note].keys())
            probabilities = list(next_chain[current_note].values())

            if next_notes:
                current_note = random.choices(next_notes, probabilities)[0]
            else:
                current_note = random.choice(all_notes)

            measure.append(current_note)

        melody.append(measure)

    return melody


# メロディを保存
def save_melody(melody, filename="generated_melody.txt"):
    with open(filename, 'w', encoding='utf-8') as f:
        for measure in melody:
            f.write(NOTE_SPLIT.join(measure) + MEASURE_SPLIT)  # 小節ごとに改行して保存

if __name__ == "__main__":
    melody_data = load_melody(FILE_NAME)

    markov_chain = build_markov_chain_by_position(melody_data)

    with open("markov_chain.txt", 'w', encoding='utf-8') as f:
        f.writelines("\n".join(str(k)+","+str(v) for k,v in markov_chain.items()))

    # 新しいメロディを生成（遷移辞書、生成する小節数、生成する一小節あたりの音符数）
    generated_melody = generate_melody_with_position(markov_chain, gen_measures, gen_notes_per_measure)

    save_melody(generated_melody)
