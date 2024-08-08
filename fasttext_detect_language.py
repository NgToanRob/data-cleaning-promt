from ftlangdetect import detect_langs

# Hàm nhận diện ngôn ngữ của một dòng
def detect_language(line):
    try:
        result = detect_langs(line)
        if result:
            # Trả về ngôn ngữ có xác suất cao nhất
            return result[0]['lang']
        return None
    except Exception:
        return None

# Hàm lọc các dòng dựa trên ngôn ngữ
async def filter_by_language(lines, target_lang):
    filtered_indices = []
    filtered_lines = []
    
    for i, line in enumerate(lines):
        lang = detect_language(line)
        if lang == target_lang:
            filtered_indices.append(i)
            filtered_lines.append(line)
    
    return filtered_indices, filtered_lines