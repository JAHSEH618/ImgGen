## Anthropic-Style React Image Upload Frontend

This is a beautiful React frontend interface for uploading prompts and multiple images, styled with Anthropic's design language.

### Features

- 🎨 **Anthropic-Inspired Design**: Clean, modern UI with gradients and smooth animations
- 📝 **Prompt Input**: Large textarea for creative prompts with character count
- 🖼️ **Multi-Image Upload**: Drag-and-drop interface supporting multiple images
- 📱 **Responsive Design**: Works beautifully on desktop and mobile
- ⚡ **Real-time Preview**: Image thumbnails with remove functionality
- 🚀 **Upload Progress**: Loading states and status messages
- 🛡️ **File Validation**: Supports common image formats with size limits

### Setup Instructions

1. **Navigate to the frontend directory:**
   ```bash
   cd img/frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   ```

4. **Open your browser to:**
   ```
   http://localhost:5173
   ```

### API Integration

The frontend is configured to proxy API requests to your Flask backend running on port 10086:
- Upload endpoint: `/api/upload`
- The Vite proxy automatically forwards requests to `http://localhost:10086`

### Usage

1. Enter your creative prompt in the textarea
2. Drag and drop images or click to browse
3. Preview selected images and remove if needed
4. Click "Generate with AI" to upload and process

### File Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── ImageUploadForm.jsx    # Main upload component
│   │   └── ImageUploadForm.css    # Component styles
│   ├── App.jsx                    # Main app component
│   ├── App.css                    # App styles
│   ├── main.jsx                   # Entry point
│   └── index.css                  # Global styles
├── index.html                     # HTML template
├── package.json                   # Dependencies
└── vite.config.js                # Vite configuration
```

### Styling

The interface follows Anthropic's design principles:
- **Typography**: Inter font family for clean readability
- **Colors**: Professional gradients (blues and purples)
- **Spacing**: Generous whitespace and consistent padding
- **Interactions**: Smooth hover effects and transitions
- **Accessibility**: Proper contrast and focus states