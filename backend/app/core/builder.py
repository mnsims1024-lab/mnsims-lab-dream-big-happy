"""
Intelligent Builder Engine for Accessible Applications
"""

import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class BuilderConfig:
    """Configuration for the builder"""
    wcag_level: str = "AA"  # A, AA, AAA
    framework: str = "react"
    language: str = "en"
    voice_enabled: bool = True
    theme: str = "high-contrast"
    responsive: bool = True


@dataclass
class BuildResult:
    """Result of a build operation"""
    success: bool
    generated_code: Dict[str, str]
    components: List[str]
    accessibility_score: float
    errors: List[str]
    warnings: List[str]
    timestamp: str


class Builder:
    """
    Main builder engine for generating accessible applications.
    
    This class orchestrates the code generation process, ensuring
    WCAG 2.1 compliance and accessibility best practices.
    """
    
    def __init__(self, config: Optional[BuilderConfig] = None):
        """
        Initialize the Builder
        
        Args:
            config: BuilderConfig object with builder settings
        """
        self.config = config or BuilderConfig()
        self.generated_code = {}
        self.components = []
        self.errors = []
        self.warnings = []
    
    def generate_from_text(self, description: str) -> BuildResult:
        """
        Generate accessible application from text description.
        
        Args:
            description: Natural language description of the app
            
        Returns:
            BuildResult with generated code and analysis
        """
        self.errors = []
        self.warnings = []
        self.generated_code = {}
        self.components = []
        
        try:
            # Parse the description
            parsed = self._parse_description(description)
            
            # Generate components
            self.components = self._generate_components(parsed)
            
            # Generate code for each component
            for component in self.components:
                self.generated_code[component["name"]] = self._generate_component_code(component)
            
            # Generate main app structure
            self.generated_code["App.jsx"] = self._generate_app_structure(parsed)
            self.generated_code["main.py"] = self._generate_backend_structure(parsed)
            
            # Calculate accessibility score
            score = self._calculate_accessibility_score()
            
            return BuildResult(
                success=len(self.errors) == 0,
                generated_code=self.generated_code,
                components=[c["name"] for c in self.components],
                accessibility_score=score,
                errors=self.errors,
                warnings=self.warnings,
                timestamp=datetime.now().isoformat()
            )
        
        except Exception as e:
            self.errors.append(f"Build failed: {str(e)}")
            return BuildResult(
                success=False,
                generated_code={},
                components=[],
                accessibility_score=0.0,
                errors=self.errors,
                warnings=self.warnings,
                timestamp=datetime.now().isoformat()
            )
    
    def _parse_description(self, description: str) -> Dict[str, Any]:
        """Parse natural language description into structured data"""
        # Basic parsing - can be enhanced with NLP
        return {
            "description": description,
            "requires_voice": "voice" in description.lower(),
            "requires_tts": "text to speech" in description.lower() or "audio" in description.lower(),
            "target_users": self._identify_users(description),
            "features": self._extract_features(description),
            "accessibility_requirements": self._extract_a11y_requirements(description)
        }
    
    def _identify_users(self, description: str) -> List[str]:
        """Identify target user groups from description"""
        users = []
        keywords = {
            "elderly": ["elderly", "seniors", "older", "aging"],
            "blind": ["blind", "vision loss", "visual impairment"],
            "deaf": ["deaf", "hearing loss", "hard of hearing"],
            "mobility": ["mobility", "wheelchair", "motor"],
            "cognitive": ["cognitive", "dyslexia", "adhd"]
        }
        
        desc_lower = description.lower()
        for user_type, keywords_list in keywords.items():
            if any(keyword in desc_lower for keyword in keywords_list):
                users.append(user_type)
        
        return users or ["general"]
    
    def _extract_features(self, description: str) -> List[str]:
        """Extract features from description"""
        features = []
        feature_keywords = {
            "reminders": ["reminder", "notification", "alert"],
            "voice_control": ["voice", "command", "speak"],
            "large_text": ["large", "font", "text size", "readable"],
            "high_contrast": ["contrast", "color", "visibility"],
            "simple_ui": ["simple", "easy", "minimal", "clean"],
            "audio": ["audio", "sound", "speak", "text-to-speech"]
        }
        
        desc_lower = description.lower()
        for feature, keywords in feature_keywords.items():
            if any(keyword in desc_lower for keyword in keywords):
                features.append(feature)
        
        return list(set(features))  # Remove duplicates
    
    def _extract_a11y_requirements(self, description: str) -> List[str]:
        """Extract accessibility requirements"""
        requirements = [
            "keyboard_navigation",
            "screen_reader_compatible",
            "semantic_html",
            "aria_labels",
            "color_contrast"
        ]
        
        if "high contrast" in description.lower():
            requirements.append("high_contrast_mode")
        if "voice" in description.lower():
            requirements.append("voice_control")
        if "audio" in description.lower() or "text to speech" in description.lower():
            requirements.append("text_to_speech")
        
        return requirements
    
    def _generate_components(self, parsed: Dict) -> List[Dict]:
        """Generate list of components needed"""
        components = [
            {"name": "AccessibleButton", "type": "UI"},
            {"name": "AccessibleInput", "type": "UI"},
            {"name": "AccessibleCard", "type": "UI"},
            {"name": "SkipLinks", "type": "Navigation"},
            {"name": "AriaLiveRegion", "type": "Accessibility"},
        ]
        
        if parsed["requires_voice"]:
            components.append({"name": "VoiceControl", "type": "Feature"})
        
        if parsed["requires_tts"]:
            components.append({"name": "TextToSpeech", "type": "Feature"})
        
        return components
    
    def _generate_component_code(self, component: Dict) -> str:
        """Generate code for a component"""
        templates = {
            "AccessibleButton": self._template_accessible_button(),
            "AccessibleInput": self._template_accessible_input(),
            "AccessibleCard": self._template_accessible_card(),
            "SkipLinks": self._template_skip_links(),
            "AriaLiveRegion": self._template_aria_live(),
            "VoiceControl": self._template_voice_control(),
            "TextToSpeech": self._template_text_to_speech(),
        }
        
        return templates.get(component["name"], "// Component not found")
    
    def _template_accessible_button(self) -> str:
        """Template for accessible button component"""
        return '''import React from 'react';
import './AccessibleButton.css';

export const AccessibleButton = ({ 
  children, 
  onClick, 
  ariaLabel,
  variant = 'primary',
  disabled = false 
}) => {
  return (
    <button
      className={`accessible-button accessible-button--${variant}`}
      onClick={onClick}
      aria-label={ariaLabel || children}
      disabled={disabled}
      tabIndex={disabled ? -1 : 0}
    >
      {children}
    </button>
  );
};
'''
    
    def _template_accessible_input(self) -> str:
        """Template for accessible input component"""
        return '''import React from 'react';
import './AccessibleInput.css';

export const AccessibleInput = ({
  label,
  id,
  type = 'text',
  placeholder,
  required = false,
  ariaDescription,
  value,
  onChange,
  error
}) => {
  return (
    <div className="accessible-input-wrapper">
      <label htmlFor={id} className="accessible-input-label">
        {label}
        {required && <span aria-label="required">*</span>}
      </label>
      <input
        id={id}
        type={type}
        className={`accessible-input ${error ? 'accessible-input--error' : ''}`}
        placeholder={placeholder}
        required={required}
        value={value}
        onChange={onChange}
        aria-describedby={ariaDescription}
        aria-invalid={!!error}
      />
      {error && (
        <div id={`${id}-error`} className="accessible-input-error" role="alert">
          {error}
        </div>
      )}
    </div>
  );
};
'''
    
    def _template_accessible_card(self) -> str:
        """Template for accessible card component"""
        return '''import React from 'react';
import './AccessibleCard.css';

export const AccessibleCard = ({
  title,
  children,
  level = 'h2'
}) => {
  const HeadingTag = level;
  
  return (
    <article className="accessible-card">
      <HeadingTag className="accessible-card-title">
        {title}
      </HeadingTag>
      <div className="accessible-card-content">
        {children}
      </div>
    </article>
  );
};
'''
    
    def _template_skip_links(self) -> str:
        """Template for skip links"""
        return '''import React from 'react';
import './SkipLinks.css';

export const SkipLinks = () => {
  return (
    <nav className="skip-links">
      <a href="#main-content" className="skip-link">
        Skip to main content
      </a>
      <a href="#navigation" className="skip-link">
        Skip to navigation
      </a>
      <a href="#footer" className="skip-link">
        Skip to footer
      </a>
    </nav>
  );
};
'''
    
    def _template_aria_live(self) -> str:
        """Template for ARIA live region"""
        return '''import React from 'react';

export const AriaLiveRegion = ({
  message,
  politeness = 'polite',
  role = 'status'
}) => {
  return (
    <div
      aria-live={politeness}
      aria-atomic="true"
      role={role}
      className="aria-live-region"
    >
      {message}
    </div>
  );
};
'''
    
    def _template_voice_control(self) -> str:
        """Template for voice control"""
        return '''import React, { useState, useEffect } from 'react';

export const VoiceControl = ({ onCommand, ariaLabel }) => {
  const [isListening, setIsListening] = useState(false);
  
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  const recognition = new SpeechRecognition();
  
  useEffect(() => {
    recognition.onstart = () => setIsListening(true);
    recognition.onend = () => setIsListening(false);
    recognition.onresult = (event) => {
      const transcript = Array.from(event.results)
        .map(result => result[0].transcript)
        .join('');
      onCommand(transcript);
    };
  }, []);
  
  const toggleListening = () => {
    if (isListening) {
      recognition.stop();
    } else {
      recognition.start();
    }
  };
  
  return (
    <button
      onClick={toggleListening}
      aria-label={ariaLabel || (isListening ? 'Stop listening' : 'Start voice control')}
      aria-pressed={isListening}
      className={`voice-button ${isListening ? 'listening' : ''}`}
    >
      🎤 {isListening ? 'Listening...' : 'Voice Control'}
    </button>
  );
};
'''
    
    def _template_text_to_speech(self) -> str:
        """Template for text-to-speech"""
        return '''import React, { useState } from 'react';

export const TextToSpeech = ({ text, ariaLabel }) => {
  const [isSpeaking, setIsSpeaking] = useState(false);
  
  const synth = window.speechSynthesis;
  
  const speak = () => {
    if (isSpeaking) {
      synth.cancel();
      setIsSpeaking(false);
      return;
    }
    
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 0.9;
    utterance.pitch = 1;
    utterance.volume = 1;
    
    utterance.onend = () => setIsSpeaking(false);
    utterance.onerror = (event) => {
      console.error('Speech synthesis error:', event);
      setIsSpeaking(false);
    };
    
    setIsSpeaking(true);
    synth.speak(utterance);
  };
  
  return (
    <button
      onClick={speak}
      aria-label={ariaLabel || (isSpeaking ? 'Stop reading' : 'Read aloud')}
      aria-pressed={isSpeaking}
      className={`tts-button ${isSpeaking ? 'speaking' : ''}`}
    >
      🔊 {isSpeaking ? 'Reading...' : 'Read Aloud'}
    </button>
  );
};
'''
    
    def _generate_app_structure(self, parsed: Dict) -> str:
        """Generate main React app structure"""
        return '''import React, { useState } from 'react';
import { SkipLinks } from './components/SkipLinks';
import { AccessibleButton } from './components/AccessibleButton';
import { AccessibleInput } from './components/AccessibleInput';
import { AriaLiveRegion } from './components/AriaLiveRegion';
import './App.css';

function App() {
  const [message, setMessage] = useState('');

  return (
    <>
      <SkipLinks />
      <div className="app-container">
        <header role="banner">
          <h1>Accessible Application</h1>
        </header>
        
        <nav id="navigation" role="navigation" aria-label="Main navigation">
          <ul>
            <li><a href="#home">Home</a></li>
            <li><a href="#about">About</a></li>
            <li><a href="#help">Help</a></li>
          </ul>
        </nav>
        
        <main id="main-content">
          <AriaLiveRegion message={message} politeness="polite" />
          
          <section>
            <h2>Welcome</h2>
            <p>This is an accessible application built for everyone.</p>
            <AccessibleButton 
              onClick={() => setMessage('Button clicked!')}
              ariaLabel="Click me for welcome message"
            >
              Click Me
            </AccessibleButton>
          </section>
        </main>
        
        <footer id="footer">
          <p>&copy; 2024 Accessible Application. Made with ❤️</p>
        </footer>
      </div>
    </>
  );
}

export default App;
'''
    
    def _generate_backend_structure(self, parsed: Dict) -> str:
        """Generate main backend structure"""
        return '''from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(
    title="Accessible App API",
    description="Backend for accessible applications",
    version="1.0.0"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class HealthResponse(BaseModel):
    status: str
    message: str

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "API is running"
    }

@app.get("/api/config")
async def get_config():
    """Get application configuration"""
    return {
        "wcag_level": "AA",
        "theme": "high-contrast",
        "voice_enabled": True,
        "text_to_speech_enabled": True
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''
    
    def _calculate_accessibility_score(self) -> float:
        """Calculate accessibility score based on components and features"""
        base_score = 80.0
        
        # Add points for components
        base_score += len(self.components) * 2
        
        # Subtract points for warnings/errors
        base_score -= len(self.warnings) * 3
        base_score -= len(self.errors) * 5
        
        # Ensure score stays between 0-100
        return max(0, min(100, base_score))


if __name__ == "__main__":
    builder = Builder()
    description = """
    Create a medication reminder app for elderly users.
    Include voice commands and high contrast display.
    """
    result = builder.generate_from_text(description)
    print(f"Build successful: {result.success}")
    print(f"Accessibility score: {result.accessibility_score}")
    print(f"Components: {result.components}")
