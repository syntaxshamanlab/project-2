#!/usr/bin/env python3
"""
Auto-ingest new files from /notebooklm-import-raw/ into the database.
Updates processed records, index.json, and relations.json automatically.
"""

import os
import json
import re
from datetime import datetime
from pathlib import Path

# Configuration
IMPORT_DIR = Path("/workspaces/project-2/notebooklm-import-raw")
DB_DIR = Path("/workspaces/project-2/database")
PROCESSED_DIR = DB_DIR / "processed"
RAW_DIR = DB_DIR / "raw"
IMPORT_ARCHIVE_DIR = DB_DIR / "imports" / "notebooklm"
INDEX_FILE = DB_DIR / "indexed" / "index.json"
RELATIONS_FILE = DB_DIR / "indexed" / "relations.json"

# Metadata schema
METADATA_TEMPLATE = """---
id: {id}
source: notebooklm
title: {title}
category: {category}
tags: {tags}
created: {date}
updated: {date}
summary: {summary}
---

"""

def get_processed_ids():
    """Get all processed file IDs from index.json"""
    if INDEX_FILE.exists():
        with open(INDEX_FILE, 'r') as f:
            index = json.load(f)
            return {entry['id'] for entry in index}
    return set()

def get_next_id():
    """Generate next ID in sequence nb-YYYYMMDD-###"""
    processed_ids = get_processed_ids()
    
    if not processed_ids:
        return "nb-20260105-001"
    
    # Extract the largest number from existing IDs for today's date
    today = datetime.now().strftime("%Y%m%d")
    today_ids = [id for id in processed_ids if f"nb-{today}" in id]
    
    if not today_ids:
        return f"nb-{today}-001"
    
    # Get the highest number
    numbers = [int(id.split('-')[-1]) for id in today_ids]
    next_num = max(numbers) + 1
    return f"nb-{today}-{next_num:03d}"

def extract_title_from_filename(filename):
    """Extract clean title from filename"""
    # Remove file extension
    title = filename.rsplit('.', 1)[0]
    # Replace underscores with spaces
    title = title.replace('_', ' ')
    return title

def categorize_content(filename, content_preview):
    """Auto-categorize based on filename and content"""
    filename_lower = filename.lower()
    
    if 'doctrine' in filename_lower:
        return 'doctrine'
    elif 'forensic' in filename_lower:
        return 'forensic-analysis'
    elif 'psychological' in filename_lower or 'warfare' in filename_lower:
        return 'psychological-warfare'
    elif 'playbook' in filename_lower:
        return 'playbook'
    elif 'infiltrator' in filename_lower:
        return 'tactical-strategy'
    elif 'social' in filename_lower and 'test' in filename_lower:
        return 'social-test'
    elif 'classroom' in filename_lower:
        return 'pedagogy'
    elif 'unseen' in filename_lower and 'war' in filename_lower:
        return 'strategic-brief'
    elif 'game' in filename_lower:
        return 'field-manual'
    elif 'content' in filename_lower and 'index' in filename_lower:
        return 'reference-index'
    else:
        return 'miscellaneous'

def generate_tags(title, category, content_preview):
    """Generate 5-12 tags based on content"""
    tags = [category]
    
    keywords = [
        'psychological-warfare', 'forensic-analysis', 'doctrine', 'humint',
        'manipulation', 'tactical', 'strategic', 'counter-intelligence',
        'narrative', 'identity', 'resilience', 'pedagogy', 'curriculum',
        'counter-offensive', 'psychological-operations', 'non-kinetic-warfare'
    ]
    
    content_lower = (title + ' ' + content_preview).lower()
    for keyword in keywords:
        if keyword.replace('-', ' ') in content_lower and keyword not in tags:
            tags.append(keyword)
            if len(tags) >= 12:
                break
    
    # Ensure we have 5-12 tags
    while len(tags) < 5:
        tags.append('notebooklm')
    
    return tags[:12]

def generate_summary(filename, content_preview):
    """Generate a summary from content preview"""
    # Take first 2-4 sentences from content
    sentences = re.split(r'(?<=[.!?])\s+', content_preview.strip())[:3]
    summary = ' '.join(sentences)
    
    # Truncate to reasonable length
    if len(summary) > 200:
        summary = summary[:197] + '...'
    
    return summary if summary else f"Document: {filename}"

def is_file_already_processed(filename):
    """Check if a file has already been processed by examining index"""
    if not INDEX_FILE.exists():
        return False
    
    try:
        with open(INDEX_FILE, 'r') as f:
            index = json.load(f)
            for entry in index:
                path = entry['path']
                if 'processed/' in path:
                    # Extract filename from path (after the ID prefix)
                    full_filename = path.split('processed/')[-1]
                    # Remove ID prefix (nb-YYYYMMDD-###_)
                    if '_' in full_filename:
                        original_filename = full_filename.split('_', 1)[1]
                        if original_filename == filename:
                            return True
    except:
        pass
    
    return False

def process_new_file(filename):
    """Process a single new file into the database"""
    source_path = IMPORT_DIR / filename
    
    if not source_path.exists():
        return False, f"File not found: {filename}"
    
    # Check if already processed
    if is_file_already_processed(filename):
        return True, f"⊘ Already processed: {filename}"
    
    try:
        # Read file content
        with open(source_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Generate metadata
        title = extract_title_from_filename(filename)
        content_preview = content[:500]
        category = categorize_content(filename, content_preview)
        tags = generate_tags(title, category, content_preview)
        summary = generate_summary(filename, content_preview)
        
        # Generate next ID
        record_id = get_next_id()
        date_str = datetime.now().strftime("%Y-%m-%d")
        
        # Create processed record
        metadata = METADATA_TEMPLATE.format(
            id=record_id,
            title=title,
            category=category,
            tags=json.dumps(tags),
            date=date_str,
            summary=summary
        )
        
        processed_content = metadata + content
        
        # Write processed file
        processed_filename = f"{record_id}_{filename}"
        processed_path = PROCESSED_DIR / processed_filename
        with open(processed_path, 'w', encoding='utf-8') as f:
            f.write(processed_content)
        
        # Write raw copy
        raw_path = RAW_DIR / filename
        with open(raw_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Write import archive copy
        import_path = IMPORT_ARCHIVE_DIR / filename
        with open(import_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Update index.json
        index_entry = {
            "id": record_id,
            "title": title,
            "category": category,
            "tags": tags,
            "path": f"database/processed/{processed_filename}",
            "summary": summary
        }
        
        if INDEX_FILE.exists():
            with open(INDEX_FILE, 'r') as f:
                index = json.load(f)
        else:
            index = []
        
        index.append(index_entry)
        
        with open(INDEX_FILE, 'w') as f:
            json.dump(index, f, indent=2)
        
        # Update relations.json
        relations = []
        if RELATIONS_FILE.exists():
            with open(RELATIONS_FILE, 'r') as f:
                relations = json.load(f)
        
        # Add category as concept
        category_entry = {
            "concept": category,
            "appears_in": [record_id],
            "related_terms": tags
        }
        relations.append(category_entry)
        
        with open(RELATIONS_FILE, 'w') as f:
            json.dump(relations, f, indent=2)
        
        return True, f"✓ Processed: {record_id} ({title})"
    
    except Exception as e:
        return False, f"✗ Error processing {filename}: {str(e)}"

def main():
    """Main entry point"""
    if not IMPORT_DIR.exists():
        print(f"Error: Import directory not found: {IMPORT_DIR}")
        return
    
    # Get all files in import directory
    import_files = [f.name for f in IMPORT_DIR.iterdir() if f.is_file()]
    
    # Find new files (check against index)
    new_files = [f for f in import_files if not is_file_already_processed(f)]
    
    if not new_files:
        print("✓ No new files to process.")
        return
    
    print(f"Found {len(new_files)} new file(s) to process:\n")
    
    for filename in new_files:
        success, message = process_new_file(filename)
        print(f"  {message}")
    
    print(f"\n✓ Processing complete!")

if __name__ == "__main__":
    main()
