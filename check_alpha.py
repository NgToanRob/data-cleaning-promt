import re

def is_alpha_line(line, threshold=0.3):
    total_chars = len(line)
    if total_chars == 0:
        return False
    # Kết hợp các ký tự bảng chữ cái của cả tiếng Hungary và tiếng Nga
    alpha_chars = len(re.findall(r'[A-Za-zÁÉÍÓÖŐÚÜŰáéíóöőúüűА-яЁё]', line))
    return (alpha_chars / total_chars) >= threshold

def test():
    line_ru = "Но на деле наш вклад значительно больше: мы предлагаем оптимальную систему опалубки вместе с техническим решением."
    line_hu= "Lényegében azonban még többet adunk: a megfelelő zsaluzati rendszert, mint megoldást. "
    blank = ""
    print(is_alpha_line(line_ru, 0.3))
    print(is_alpha_line(line_hu, 0.3))
    print(is_alpha_line(blank, 0.3))

if __name__ == "__main__":
    test()