import matplotlib.font_manager as fm

# 使用可能なフォントを表示
for font in fm.findSystemFonts(fontpaths=None, fontext="ttf"):
    print(font)
