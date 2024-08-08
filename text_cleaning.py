import re
import asyncio
import aiofiles
from tqdm.asyncio import tqdm

from detect_language import detect_language

def is_alpha_line(line, threshold=0.3):
    line = line.strip()  # Xóa khoảng trắng ở đầu và cuối dòng
    if not line:  # Loại bỏ các dòng rỗng hoặc chỉ có khoảng trắng
        return False
    total_chars = len(line)
    alpha_chars = len(re.findall(r'[A-Za-zÁÉÍÓÖŐÚÜŰáéíóöőúüűА-яЁё]', line))
    return (alpha_chars / total_chars) >= threshold

# Hàm xử lý từng dòng bất đồng bộ và lấy các index của các dòng cần giữ
async def filter_by_alpha(input_file):
    indices = []
    lines_to_keep = []
    
    async with aiofiles.open(input_file, 'r', encoding='utf-8') as afp:
        # Đếm tổng số dòng trong file để thiết lập thanh tiến trình
        total_lines = sum(1 for _ in await afp.readlines())
        await afp.seek(0)  # Quay lại đầu file để bắt đầu đọc
        
        i = 0
        async for line in tqdm(afp, total=total_lines, desc=f"Processing {input_file}"):
            line = line.strip()
            if is_alpha_line(line):
                indices.append(i)
                lines_to_keep.append(line)
            i += 1
    
    return indices, lines_to_keep

# Hàm xử lý từng dòng bất đồng bộ và kiểm tra ngôn ngữ, trả về các index và các dòng cần giữ
async def filter_by_language(input_file, target_lang):
    indices = []
    lines_to_keep = []
    
    async with aiofiles.open(input_file, 'r', encoding='utf-8') as afp:
        # Đếm tổng số dòng trong file để thiết lập thanh tiến trình
        total_lines = sum(1 for _ in await afp.readlines())
        await afp.seek(0)  # Quay lại đầu file để bắt đầu đọc
        
        i = 0
        async for line in tqdm(afp, total=total_lines, desc=f"Processing {input_file}"):
            line = line.strip()
            detected_lang = detect_language(line)
            if detected_lang == target_lang:
                indices.append(i)
                lines_to_keep.append(line)
            i += 1
    
    return indices, lines_to_keep

# Hàm merge các index của hai file
def merge_indices(indices1, indices2):
    return sorted(set(indices1) & set(indices2))

# Hàm lưu các dòng đã lọc vào file mới
async def save_filtered_lines(indices, lines, output_file):
    async with aiofiles.open(output_file, 'w', encoding='utf-8') as afp:
        for i in tqdm(indices, desc=f"Saving {output_file}"):
            try:
                await afp.write(lines[i] + "\n")
            except IndexError:
                print(f"Index {i} out of range")
                break

# Hàm chính
async def main():
    # # Đường dẫn tới file đầu vào
    # input_file_hu = 'hu-ru.txt\MultiParaCrawl.hu-ru.hu'
    # input_file_ru = 'hu-ru.txt\MultiParaCrawl.hu-ru.ru'
    
    # Lọc các dòng từ file Hungary và Russian
    # indices_hu, lines_hu = await filter_by_alpha(input_file_hu)
    # indices_ru, lines_ru = await filter_by_alpha(input_file_ru)
    
    # # Merge các index
    # merged_indices = merge_indices(indices_hu, indices_ru)
    
    # # Lưu các dòng đã lọc vào file mới
    # await save_filtered_lines(merged_indices, lines_hu, 'output_alpha.hu')
    # await save_filtered_lines(merged_indices, lines_ru, 'output_alpha.ru')

    # Đường dẫn tới file đầu vào
    input_file_hu = 'output.hu'
    input_file_ru = 'output.ru'
    
    # Lọc các dòng dựa trên ngôn ngữ
    filtered_indices_hu, filtered_lines_hu = await filter_by_language(input_file_hu, 'hu')
    filtered_indices_ru, filtered_lines_ru = await filter_by_language(input_file_ru, 'ru')
    
    # Lưu các dòng đã lọc ngôn ngữ vào file
    await save_filtered_lines(filtered_indices_hu, filtered_lines_hu, 'final_output.hu')
    await save_filtered_lines(filtered_indices_ru, filtered_lines_ru, 'final_output.ru')

# Chạy chương trình
asyncio.run(main())
