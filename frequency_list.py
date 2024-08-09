from sacremoses import MosesTokenizer
from collections import Counter
from tqdm import tqdm


def tokenize_and_get_frequency(file_path):
    tokenizer = MosesTokenizer(lang='hu')
    frequency_list = Counter()
    
    with open(file_path, 'r', encoding='utf-8') as file:
        total_lines = sum(1 for _ in file)
    
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in tqdm(file, total=total_lines, desc="Processing lines"):
            line = line.strip()
            if line:  # skip empty lines
                # Tokenize each line
                tokens = tokenizer.tokenize(line, return_str=False)
                # Lowercase all tokens
                tokens = [token.lower() for token in tokens]
                # Update frequency list
                frequency_list.update(tokens)
    
    return frequency_list

def main(file_path, output_file):
    # Tokenize and get frequency
    frequency_list = tokenize_and_get_frequency(file_path)
    
    # Save frequency list to file
    with open(output_file, 'w', encoding='utf-8') as f:
        for token, freq in frequency_list.most_common():
            f.write(f"{token}\t{freq}\n")

# path to cleaned file
file_path = 'final_output.hu'
# path to output frequency list
output_file = 'frequency_list.hu'

if __name__ == '__main__':
    main(file_path, output_file)
