# AccessibilityBuilder Bot 🌟

An open-source intelligent builder bot that generates accessible software for elderly, blind, disabled, and handicapped people.

**Mission:** Democratize assistive technology development through AI-powered code generation with accessibility-first principles.

## Features

- 🤖 **Intelligent Code Generation** - Convert text descriptions into production-ready accessible web apps
- ♿ **Accessibility-First** - WCAG 2.1 AA compliance built into every generated component
- 🔧 **Automatic Error Detection & Patching** - Real-time validation and self-healing code
- 🎯 **Voice Control Ready** - Built-in speech recognition and text-to-speech integration
- ⌨️ **Keyboard Navigation** - Full keyboard support on all generated components
- 🔊 **Screen Reader Optimized** - Semantic HTML and ARIA labels by default
- 📱 **Responsive Design** - Mobile and desktop accessibility support
- 🧪 **Automated Testing** - Accessibility testing included in build pipeline
- 📚 **Component Library** - Pre-built accessible components for rapid development

## Tech Stack

- **Backend:** Python (FastAPI)
- **Frontend:** React with Vite
- **Testing:** Pytest, Jest, Cypress with accessibility plugins
- **Accessibility Tools:** axe-core, WAVE, Pa11y
- **License:** MIT

## Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+
- Git

### Installation

```bash
# Clone repository
git clone https://github.com/mnsims1024-lab/mnsims-lab-dream-big-happy.git
cd mnsims-lab-dream-big-happy

# Install backend dependencies
cd backend
pip install -r requirements.txt

# Install frontend dependencies
cd ../frontend
npm install

# Start development servers
npm run dev
```

## Usage

### Generate an Accessible App from Text

```python
from accessibility_builder import Builder

builder = Builder()

# Simple text description
description = """
Create a medication reminder app for elderly users.
Include:
- Large, easy-to-read font
- Simple voice commands (say 'remind me')
- High contrast display
- Clear audio alerts
"""

app = builder.generate(description)
app.validate()  # Automatic accessibility check
app.build()     # Generate code
app.test()      # Run accessibility tests
```

## Project Structure

```
mnsims-lab-dream-big-happy/
├── backend/
│   ├── app/
│   │   ├── core/
│   │   ├── models/
│   │   ├── routes/
│   │   └── utils/
│   ├── tests/
│   ├── requirements.txt
│   └── main.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── App.jsx
│   ├── package.json
│   └── vite.config.js
├── templates/
├── docs/
├── examples/
├── .github/workflows/
├── LICENSE
└── README.md
```

## Documentation

- [Getting Started](docs/GETTING_STARTED.md)
- [Accessibility Guidelines](docs/ACCESSIBILITY_GUIDE.md)
- [API Documentation](docs/API.md)
- [Contributing](CONTRIBUTING.md)

## Examples

- Medication Reminder App
- Audio Book Reader
- Voice Journal

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

---

**Made with ❤️ for accessibility. For people who need it.**