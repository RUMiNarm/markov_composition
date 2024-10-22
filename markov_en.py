import random
from collections import defaultdict

# テキストファイルからメロディを読み込む関数
def load_melody(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return [line.strip().split() for line in f.readlines()]

# マルコフ連鎖用の遷移辞書を作成する関数
def build_markov_chain(melody_data):
    chain = defaultdict(lambda: defaultdict(int))
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

# マルコフ連鎖に基づき新しいメロディを生成する関数
def generate_melody(chain, length=16):
    melody = []
    current_note = random.choice(list(chain.keys()))
    
    for _ in range(length):
        melody.append(current_note)
        
        # 現在の音符に対する次の音符を取得
        next_notes = list(chain[current_note].keys())
        probabilities = list(chain[current_note].values())
        
        if not next_notes:  # 遷移先がない場合
            break  # 生成を終了
            
        current_note = random.choices(next_notes, probabilities)[0]
    
    return melody

# メロディをテキスト形式で保存する関数
def save_melody(melody, filename="generated_melody.txt"):
    with open(filename, 'w', encoding='utf-8') as f:
        for i, note in enumerate(melody):
            f.write(note + ('\n' if (i + 1) % 4 == 0 else ' '))

# メイン処理
if __name__ == "__main__":
    # 入力ファイルの読み込み
    melody_data = load_melody("input_melody2.txt")
    
    # マルコフ連鎖の遷移辞書を作成
    markov_chain = build_markov_chain(melody_data)
    
    # 新しいメロディを生成
    generated_melody = generate_melody(markov_chain, length=32)
    
    # 生成したメロディを保存
    save_melody(generated_melody)
    print("メロディが 'generated_melody.txt' に保存されました。")
