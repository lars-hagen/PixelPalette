# PixelPalette 🎨

A creative web application that generates stunning AI art using OpenAI's DALL-E API. Built with SvelteKit for the frontend and Flask for API handling.

## Features

- 🖼️ Generate AI art from text prompts using DALL-E
- 🎨 Customize image styles and color palettes
- 📱 Responsive, modern interface built with Tailwind CSS
- 💾 Download generated images instantly
- 🚀 Runs completely locally

## Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- Poetry for Python dependency management
- OpenAI API key

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/PixelPalette.git
   cd PixelPalette
   ```

2. Install Python dependencies:
   ```bash
   poetry install
   ```

3. Install Node.js dependencies:
   ```bash
   cd app
   npm install
   ```

4. Set up your environment variables:
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

## Development

1. Start the Flask backend:
   ```bash
   poetry run python app/flask/main.py
   ```

2. In a separate terminal, start the SvelteKit development server:
   ```bash
   cd app
   npm run dev
   ```

3. Open your browser and navigate to `http://localhost:5173`

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 