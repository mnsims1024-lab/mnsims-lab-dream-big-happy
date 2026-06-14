from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from app.core import Builder, AccessibilityValidator, AutoPatcher

app = FastAPI(
    title="AccessibilityBuilder API",
    description="Build accessible applications with AI assistance",
    version="1.0.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============ Pydantic Models ============

class HealthResponse(BaseModel):
    status: str
    message: str
    version: str


class GenerateRequest(BaseModel):
    description: str
    wcag_level: str = "AA"
    voice_enabled: bool = True
    include_tts: bool = True


class ValidateRequest(BaseModel):
    code: str
    code_type: str  # "html", "react", "css"


class PatchRequest(BaseModel):
    html: Optional[str] = None
    css: Optional[str] = None
    component: Optional[str] = None


# ============ Health & Info Endpoints ============

@app.get("/", response_model=HealthResponse)
async def root():
    """Welcome endpoint"""
    return {
        "status": "healthy",
        "message": "AccessibilityBuilder API is running",
        "version": "1.0.0"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "API is operational",
        "version": "1.0.0"
    }


@app.get("/api/info")
async def api_info():
    """Get API information"""
    return {
        "name": "AccessibilityBuilder Bot",
        "version": "1.0.0",
        "description": "Intelligent builder for accessible applications",
        "features": [
            "Code generation from text descriptions",
            "WCAG 2.1 AA compliance validation",
            "Automatic error detection and patching",
            "Voice control support",
            "Text-to-speech integration"
        ]
    }


# ============ Builder Endpoints ============

@app.post("/api/build")
async def build_from_description(request: GenerateRequest):
    """Generate accessible application from text description"""
    try:
        from app.core import BuilderConfig
        config = BuilderConfig(
            wcag_level=request.wcag_level,
            voice_enabled=request.voice_enabled
        )
        builder = Builder(config)
        result = builder.generate_from_text(request.description)
        
        return {
            "success": result.success,
            "accessibility_score": result.accessibility_score,
            "components": result.components,
            "generated_files": list(result.generated_code.keys()),
            "errors": result.errors,
            "warnings": result.warnings,
            "timestamp": result.timestamp
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============ Validation Endpoints ============

@app.post("/api/validate")
async def validate_code(request: ValidateRequest):
    """Validate code for accessibility compliance"""
    try:
        validator = AccessibilityValidator(wcag_level="AA")
        
        if request.code_type == "html":
            is_valid, issues = validator.validate_html(request.code)
        elif request.code_type == "react":
            is_valid, issues = validator.validate_react_component(request.code)
        elif request.code_type == "css":
            is_valid, issues = validator.validate_css(request.code)
        else:
            raise ValueError(f"Unknown code type: {request.code_type}")
        
        return {
            "is_valid": is_valid,
            "code_type": request.code_type,
            "issues_count": len(issues),
            "issues": [
                {
                    "rule": issue.rule,
                    "severity": issue.severity,
                    "element": issue.element,
                    "description": issue.description,
                    "suggestion": issue.suggestion,
                    "wcag_criterion": issue.wcag_criterion
                }
                for issue in issues
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============ Patching Endpoints ============

@app.post("/api/patch")
async def auto_patch_code(request: PatchRequest):
    """Automatically patch code for accessibility issues"""
    try:
        patcher = AutoPatcher()
        results = {}
        
        if request.html:
            patched_html, patches = patcher.patch_html(request.html)
            results["html"] = {
                "patched": patched_html,
                "patches_applied": patches,
                "patches_count": len(patches)
            }
        
        if request.css:
            patched_css, patches = patcher.patch_css(request.css)
            results["css"] = {
                "patched": patched_css,
                "patches_applied": patches,
                "patches_count": len(patches)
            }
        
        if request.component:
            patched_component, patches = patcher.patch_react_component(request.component)
            results["component"] = {
                "patched": patched_component,
                "patches_applied": patches,
                "patches_count": len(patches)
            }
        
        return {"success": True, "results": results}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============ Components Endpoints ============

@app.get("/api/components")
async def list_components():
    """List all available accessible components"""
    return {
        "components": [
            {"name": "AccessibleButton", "description": "Fully accessible button with ARIA labels and keyboard support"},
            {"name": "AccessibleInput", "description": "Accessible form input with proper labels"},
            {"name": "AccessibleCard", "description": "Accessible content card with semantic structure"},
            {"name": "SkipLinks", "description": "Skip navigation links for keyboard users"},
            {"name": "VoiceControl", "description": "Voice control interface"},
            {"name": "TextToSpeech", "description": "Read aloud functionality"},
            {"name": "AriaLiveRegion", "description": "Live region for dynamic content"}
        ]
    }


# ============ Templates Endpoints ============

@app.get("/api/templates")
async def list_templates():
    """List available app templates"""
    return {
        "templates": [
            {"id": "medication-reminder", "name": "Medication Reminder", "description": "Voice-controlled reminder for elderly users"},
            {"id": "audio-book-reader", "name": "Audio Book Reader", "description": "Text-to-speech enabled reader"},
            {"id": "voice-journal", "name": "Voice Journal", "description": "Hands-free journaling"}
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
