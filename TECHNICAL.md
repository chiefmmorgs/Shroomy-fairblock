# Technical Documentation - Shroomy Editor

## Architecture Overview

### Technology Stack
- **React 18**: Component architecture and state management
- **Konva.js 9**: Canvas manipulation library
- **React-Konva 18**: React bindings for Konva
- **Vanilla JavaScript**: Core logic
- **CSS3**: Styling with hand-drawn aesthetic

### Application Structure

```
App Component (Root)
├── State Management
│   ├── photo & photoImage
│   ├── stickers array
│   ├── selectedId
│   ├── history & historyStep
│   └── UI state (grid, guides, toast)
│
├── Left Panel
│   ├── Upload Area
│   ├── Default Sticker Palette
│   ├── Custom Sticker Palette
│   └── Settings (grid, guides)
│
├── Center Panel
│   └── CanvasEditor Component
│       ├── Konva Stage
│       ├── Background Layer (photo)
│       ├── Overlay Layer (grid, guides)
│       ├── Sticker Layer
│       └── Transformer (selection handles)
│
└── Right Panel
    ├── Position Controls
    ├── Transform Controls
    ├── Layer Management
    └── Action Buttons
```

## Core Components

### 1. App Component
**Responsibilities:**
- Global state management
- File upload handling
- Sticker creation and manipulation
- History management (undo/redo)
- Export functionality
- Toast notifications

**Key State:**
```javascript
{
  photo: {
    src: string,              // Data URL
    originalWidth: number,
    originalHeight: number,
    displayWidth: number,
    displayHeight: number
  },
  photoImage: HTMLImageElement,
  stickers: Sticker[],
  selectedId: number | null,
  history: Sticker[][],      // Array of sticker states
  historyStep: number,
  customStickers: string[],  // Data URLs
  canvasSize: { width, height }
}
```

### 2. CanvasEditor Component
**Responsibilities:**
- Rendering Konva stage
- Handling sticker transforms
- Managing selection state
- Drawing grid and guides

**Props:**
```javascript
{
  stageRef: RefObject,
  transformerRef: RefObject,
  photo: PhotoData,
  photoImage: HTMLImageElement,
  stickers: Sticker[],
  setStickers: Function,
  selectedId: number | null,
  setSelectedId: Function,
  canvasSize: { width, height },
  showGrid: boolean,
  showGuides: boolean,
  addToHistory: Function
}
```

## Data Models

### Sticker Object
```javascript
{
  id: number,           // Unique timestamp-based ID
  content: string,      // Emoji char or image data URL
  isCustom: boolean,    // Distinguishes emoji from images
  
  // Position (center point)
  x: number,
  y: number,
  
  // Dimensions
  width: number,
  height: number,
  
  // Transform
  rotation: number,     // -180 to 180 degrees
  opacity: number,      // 0 to 1
  scaleX: number,       // Scale multiplier
  scaleY: number,
  
  // Flip
  flipX: boolean,
  flipY: boolean
}
```

### Photo Data
```javascript
{
  src: string,              // Base64 data URL
  originalWidth: number,    // Source image dimensions
  originalHeight: number,
  displayWidth: number,     // Canvas display dimensions
  displayHeight: number
}
```

## Key Algorithms

### 1. Canvas Size Calculation
```javascript
// Fit image to max 600px while preserving aspect ratio
const maxSize = 600;
let width = img.width;
let height = img.height;

if (width > maxSize || height > maxSize) {
  if (width > height) {
    height = (height / width) * maxSize;
    width = maxSize;
  } else {
    width = (width / height) * maxSize;
    height = maxSize;
  }
}
```

### 2. Export Scaling
```javascript
// Calculate scale factor for original resolution
const scaleX = photo.originalWidth / canvasSize.width;
const scaleY = photo.originalHeight / canvasSize.height;

// Apply to each sticker during export
const exportSticker = {
  ...sticker,
  x: sticker.x * scaleX,
  y: sticker.y * scaleY,
  width: sticker.width * scaleX,
  height: sticker.height * scaleY
};
```

### 3. History Management
```javascript
const addToHistory = (newState) => {
  // Remove future history if we're in the middle
  const newHistory = history.slice(0, historyStep + 1);
  
  // Add new state
  newHistory.push(newState);
  
  // Limit to 20 steps
  if (newHistory.length > 20) {
    newHistory.shift();
  } else {
    setHistoryStep(historyStep + 1);
  }
  
  setHistory(newHistory);
};
```

### 4. Sticker Transform Sync
```javascript
// Sync Konva transform to React state
const handleStickerTransformEnd = (id, e) => {
  const node = e.target;
  
  const newStickers = stickers.map(s => {
    if (s.id === id) {
      return {
        ...s,
        x: node.x(),
        y: node.y(),
        rotation: node.rotation(),
        scaleX: node.scaleX(),
        scaleY: node.scaleY(),
        // Update dimensions based on scale
        width: Math.max(10, node.width() * Math.abs(node.scaleX())),
        height: Math.max(10, node.height() * Math.abs(node.scaleY()))
      };
    }
    return s;
  });
  
  setStickers(newStickers);
  addToHistory(newStickers);
};
```

## Performance Optimizations

### 1. Image Loading
- Use `HTMLImageElement` for efficient rendering
- Cache custom sticker images in state
- Preload images before rendering to canvas

### 2. Canvas Rendering
- Separate preview resolution from export resolution
- Use `createImageBitmap` for large images
- Implement offscreen canvas for export

### 3. State Updates
- Batch related state changes
- Use functional updates to prevent race conditions
- Debounce rapid updates (could be added)

### 4. Memory Management
- Limit history to 20 steps
- Revoke blob URLs after download
- Clean up Konva stages after export

## Event Flow

### Photo Upload
```
User selects file
  → FileReader reads as data URL
    → Create HTMLImageElement
      → Calculate display size
        → Update photo state
          → Trigger canvas render
```

### Sticker Addition
```
User clicks sticker
  → Create sticker object with default props
    → Add to stickers array
      → Add to history
        → Set as selected
          → Render on canvas
```

### Sticker Transform
```
User drags/resizes sticker
  → Konva fires transform events
    → Update sticker properties
      → Sync to React state
        → Add to history
          → Re-render canvas
```

### Export
```
User clicks download
  → Create temporary Konva stage
    → Set to original resolution
      → Scale all elements
        → Add photo background
          → Add all stickers (with async image loading)
            → Export to blob
              → Trigger download
                → Clean up temporary stage
```

## Konva Integration

### Stage Setup
```javascript
<Stage
  ref={stageRef}
  width={canvasSize.width}
  height={canvasSize.height}
  onClick={handleStageClick}
>
  <Layer>
    {/* Photo background */}
    {/* Grid overlay */}
    {/* Guides */}
    {/* Stickers */}
  </Layer>
</Stage>
```

### Transformer Configuration
```javascript
<Transformer
  ref={transformerRef}
  boundBoxFunc={(oldBox, newBox) => {
    // Prevent resize below 10px
    if (newBox.width < 10 || newBox.height < 10) {
      return oldBox;
    }
    return newBox;
  }}
/>
```

### Custom Sticker Rendering
```javascript
// For custom images
<KonvaImage
  image={loadedImage}
  x={sticker.x}
  y={sticker.y}
  width={sticker.width}
  height={sticker.height}
  rotation={sticker.rotation}
  opacity={sticker.opacity}
  offsetX={sticker.width / 2}    // Center pivot
  offsetY={sticker.height / 2}
  draggable
/>

// For emoji
<KonvaText
  text={sticker.content}
  fontSize={sticker.width}
  // ... same props as KonvaImage
/>
```

## Extension Points

### Adding New Features

#### 1. Text Tool
```javascript
// Add to sticker object
{
  type: 'text',
  content: string,
  fontFamily: string,
  fontSize: number,
  fontStyle: string,
  align: string,
  // ... existing props
}

// Render with KonvaText
<KonvaText
  text={sticker.content}
  fontFamily={sticker.fontFamily}
  // ...
/>
```

#### 2. Filters/Effects
```javascript
// Add to sticker object
{
  filters: [{
    type: 'blur',
    radius: number
  }, {
    type: 'brightness',
    value: number
  }]
}

// Apply Konva filters
import Konva from 'konva';

<KonvaImage
  filters={[Konva.Filters.Blur, Konva.Filters.Brighten]}
  blurRadius={sticker.blurRadius}
  brightness={sticker.brightness}
/>
```

#### 3. Shape Tool
```javascript
// Add shape components
<Rect
  x={shape.x}
  y={shape.y}
  width={shape.width}
  height={shape.height}
  fill={shape.fill}
  stroke={shape.stroke}
  strokeWidth={shape.strokeWidth}
  cornerRadius={shape.cornerRadius}
/>

<Circle
  x={shape.x}
  y={shape.y}
  radius={shape.radius}
  fill={shape.fill}
/>
```

#### 4. Drawing Tool
```javascript
// Add line drawing
<Line
  points={shape.points}  // [x1, y1, x2, y2, ...]
  stroke={shape.color}
  strokeWidth={shape.width}
  tension={0.5}          // Smoothing
  lineCap="round"
  lineJoin="round"
/>
```

### Modifying Export

#### 1. Different Formats
```javascript
// Add format parameter
const downloadImage = (format = 'png') => {
  if (format === 'jpg') {
    stage.toBlob({
      callback: handleBlob,
      mimeType: 'image/jpeg',
      quality: 0.9
    });
  }
};
```

#### 2. Adding Watermark
```javascript
// Before export, add watermark to layer
const watermark = new Konva.Text({
  text: '© Your Name',
  fontSize: 24,
  x: width - 150,
  y: height - 40,
  opacity: 0.5
});
layer.add(watermark);
```

#### 3. Multiple Resolutions
```javascript
const resolutions = [
  { name: 'thumbnail', scale: 0.25 },
  { name: 'medium', scale: 0.5 },
  { name: 'full', scale: 1 }
];

for (const res of resolutions) {
  // Create stage at res.scale
  // Export with filename including res.name
}
```

## Testing Considerations

### Unit Tests
```javascript
// Test sticker creation
test('addSticker creates valid sticker object', () => {
  const sticker = createSticker('🍄');
  expect(sticker).toHaveProperty('id');
  expect(sticker).toHaveProperty('content', '🍄');
  expect(sticker.x).toBeGreaterThan(0);
});

// Test history management
test('undo reverts to previous state', () => {
  // Add sticker
  // Undo
  // Check stickers array matches previous state
});
```

### Integration Tests
```javascript
// Test photo upload
test('photo upload updates canvas size', async () => {
  const file = new File(['...'], 'test.jpg', { type: 'image/jpeg' });
  await handlePhotoUpload(file);
  expect(canvasSize.width).toBeGreaterThan(0);
});

// Test export
test('export produces valid blob', async () => {
  const blob = await exportImage();
  expect(blob.type).toBe('image/png');
  expect(blob.size).toBeGreaterThan(0);
});
```

### E2E Tests
```javascript
// Cypress example
it('complete workflow', () => {
  cy.visit('/shroomy-editor.html');
  cy.get('input[type="file"]').attachFile('test-photo.jpg');
  cy.get('.sticker-item').first().click();
  cy.get('.btn-primary').contains('Download').click();
  cy.readFile('downloads/shroomy-creation.png').should('exist');
});
```

## Browser Compatibility Notes

### Required Features
- Canvas 2D Context
- FileReader API
- Blob and URL APIs
- ES6+ JavaScript
- CSS Grid and Flexbox

### Polyfill Needs (for older browsers)
```javascript
// Array.prototype.findIndex
// Array.prototype.find
// Object.assign
// Promise
```

### Known Issues
1. **Safari**: May require user gesture for file download
2. **iOS**: Large images may crash on low-memory devices
3. **Firefox**: Emoji rendering differs from Chrome
4. **Edge Legacy**: Limited Canvas API support

## Debugging Tips

### Enable Konva Debug Mode
```javascript
Konva.showWarnings = true;
```

### Log State Changes
```javascript
useEffect(() => {
  console.log('Stickers updated:', stickers);
}, [stickers]);
```

### Canvas Inspection
```javascript
// Access Konva stage
const stage = stageRef.current;
console.log('Stage size:', stage.width(), stage.height());
console.log('Layer children:', stage.getLayers()[0].getChildren());
```

### Performance Profiling
```javascript
// Wrap expensive operations
console.time('export');
await downloadImage();
console.timeEnd('export');
```

## Common Modifications

### Change Default Canvas Size
```javascript
// Line 119 in handlePhotoUpload
const maxSize = 800; // Increase from 600
```

### Adjust Transform Limits
```javascript
// In Transformer boundBoxFunc
if (newBox.width < 20 || newBox.height < 20) { // Changed from 10
  return oldBox;
}
```

### Add More Default Stickers
```javascript
const DEFAULT_STICKERS = [
  '🍄', '🌟', '✨', '💜',
  '🌸', '🦋', '🌈', '⭐', // Add more here
];
```

### Customize Color Theme
```css
/* Change primary purple */
:root {
  --primary-color: #b577d6;
  --primary-dark: #8b5ca8;
}

/* Use in CSS */
.btn-primary {
  background: var(--primary-color);
}
```

## API Reference

### Main Functions

#### `handlePhotoUpload(file: File)`
Processes uploaded photo, creates HTMLImageElement, calculates canvas size.

#### `addSticker(content: string, isCustom: boolean)`
Creates new sticker object and adds to canvas.

#### `updateSticker(updates: Partial<Sticker>)`
Updates selected sticker properties and adds to history.

#### `addToHistory(newState: Sticker[])`
Adds current sticker state to history, maintains 20-step limit.

#### `downloadImage()`
Exports composition at original resolution as PNG blob.

### Utility Functions

#### `showToast(message: string)`
Displays temporary notification to user.

#### `moveLayer(direction: 'up' | 'down' | 'top' | 'bottom')`
Reorders stickers in layer stack.

#### `handleStickerDragEnd(id: number, e: KonvaEventObject)`
Syncs sticker position after drag.

#### `handleStickerTransformEnd(id: number, e: KonvaEventObject)`
Syncs sticker transform after resize/rotate.

---

## Support & Contributing

For questions or contributions, please refer to:
- Main README.md for user documentation
- GitHub repository (if applicable)
- Issue tracker for bug reports

**Last Updated**: October 2025  
**Version**: 1.0.0
