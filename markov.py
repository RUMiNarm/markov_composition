import json
import random


# JSONデータを読み込む
def load_data(file_name):
    with open(file_name, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


# 適切な開始音符をランダムに選択
def select_random_start(data):
    probabilities = data["transition_probabilities"]
    valid_start_notes = [
        key
        for key in probabilities.keys()
        if all(note in "ドレミファソラシ" for note in eval(key))
    ]
    if not valid_start_notes:
        raise ValueError("適切な開始音符がありません。")
    return random.choice(valid_start_notes)


# メロディを生成
def generate_music(data, length=50):
    probabilities = data["transition_probabilities"]
    current_note = select_random_start(data)
    music = [note for note in eval(current_note)]  # 初期状態をリストに変換

    for _ in range(length - len(music)):
        if current_note in probabilities:
            next_notes = probabilities[current_note]
            next_note = random.choices(
                list(next_notes.keys()), weights=next_notes.values()
            )[0]
            music.append(next_note)
            current_note = str(tuple(music[-3:]))  # 次の遷移元を更新
        else:
            # 遷移がない場合、再びランダムな開始音符を選択
            current_note = select_random_start(data)
            music.extend(eval(current_note))

    return music[:length]


def main():
    file_name = "chain.json"  # JSONデータファイル
    length = 50  # 生成する音符の数

    # JSONデータを読み込む
    data = load_data(file_name)

    # マルコフ連鎖で音楽を生成
    generated_music = generate_music(data, length)
    print("生成された音楽:")
    print(" ".join(generated_music))


if __name__ == "__main__":
    main()
