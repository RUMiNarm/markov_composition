import markovify
import MeCab

# Load file
# text_file = open("input.txt", "r",encoding="utf-8")
# text = text_file.read()
text = "ド ド ド ソ ソ ラ ラ ソ\nファ ファ ミ ミ レ レ ド\nソ ソ ファ ファ ミ ミ レ\nソ ソ ファ ファ ミ ミ レ\nド ド ソ ソ ラ ラ ソ\nファ ファ ミ ミ レ レ ド\n"

# Parse text using MeCab
parsed_text = MeCab.Tagger('-Owakati').parse(text)

# Build model
text_model = markovify.Text(parsed_text, state_size=2)

# Output
for _ in range(10):
    sentence = text_model.make_short_sentence(100, 20, tries=100).replace(' ', '')
    print(sentence)
