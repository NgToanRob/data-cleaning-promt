from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException

# Đảm bảo kết quả của detect lang là nhất quán
DetectorFactory.seed = 0

# Hàm nhận diện ngôn ngữ của một dòng
def detect_language(line):
    try:
        return detect(line)
    except LangDetectException:
        return None