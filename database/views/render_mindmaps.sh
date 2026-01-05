#!/bin/bash

# Check if mermaid-cli is installed
if ! command -v mmdc &> /dev/null; then
    echo "Mermaid CLI (mmdc) could not be found."
    echo "Please install it using: npm install -g @mermaid-js/mermaid-cli"
    exit 1
fi

# Render mind maps to SVG
echo "Rendering mind maps to SVG..."
mmdc -i database/views/mindmap_people_relationships.mermaid -o database/views/mindmap_people_relationships.svg
mmdc -i database/views/mindmap_concepts_frameworks.mermaid -o database/views/mindmap_concepts_frameworks.svg
mmdc -i database/views/mindmap_people_concepts_integration.mermaid -o database/views/mindmap_people_concepts_integration.svg
echo "Done."