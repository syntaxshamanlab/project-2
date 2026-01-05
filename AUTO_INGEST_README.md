# Auto-Ingest System

Automatically ingest new files from `/notebooklm-import-raw/` into the database with metadata, indexing, and relation mapping.

## How It Works

The auto-ingest system:
1. **Detects** new files in `/notebooklm-import-raw/`
2. **Validates** they haven't been processed yet
3. **Processes** each file with automatic metadata generation
4. **Creates** three copies (processed, raw, import-archive)
5. **Updates** index.json and relations.json
6. **Logs** all actions for verification

## VS Code Tasks

Three tasks are available in VS Code:

### 1. Manual Ingest Check (Default - Ctrl+Shift+B)
- Runs once to check for new files
- Best for: Quick checks after adding new files
- Command: `python3 auto-ingest.py`

### 2. Auto-Ingest New NotebookLM Files
- Single run task
- Best for: One-time processing
- From VS Code: Tasks > Run Task > "Auto-Ingest New NotebookLM Files"

### 3. Watch for New Files (Auto-Ingest Every 30s)
- Continuous monitoring background task
- Checks every 30 seconds for new files
- Best for: Long-term development with frequent file additions
- From VS Code: Tasks > Run Task > "Watch for New Files (Auto-Ingest Every 30s)"

## Manual Command Line Usage

```bash
# Single check
python3 /workspaces/project-2/auto-ingest.py

# Continuous monitoring (every 30 seconds)
while true; do python3 /workspaces/project-2/auto-ingest.py && sleep 30; done
```

## What Gets Automated

For each new file:

### Metadata Generation
- **ID**: Auto-generated (nb-YYYYMMDD-###)
- **Title**: Extracted from filename
- **Category**: Auto-categorized based on content
- **Tags**: Generated from content (5-12 tags)
- **Summary**: First 2-4 sentences of content
- **Dates**: Creation and update timestamps

### File Copies Created
1. **Processed** (`database/processed/`) — With metadata header
2. **Raw** (`database/raw/`) — Original content
3. **Import Archive** (`database/imports/notebooklm/`) — Audit trail

### Indexes Updated
- **index.json** — New entry with all metadata
- **relations.json** — Concept mapping for new file

## Example Workflow

```
1. Add new file to /notebooklm-import-raw/
   Example: "My New Document.txt"

2. Run auto-ingest task
   (Ctrl+Shift+B or Tasks menu)

3. Script processes file:
   ✓ Processed: nb-20260105-099 (My New Document)
   ✓ Processing complete!

4. Verify in database:
   - database/processed/nb-20260105-099_My New Document.txt (with metadata)
   - database/raw/My New Document.txt (original)
   - database/imports/notebooklm/My New Document.txt (copy)
   - index.json (updated entry)
   - relations.json (updated concepts)
```

## Deduplication

The system automatically prevents duplicate processing:
- Checks if file already exists in index
- Skips already-processed files with message: "⊘ Already processed: filename"
- Safe for multiple runs on same file set

## Customization

Edit `auto-ingest.py` to:
- Change auto-categorization rules (see `categorize_content()`)
- Modify tag generation (see `generate_tags()`)
- Adjust summary extraction (see `generate_summary()`)
- Change directory paths at top of script

## Troubleshooting

**"File not found" error**
- Verify file exists in `/notebooklm-import-raw/`
- Check filename spelling

**"Error processing file" message**
- Check file encoding (should be UTF-8)
- Verify file isn't corrupted
- Check disk space

**Script won't run**
- Verify Python 3 is installed: `python3 --version`
- Check script is executable: `chmod +x auto-ingest.py`
- Verify database directories exist

## Integration Points

Auto-ingest integrates with:
- `database/indexed/index.json` — Main document index
- `database/indexed/relations.json` — Concept relationships
- `database/processed/` — Final processed records
- `database/raw/` — Original file preservation
- `database/imports/notebooklm/` — Import archive

---

**Status**: ✓ Active and Ready
**Next File ID**: Check script output or latest in index.json
**Last Run**: See terminal output
