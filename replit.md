# Shroomy Sticker Editor - Replit Setup

## Project Overview
A single-page web application for adding stickers and emoji to photos, with full editing capabilities and high-resolution export. This is a static HTML/CSS/JavaScript application using React, Konva.js, and React-Konva loaded from CDNs.

## Last Updated
October 27, 2025 - Initial Replit setup

## Recent Changes
- Updated sticker configuration to use actual PNG files from stickers folder (24 sticker images)
- Created Python HTTP server with no-cache headers for proper development
- Configured workflow to serve on port 5000
- Added .gitignore for Python and Replit files

## Project Architecture

### Tech Stack
- **Frontend**: Vanilla HTML with embedded React 18 (via CDN)
- **Canvas Library**: Konva.js v9 + React-Konva v18
- **Styling**: Inline CSS with hand-drawn/sketchy aesthetic
- **Build Process**: None - completely static, runs in browser
- **Server**: Python 3.11 SimpleHTTPServer (development only)

### File Structure
```
/
├── index.html              # Main application (single-page React app)
├── shroomy-editor.html     # Alternative entry point (same app)
├── sticker-reference.html  # Sticker guide/reference
├── stickers/               # PNG sticker images (3.png - 26.png, image.png)
├── server.py               # Python HTTP server with cache control
├── README.md               # User documentation
├── QUICKSTART.md           # Quick start guide
├── TECHNICAL.md            # Technical documentation
├── PROJECT-SUMMARY.md      # Project summary
├── DEPLOYMENT.md           # Deployment guide
└── replit.md               # This file
```

### Key Features
- Photo upload (drag & drop, up to 10MB)
- 24 default PNG stickers + emoji stickers + custom sticker upload
- Transform controls: move, resize, rotate, opacity, flip
- Layer management (forward/backward, front/back)
- Undo/Redo (20-step history)
- High-resolution export (preserves original photo resolution)
- Visual guides (grid, center alignment)
- Touch support for mobile
- Responsive design

## Development Setup

### Running the Application
1. The application runs automatically via the configured workflow
2. Server runs on port 5000 (required for Replit)
3. Access via the webview preview

### Server Configuration
- **Host**: 0.0.0.0 (allows Replit proxy)
- **Port**: 5000 (only port exposed by Replit)
- **Cache Control**: Disabled (no-cache headers for development)

### Making Changes
1. Edit `index.html` for application logic/UI changes
2. Server auto-reloads are not enabled - manually refresh browser
3. Stickers are in `stickers/` folder - update `STICKER_FILES` array in index.html

## Sticker Configuration
The app uses actual PNG files from the stickers folder. To add/remove stickers:
1. Add PNG files to `stickers/` folder
2. Update `STICKER_FILES` array in `index.html` (around line 360)
3. Refresh the browser

Current stickers: 3-26.png (excluding 10.png), image.png, plus emoji fallbacks

## Deployment

### Deployment Type
- **Target**: Static hosting (Autoscale recommended)
- **Build**: None required
- **Run**: HTTP server to serve static files

### Publishing
When ready to publish, the app should be configured as:
- **Deployment Target**: Autoscale (static website)
- **No build step needed** (all assets are static)
- **Serve index.html as entry point**

## User Preferences
None specified yet.

## Notes
- All processing happens client-side (no backend needed for core functionality)
- No database required
- No environment variables needed
- Assets loaded from CDNs (React, Konva.js)
- Works offline after initial load
