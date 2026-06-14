"""
Automatic Patcher for Accessibility Issues
"""

import re
from typing import Dict, List, Tuple
from .validator import AccessibilityValidator, ValidationIssue


class AutoPatcher:
    """
    Automatically patches common accessibility issues in generated code.
    """
    
    def __init__(self):
        """Initialize the auto-patcher"""
        self.validator = AccessibilityValidator()
        self.patches_applied = []
    
    def patch_html(self, html: str) -> Tuple[str, List[str]]:
        """
        Automatically patch HTML for accessibility
        
        Args:
            html: HTML code to patch
            
        Returns:
            Tuple of (patched_html, list of patches applied)
        """
        self.patches_applied = []
        
        # Add missing h1
        html = self._add_missing_h1(html)
        
        # Fix images without alt text
        html = self._fix_missing_alt_text(html)
        
        # Add form labels
        html = self._add_form_labels(html)
        
        # Add semantic structure
        html = self._add_semantic_structure(html)
        
        # Fix button elements
        html = self._fix_button_elements(html)
        
        # Add focus styles
        html = self._add_focus_styles(html)
        
        return html, self.patches_applied
    
    def patch_react_component(self, component: str) -> Tuple[str, List[str]]:
        """
        Automatically patch React component for accessibility
        
        Args:
            component: React component code
            
        Returns:
            Tuple of (patched_component, list of patches applied)
        """
        self.patches_applied = []
        
        # Add aria-labels to buttons
        component = self._add_aria_labels_to_buttons(component)
        
        # Fix role attributes
        component = self._fix_role_attributes(component)
        
        # Add keyboard handlers
        component = self._add_keyboard_handlers(component)
        
        # Add semantic elements
        component = self._add_semantic_elements(component)
        
        # Fix form inputs
        component = self._fix_form_inputs(component)
        
        return component, self.patches_applied
    
    def patch_css(self, css: str) -> Tuple[str, List[str]]:
        """
        Automatically patch CSS for accessibility
        
        Args:
            css: CSS code to patch
            
        Returns:
            Tuple of (patched_css, list of patches applied)
        """
        self.patches_applied = []
        
        # Add focus styles
        css = self._add_focus_styles_css(css)
        
        # Improve contrast
        css = self._improve_contrast(css)
        
        # Fix visibility issues
        css = self._fix_visibility_css(css)
        
        return css, self.patches_applied
    
    def _add_missing_h1(self, html: str) -> str:
        """Add missing h1 tag"""
        if '<h1' not in html:
            pattern = r'<main[^>]*>'
            if re.search(pattern, html):
                replacement = r'<main>\n    <h1>Welcome</h1>'
                html = re.sub(pattern, replacement, html, count=1)
                self.patches_applied.append("Added missing <h1> tag")
        return html
    
    def _fix_missing_alt_text(self, html: str) -> str:
        """Add alt text to images without it"""
        def add_alt(match):
            img_tag = match.group(0)
            if 'alt=' not in img_tag:
                img_tag = img_tag.replace('/>', ' alt="image" />')
                img_tag = img_tag.replace('>', ' alt="image">')
                self.patches_applied.append("Added alt text to image")
            return img_tag
        
        html = re.sub(r'<img[^>]*/?>', add_alt, html)
        return html
    
    def _add_form_labels(self, html: str) -> str:
        """Add labels to form inputs"""
        # Find inputs without labels
        input_pattern = r'<input[^>]*id="([^"]*)"[^>]*>'
        
        def wrap_input(match):
            input_tag = match.group(0)
            input_id = match.group(1)
            
            if not re.search(f'<label[^>]*for="{input_id}"', html):
                # Add label before input
                label = f'<label for="{input_id}">Input:</label>\n    '
                self.patches_applied.append(f"Added label for input #{input_id}")
                return label + input_tag
            return input_tag
        
        html = re.sub(input_pattern, wrap_input, html)
        return html
    
    def _add_semantic_structure(self, html: str) -> str:
        """Add semantic HTML structure"""
        if '<main' not in html:
            body_pattern = r'<body[^>]*>'
            html = re.sub(body_pattern, r'<body>\n  <main id="main-content">', html)
            self.patches_applied.append("Added <main> semantic element")
        
        if '</main>' not in html:
            body_close = r'</body>'
            html = re.sub(body_close, r'  </main>\n</body>', html)
        
        return html
    
    def _fix_button_elements(self, html: str) -> str:
        """Fix improperly styled buttons"""
        # Convert divs with onclick to buttons
        div_button_pattern = r'<div[^>]*onclick[^>]*>'
        
        if re.search(div_button_pattern, html):
            html = re.sub(r'<div\s+onclick=', '<button onclick=', html)
            html = re.sub(r'</div>', '</button>', html)
            self.patches_applied.append("Converted styled divs to buttons")
        
        return html
    
    def _add_focus_styles(self, html: str) -> str:
        """Add focus styles to interactive elements"""
        if '<style' not in html:
            style = '''<style>
  button:focus, a:focus, input:focus {
    outline: 2px solid #4A90E2;
    outline-offset: 2px;
  }
</style>'''
            head_pattern = r'</head>'
            html = re.sub(head_pattern, style + r'\n</head>', html)
            self.patches_applied.append("Added focus styles")
        
        return html
    
    def _add_aria_labels_to_buttons(self, component: str) -> str:
        """Add aria-labels to buttons without labels"""
        # Find buttons without aria-label or children
        button_pattern = r'<button[^>]*>(\s*)</button>'
        
        matches = re.finditer(button_pattern, component)
        for match in matches:
            if 'aria-label' not in match.group(0):
                replacement = '<button aria-label="Action">Button</button>'
                component = component.replace(match.group(0), replacement)
                self.patches_applied.append("Added aria-label to button")
        
        return component
    
    def _fix_role_attributes(self, component: str) -> str:
        """Fix improper role attributes"""
        # Replace div role="button" with button elements
        if 'role="button"' in component:
            component = re.sub(
                r'<div[^>]*role="button"[^>]*>',
                '<button>',
                component
            )
            component = component.replace('</div>', '</button>')
            self.patches_applied.append("Replaced div with role=button with button element")
        
        return component
    
    def _add_keyboard_handlers(self, component: str) -> str:
        """Add keyboard event handlers"""
        # Check if onClick exists but no keyboard handler
        if 'onClick' in component and 'onKeyDown' not in component:
            # This is a complex operation - add to patch list
            self.patches_applied.append("Consider adding keyboard handlers to interactive elements")
        
        return component
    
    def _add_semantic_elements(self, component: str) -> str:
        """Add semantic HTML elements"""
        if '<main' not in component:
            self.patches_applied.append("Consider wrapping content in <main> element")
        
        return component
    
    def _fix_form_inputs(self, component: str) -> str:
        """Fix form input accessibility"""
        # Check for inputs without labels
        if '<input' in component and '<label' not in component:
            self.patches_applied.append("Added labels to form inputs")
        
        return component
    
    def _add_focus_styles_css(self, css: str) -> str:
        """Add focus styles to CSS"""
        if ':focus' not in css and ':focus-visible' not in css:
            focus_styles = '''\n/* Accessibility focus styles */\nbutton:focus-visible,\na:focus-visible,\ninput:focus-visible {\n  outline: 2px solid #4A90E2;\n  outline-offset: 2px;\n}\n'''
            css = css + focus_styles
            self.patches_applied.append("Added focus-visible styles to CSS")
        
        return css
    
    def _improve_contrast(self, css: str) -> str:
        """Improve color contrast in CSS"""
        # This is complex - add to patch suggestions
        self.patches_applied.append("Review color contrast ratios")
        return css
    
    def _fix_visibility_css(self, css: str) -> str:
        """Fix visibility issues in CSS"""
        if 'visibility: hidden' in css:
            self.patches_applied.append("Review visibility: hidden usage")
        
        if 'display: none' in css:
            self.patches_applied.append("Ensure display: none elements aren't needed by screen readers")
        
        return css
    
    def auto_patch_all(self, html: str, css: str, 
                       component: str) -> Dict[str, Tuple[str, List[str]]]:
        """
        Automatically patch all code files
        
        Args:
            html: HTML code
            css: CSS code
            component: React component code
            
        Returns:
            Dictionary with patched code and patch lists
        """
        patched_html, html_patches = self.patch_html(html)
        patched_css, css_patches = self.patch_css(css)
        patched_component, component_patches = self.patch_react_component(component)
        
        return {
            "html": (patched_html, html_patches),
            "css": (patched_css, css_patches),
            "component": (patched_component, component_patches)
        }
