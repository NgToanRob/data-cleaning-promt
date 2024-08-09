import re
import asyncio
import aiofiles
from tqdm.asyncio import tqdm

from fasttext_detect_language import detect_language

def is_alpha_line(line, threshold=0.3):
    line = line.strip()
    if not line:
        return False
    total_chars = len(line)
    alpha_chars = len(re.findall(r'[A-Za-zÁÉÍÓÖŐÚÜŰáéíóöőúüűА-яЁё]', line))
    return (alpha_chars / total_chars) >= threshold


async def filter_by_alpha(input_file):
    indices = []
    lines_to_keep = []
    
    async with aiofiles.open(input_file, 'r', encoding='utf-8') as afp:
        # count total lines in file to set up progress bar
        total_lines = sum(1 for _ in await afp.readlines())
        await afp.seek(0)  # go back to the beginning of the file to start reading
        
        i = 0
        async for line in tqdm(afp, total=total_lines, desc=f"Processing {input_file}"):
            line = line.strip()
            if is_alpha_line(line):
                indices.append(i)
                lines_to_keep.append(line)
            i += 1
    
    return indices, lines_to_keep


async def filter_by_language(input_file, target_lang):
    indices = []
    lines_to_keep = []
    
    async with aiofiles.open(input_file, 'r', encoding='utf-8') as afp:
        # Count total lines in file to set up progress bar
        total_lines = sum(1 for _ in await afp.readlines())
        await afp.seek(0)  # Go back to the beginning of the file to start reading
        
        i = 0
        async for line in tqdm(afp, total=total_lines, desc=f"Processing {input_file}"):
            line = line.strip()
            detected_lang = detect_language(line)
            if detected_lang == target_lang:
                indices.append(i)
                lines_to_keep.append(line)
            i += 1
    
    return indices, lines_to_keep

# Merge indices
def merge_indices(indices1, indices2):
    return sorted(set(indices1) & set(indices2))

# Save filtered lines
async def save_filtered_lines(indices, lines, output_file):
    async with aiofiles.open(output_file, 'w', encoding='utf-8') as afp:
        for i in tqdm(indices, desc=f"Saving {output_file}"):
            try:
                await afp.write(lines[i] + "\n")
            except IndexError:
                print(f"Index {i} out of range")
                break

async def main():
    # input file paths
    input_file_hu = 'hu-ru.txt\MultiParaCrawl.hu-ru.hu'
    input_file_ru = 'hu-ru.txt\MultiParaCrawl.hu-ru.ru'
    
    # filter lines based on alphabetic characters
    indices_hu, lines_hu = await filter_by_alpha(input_file_hu)
    indices_ru, lines_ru = await filter_by_alpha(input_file_ru)
    
    # Merge các index
    merged_indices = merge_indices(indices_hu, indices_ru)
    
    # Save filtered lines
    await save_filtered_lines(merged_indices, lines_hu, 'output_alpha.hu')
    await save_filtered_lines(merged_indices, lines_ru, 'output_alpha.ru')

    # input file paths
    input_file_hu = 'output_alpha.hu'
    input_file_ru = 'output_alpha.ru'
    
    # filter lines based on language
    filtered_indices_hu, filtered_lines_hu = await filter_by_language(input_file_hu, 'hu')
    filtered_indices_ru, filtered_lines_ru = await filter_by_language(input_file_ru, 'ru')
    
    # Merge các index
    merged_indices = merge_indices(filtered_indices_hu, filtered_indices_ru)

    # Save filtered lines
    await save_filtered_lines(merged_indices, filtered_lines_hu, 'final_output.hu')
    await save_filtered_lines(merged_indices, filtered_lines_ru, 'final_output.ru')

if __name__ == "__main__":
    asyncio.run(main()) 