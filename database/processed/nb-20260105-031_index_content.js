---
id: nb-20260105-031
source: notebooklm
title: index content
category: reference-index
tags: ["reference-index", "notebooklm", "notebooklm", "notebooklm", "notebooklm"]
created: 2026-01-05
updated: 2026-01-05
summary: const fs = require('fs');
const path = require('path');

const directory = 'notebooklm-import-raw';
const files = fs.readdirSync(directory).filter(f => f.endsWith('.txt') && f !== 'index.txt' && f ...
---

const fs = require('fs');
const path = require('path');

const directory = 'notebooklm-import-raw';
const files = fs.readdirSync(directory).filter(f => f.endsWith('.txt') && f !== 'index.txt' && f !== 'index_content.js');

let index = '';

for (const file of files) {
    const filePath = path.join(directory, file);
    const content = fs.readFileSync(filePath, 'utf8');
    const lines = content.split('\n');
    const title = lines[0].trim() || file;
    let summary = '';
    if (content.includes('Abstract')) {
        const start = content.indexOf('Abstract');
        const end = content.indexOf('\n\n', start);
        summary = content.substring(start, end !== -1 ? end : start + 1000);
    } else if (content.includes('Introduction')) {
        const start = content.indexOf('Introduction');
        const end = content.indexOf('\n\n', start);
        summary = content.substring(start, end !== -1 ? end : start + 1000);
    } else {
        summary = lines.slice(1, 10).join(' ').substring(0, 1000);
    }
    index += `File: ${file}\nTitle: ${title}\nSummary: ${summary.trim()}\n\n`;
}

fs.writeFileSync(path.join(directory, 'content_index.txt'), index);
