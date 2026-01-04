import os
from pathlib import Path

directory = Path('notebooklm-import-raw')
index = []

for file_path in directory.glob('*.txt'):
    if file_path.name == 'index.txt' or file_path.name == 'index_content.py':
        continue
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        lines = content.split('\n')
        # Try to find a title
        title = lines[0].strip() if lines and lines[0].strip() else file_path.name
        # Look for abstract or introduction
        summary = ''
        if 'Abstract' in content:
            start = content.find('Abstract')
            end = content.find('\n\n', start)
            if end == -1:
                end = start + 1000
            summary = content[start:end].strip()
        elif 'Introduction' in content:
            start = content.find('Introduction')
            end = content.find('\n\n', start)
            if end == -1:
                end = start + 1000
            summary = content[start:end].strip()
        else:
            # First few lines
            summary = ' '.join([line.strip() for line in lines[1:10] if line.strip()])[:1000]
        index.append(f"File: {file_path.name}\nTitle: {title}\nSummary: {summary}\n\n")

with open(directory / 'content_index.txt', 'w', encoding='utf-8') as f:
    f.writelines(index)
