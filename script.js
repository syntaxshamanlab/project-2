// Load and display content when page loads
document.addEventListener('DOMContentLoaded', function() {
    loadContentIndex();
});

// Function to load and parse content index
async function loadContentIndex() {
    try {
        const response = await fetch('notebooklm-import-raw/content_index.txt');
        if (!response.ok) {
            throw new Error('Failed to load content index');
        }
        const text = await response.text();
        const documents = parseContentIndex(text);
        displayDocuments(documents);
    } catch (error) {
        console.error('Error loading content:', error);
        document.getElementById('content-list').innerHTML = '<p>Error loading content. Please check the console for details.</p>';
    }
}

// Parse the content index text into document objects
function parseContentIndex(text) {
    const documents = [];
    const entries = text.split('\n\n');

    for (const entry of entries) {
        const lines = entry.trim().split('\n');
        if (lines.length >= 3) {
            const fileMatch = lines[0].match(/File: (.+)/);
            const titleMatch = lines[1].match(/Title: (.+)/);
            const summaryMatch = lines[2].match(/Summary: (.+)/);

            if (fileMatch && titleMatch && summaryMatch) {
                documents.push({
                    file: fileMatch[1],
                    title: titleMatch[1],
                    summary: summaryMatch[1]
                });
            }
        }
    }

    return documents;
}

// Display documents in the content list
function displayDocuments(documents) {
    const contentList = document.getElementById('content-list');

    documents.forEach((doc, index) => {
        const docElement = createDocumentElement(doc, index);
        contentList.appendChild(docElement);
    });
}

// Create HTML element for a document
function createDocumentElement(doc, index) {
    const div = document.createElement('div');
    div.className = 'document-item';

    div.innerHTML = `
        <div class="document-title">${doc.title}</div>
        <div class="document-summary">${doc.summary}</div>
        <button class="toggle-content" data-file="${doc.file}" data-index="${index}">
            Read Full Document
        </button>
        <div class="document-full-content" id="content-${index}">
            <div class="loading">Loading...</div>
        </div>
    `;

    // Add event listener to toggle button
    const toggleBtn = div.querySelector('.toggle-content');
    const contentDiv = div.querySelector('.document-full-content');

    toggleBtn.addEventListener('click', function() {
        if (contentDiv.style.display === 'block') {
            contentDiv.style.display = 'none';
            toggleBtn.textContent = 'Read Full Document';
        } else {
            loadFullContent(doc.file, contentDiv, toggleBtn);
        }
    });

    return div;
}

// Load full content of a document
async function loadFullContent(fileName, contentDiv, toggleBtn) {
    try {
        const response = await fetch(`notebooklm-import-raw/${fileName}`);
        if (!response.ok) {
            throw new Error(`Failed to load ${fileName}`);
        }
        const text = await response.text();

        contentDiv.innerHTML = text;
        contentDiv.style.display = 'block';
        toggleBtn.textContent = 'Hide Document';
    } catch (error) {
        console.error('Error loading document:', error);
        contentDiv.innerHTML = '<p>Error loading document content.</p>';
        contentDiv.style.display = 'block';
    }
}