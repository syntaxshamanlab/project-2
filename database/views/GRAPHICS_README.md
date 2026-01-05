# Forensic Mind Maps - Graphics & Visualization

This directory contains the visualization layer for the forensic mind maps.

## 1. Interactive Dashboards (HTML)
Open these files in any web browser to view the rendered mind maps. No installation required.

- **Master Dashboard**: `mindmap_test_dashboard.html` (All maps in one view)
- **People Map**: `mindmap_people_relationships.html`
- **Concepts Map**: `mindmap_concepts_frameworks.html`
- **Integration Map**: `mindmap_people_concepts_integration.html`

## 2. Source Files (Mermaid)
These files contain the diagram definitions.

- `mindmap_people_relationships.mermaid`
- `mindmap_concepts_frameworks.mermaid`
- `mindmap_people_concepts_integration.mermaid`

## 3. Static Image Generation
To generate static SVG images from the source files, use the provided script:

```bash
../../scripts/render_mindmaps.sh
```

*Requires `npm` and `@mermaid-js/mermaid-cli`.*