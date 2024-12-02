import json
import random


# JSONデータを読み込む
def load_data(file_name):
    with open(file_name, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


def generate_music(data, start_note, length=50):
    probabilities = data["transition_probabilities"]
    current_note = start_note
    music = [current_note.strip("()").replace("'", "").replace(",", "")]

    for _ in range(length - 1):
        if current_note in probabilities:
            next_notes = probabilities[current_note]
            next_note = random.choices(
                list(next_notes.keys()), weights=next_notes.values()
            )[0]
            music.append(next_note)
            current_note = f"('{next_note}',)"  # 次の状態に遷移
        else:
            # 遷移がない場合、ランダムに開始音符を選び直す
            current_note = random.choice(list(probabilities.keys()))
            music.append(current_note.strip("()").replace("'", "").replace(",", ""))

    return music


def main():
    file_name = "chain.json"  # JSONデータファイル
    start_note = "('ソ',)"  # 初期音符（例: "('ソ',)"）
    length = 50  # 生成する音符の数

    # JSONデータを読み込む
    data = load_data(file_name)

    # マルコフ連鎖で音楽を生成
    generated_music = generate_music(data, start_note, length)
    print("生成された音楽:")
    print(" ".join(generated_music))


if __name__ == "__main__":
    main()
