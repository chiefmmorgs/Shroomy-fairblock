# 🍄 Shroomy Sticker Editor

A single-page web application for adding stickers and emoji to photos, with full editing capabilities and high-resolution export.

## Features

### Core Functionality
- ✅ **Photo Upload**: Drag & drop or click to upload (JPG, PNG, WEBP, up to 10MB)
- ✅ **Sticker Palette**: 12 default mushroom-themed emoji + custom sticker uploads
- ✅ **Transform Controls**: Move, resize, rotate, adjust opacity, flip horizontal/vertical
- ✅ **Layer Management**: Bring forward/backward, send to front/back
- ✅ **Undo/Redo**: 20-step history for all edits
- ✅ **High-Res Export**: Downloads PNG at original photo resolution with 2x retina quality
- ✅ **Visual Guides**: Optional 8px grid and center alignment guides
- ✅ **Touch Support**: Works on mobile with pinch/zoom gestures via Konva
- ✅ **Responsive Design**: Stacks panels on mobile screens

### Interface Layout

**Left Panel** (Upload & Stickers):
- Photo upload area with drag & drop
- Sticker palette with circular tiles
- Custom sticker upload button
- Grid and guide toggles

**Center Panel** (Canvas):
- Live preview with photo and stickers
- Displays both original and display resolutions
- Interactive canvas with transform handles
- Optional grid overlay (8px spacing)
- Center alignment guides in purple

**Right Panel** (Controls):
- Position controls (X, Y coordinates)
- Size controls (width, height)
- Rotation slider (-180° to 180°)
- Opacity slider (0-100%)
- Flip controls (horizontal/vertical)
- Layer ordering buttons
- Duplicate and delete buttons

**Top Bar**:
- Undo/Redo buttons
- Reset all button
- Download PNG button

## Technical Implementation

### Technologies Used
- **React 18**: Component-based UI
- **Konva.js**: Canvas manipulation and transforms
- **React-Konva**: React bindings for Konva
- **HTML5 Canvas API**: High-resolution export
- **Vanilla CSS**: Hand-drawn/sketchy styling

### Performance Optimizations
- Handles photos up to 6000×6000 pixels
- Preview at display resolution (max 600px)
- Export at original resolution using offscreen rendering
- Image caching for custom stickers
- Efficient re-rendering with React hooks

### Key Design Decisions
1. **Client-side only**: All processing in browser, no server needed
2. **Original resolution preservation**: Display size ≠ export size
3. **Emoji as default stickers**: Universal, no asset dependencies
4. **Konva for transforms**: Professional-grade object manipulation
5. **History management**: Array-based undo/redo system

## Usage Instructions

### Getting Started
1. Open `shroomy-editor.html` in a modern web browser
2. Click the upload area or drag a photo into it
3. Click any sticker in the palette to add it to your photo
4. Select a sticker on the canvas to edit it

### Editing Stickers
**Mouse/Desktop**:
- Click and drag to move
- Use corner handles to resize
- Use rotation handle (top) to rotate
- Use numeric inputs in right panel for precision

**Touch/Mobile**:
- Tap to select
- Drag with one finger to move
- Pinch with two fingers to scale
- Rotate with two fingers to rotate

### Controls Reference
- **Undo/Redo**: Revert or reapply last 20 changes
- **Reset**: Clear all stickers (keeps photo)
- **Download**: Export final composition as PNG
- **Grid**: Show/hide 8px alignment grid
- **Guides**: Show/hide center alignment lines
- **Flip H/V**: Mirror sticker horizontally or vertically
- **Forward/Backward**: Change sticker layer order
- **Duplicate**: Create copy of selected sticker
- **Delete**: Remove selected sticker

### Custom Stickers
1. Click "Upload Custom Sticker" button
2. Select an image file (PNG with transparency recommended)
3. New sticker appears in the palette
4. Click to add to canvas like any other sticker

### Exporting
1. Click "Download PNG" when finished
2. Image exports at **original photo resolution**
3. All stickers are scaled proportionally
4. File saved as `shroomy-creation.png`
5. Supports retina/2x quality for sharp output

## File Structure

```
shroomy-editor.html     # Complete single-page application
README.md               # This documentation
```

## Browser Compatibility

**Fully Supported**:
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

**Requirements**:
- JavaScript enabled
- HTML5 Canvas support
- File API support
- ~50MB available memory for large images

## Customization Guide

### Adding More Default Stickers
Edit the `DEFAULT_STICKERS` array (line ~61):
```javascript
const DEFAULT_STICKERS = ['🍄', '🌟', '✨', '💜', /* add more */];
```

### Changing Colors
Main theme colors defined in CSS:
- Purple accent: `#b577d6`
- Dark purple: `#8b5ca8`
- Background: `#f5e6d3` to `#e8d5c4` gradient
- Borders: `#333`

### Adjusting Canvas Size
Change `maxSize` in `handlePhotoUpload` (line ~119):
```javascript
const maxSize = 600; // Increase for larger preview
```

### Modifying Export Quality
Change `pixelRatio` in `downloadImage` (line ~551):
```javascript
pixelRatio: 2 // 1 = standard, 2 = retina, 3 = ultra HD
```

## Known Limitations

1. **File Size**: 10MB upload limit (browser memory constraint)
2. **Image Dimensions**: 6000×6000 max (performance limit)
3. **Undo History**: 20 steps (memory optimization)
4. **Custom Stickers**: No deletion from palette (session only)
5. **No Persistence**: Work is lost on page reload
6. **Text Rendering**: Emoji may vary by OS/browser

## Troubleshooting

**Photo won't upload**:
- Check file size (must be under 10MB)
- Verify format (JPG, PNG, WEBP only)
- Try a different browser

**Sticker appears blurry**:
- This is normal for preview scaling
- Download will be sharp at original resolution

**Performance issues**:
- Reduce photo resolution before upload
- Close other browser tabs
- Disable grid/guides if using many stickers

**Download not working**:
- Check browser popup blocker
- Ensure enough disk space
- Try right-click → "Save link as"

## Advanced Features

### Keyboard Shortcuts
- `Delete` or `Backspace`: Delete selected sticker
- `Ctrl+Z` / `Cmd+Z`: Undo
- `Ctrl+Shift+Z` / `Cmd+Shift+Z`: Redo
- `Arrow keys`: Move selected sticker (when implemented)

### Snapping Behavior
With guides enabled:
- Stickers snap to center lines when within 8px
- Grid provides 8px increments for precise alignment
- Hold Shift while dragging for axis-lock (Konva native)

### Layer Management
Stickers are rendered in order:
- First in array = bottom layer
- Last in array = top layer
- Use layer buttons to reorder
- Newly added stickers appear on top

## Development Notes

### Code Organization
The application is structured as:
1. **App Component**: Main state and UI layout
2. **CanvasEditor Component**: Konva stage and rendering
3. **Utility Functions**: Upload, download, history management
4. **Style System**: CSS with hand-drawn aesthetic

### State Management
Key state variables:
- `photo`: Current photo metadata
- `photoImage`: HTML Image element for rendering
- `stickers`: Array of sticker objects with properties
- `selectedId`: Currently selected sticker ID
- `history`: Array of past sticker states
- `historyStep`: Current position in history

### Sticker Object Schema
```javascript
{
  id: number,           // Unique identifier
  content: string,      // Emoji char or image data URL
  isCustom: boolean,    // True for uploaded images
  x: number,            // Center X position
  y: number,            // Center Y position
  width: number,        // Width in pixels
  height: number,       // Height in pixels
  rotation: number,     // Degrees (-180 to 180)
  opacity: number,      // 0 to 1
  scaleX: number,       // X scale multiplier
  scaleY: number,       // Y scale multiplier
  flipX: boolean,       // Horizontal flip
  flipY: boolean        // Vertical flip
}
```

## Future Enhancement Ideas

- [ ] Text tool with custom fonts
- [ ] Drawing/brush tool
- [ ] Filters and effects
- [ ] Preset layouts/templates
- [ ] Cloud save functionality
- [ ] Batch processing
- [ ] GIF/video export
- [ ] Collaboration features
- [ ] Mobile app version
- [ ] Print-optimized export

## Credits

**Design**: Based on "Shroomy AI Tips" character design reference
**Framework**: React + Konva.js
**Icons**: Unicode emoji
**Typography**: Comic Sans MS family for hand-drawn feel

## License

This project is provided as-is for personal and commercial use.
Feel free to modify and distribute.

## Support

For issues or questions:
1. Check the Troubleshooting section above
2. Review browser console for error messages
3. Test in a different browser
4. Verify image file format and size

---

**Made with 🍄 and ✨**

*Shroomy Editor - Add magic to your photos!*
