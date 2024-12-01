import json

import matplotlib.pyplot as plt
import numpy as np


def load_json(file_name):
    """
    JSONファイルを読み込む
    """
    with open(file_name, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


def plot_transition_probabilities(data):
    """
    遷移確率をグラフ化する
    """
    for prefix, transitions in data.items():
        # キー（次の音符）と値（確率）を分割
        next_notes = list(transitions.keys())
        probabilities = list(transitions.values())

        # グラフをプロット
        x = np.arange(len(next_notes))  # x軸のインデックス
        plt.bar(x, probabilities, tick_label=next_notes)

        # グラフの装飾
        plt.title(f"Transition Probabilities for '{prefix}'")
        plt.xlabel("あいうえお")
        plt.ylabel("Probability")
        plt.ylim(0, 1)  # 確率は0～1の範囲
        plt.xticks(rotation=45)

        # 表示
        plt.tight_layout()
        plt.show()


def main():
    file_name = input("JSONファイル名： ")

    # JSONファイルを読み込む
    data = load_json(file_name)

    # 遷移確率をグラフ化
    plot_transition_probabilities(data)


if __name__ == "__main__":
    main()
