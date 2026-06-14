"""
Accessibility Validator for WCAG 2.1 Compliance
"""

from typing import List, Dict, Any, Tuple
from dataclasses import dataclass
from enum import Enum


class SeverityLevel(str, Enum):
    """Severity levels for accessibility issues"""
    CRITICAL = "critical"
    SERIOUS = "serious"
    MODERATE = "moderate"
    MINOR = "minor"


@dataclass
class ValidationIssue:
    """Represents an accessibility validation issue"""
    rule: str
    severity: SeverityLevel
    element: str
    description: str
    suggestion: str
    wcag_criterion: str


class AccessibilityValidator:
    """
    Validates accessibility compliance for generated code.
    Checks against WCAG 2.1 guidelines at AA level by default.
    """
    
    def __init__(self, wcag_level: str = "AA"):
        """
        Initialize validator
        
        Args:
            wcag_level: WCAG compliance level (A, AA, AAA)
        """
        self.wcag_level = wcag_level
        self.issues = []
    
    def validate_html(self, html: str) -> Tuple[bool, List[ValidationIssue]]:
        """
        Validate HTML for accessibility issues
        
        Args:
            html: HTML code to validate
            
        Returns:
            Tuple of (is_valid, list of issues)
        """
        self.issues = []
        
        # Check for semantic HTML
        self._check_semantic_html(html)
        
        # Check for ARIA labels
        self._check_aria_labels(html)
        
        # Check for color contrast
        self._check_color_contrast(html)
        
        # Check for keyboard navigation
        self._check_keyboard_navigation(html)
        
        # Check for form labels
        self._check_form_labels(html)
        
        # Check for alt text
        self._check_alt_text(html)
        
        # Check for heading structure
        self._check_heading_structure(html)
        
        is_valid = all(issue.severity != SeverityLevel.CRITICAL for issue in self.issues)
        return is_valid, self.issues
    
    def validate_react_component(self, component_code: str) -> Tuple[bool, List[ValidationIssue]]:
        """
        Validate React component for accessibility
        
        Args:
            component_code: React component code
            
        Returns:
            Tuple of (is_valid, list of issues)
        """
        self.issues = []
        
        # Check for aria-label or htmlFor
        self._check_aria_props(component_code)
        
        # Check for semantic elements
        self._check_semantic_elements(component_code)
        
        # Check for keyboard handlers
        self._check_keyboard_handlers(component_code)
        
        # Check for role attributes
        self._check_role_attributes(component_code)
        
        is_valid = all(issue.severity != SeverityLevel.CRITICAL for issue in self.issues)
        return is_valid, self.issues
    
    def validate_css(self, css: str) -> Tuple[bool, List[ValidationIssue]]:
        """
        Validate CSS for accessibility issues
        
        Args:
            css: CSS code to validate
            
        Returns:
            Tuple of (is_valid, list of issues)
        """
        self.issues = []
        
        # Check for color contrast ratios
        self._check_css_contrast(css)
        
        # Check for focus styles
        self._check_focus_styles(css)
        
        # Check for visibility
        self._check_visibility(css)
        
        is_valid = all(issue.severity != SeverityLevel.CRITICAL for issue in self.issues)
        return is_valid, self.issues
    
    def _check_semantic_html(self, html: str):
        """Check for proper semantic HTML"""
        if '<button' not in html and '<a' in html:
            self.issues.append(ValidationIssue(
                rule="semantic_html_buttons",
                severity=SeverityLevel.SERIOUS,
                element="button",
                description="Links styled as buttons should use <button> element",
                suggestion="Replace <a> tags used as buttons with <button> elements",
                wcag_criterion="1.3.1 Info and Relationships"
            ))
        
        if '<table' in html and '<thead' not in html:
            self.issues.append(ValidationIssue(
                rule="semantic_html_tables",
                severity=SeverityLevel.MODERATE,
                element="table",
                description="Tables should have proper structure with <thead>",
                suggestion="Add <thead>, <tbody>, and <th> elements to tables",
                wcag_criterion="1.3.1 Info and Relationships"
            ))
    
    def _check_aria_labels(self, html: str):
        """Check for proper ARIA labels"""
        if '<button' in html and 'aria-label' not in html and '>Button<' in html:
            self.issues.append(ValidationIssue(
                rule="aria_labels_buttons",
                severity=SeverityLevel.SERIOUS,
                element="button",
                description="Button lacks descriptive label",
                suggestion="Add aria-label to buttons with icon-only content",
                wcag_criterion="1.1.1 Non-text Content"
            ))
    
    def _check_color_contrast(self, html: str):
        """Check for sufficient color contrast"""
        self.issues.append(ValidationIssue(
            rule="color_contrast",
            severity=SeverityLevel.SERIOUS,
            element="*",
            description="Cannot automatically verify color contrast - manual review needed",
            suggestion="Test with tools like WebAIM Contrast Checker",
            wcag_criterion="1.4.3 Contrast (Minimum)"
        ))
    
    def _check_keyboard_navigation(self, html: str):
        """Check for keyboard navigation support"""
        if 'tabindex' in html:
            if 'tabindex="-1"' not in html:
                self.issues.append(ValidationIssue(
                    rule="keyboard_navigation",
                    severity=SeverityLevel.MODERATE,
                    element="*",
                    description="Custom tabindex values should be avoided",
                    suggestion="Remove custom tabindex values - use semantic HTML instead",
                    wcag_criterion="2.1.1 Keyboard"
                ))
    
    def _check_form_labels(self, html: str):
        """Check for form labels"""
        if '<input' in html and '<label' not in html:
            self.issues.append(ValidationIssue(
                rule="form_labels",
                severity=SeverityLevel.CRITICAL,
                element="input",
                description="Form input lacks associated label",
                suggestion="Add <label> with htmlFor attribute matching input id",
                wcag_criterion="1.3.1 Info and Relationships"
            ))
    
    def _check_alt_text(self, html: str):
        """Check for alt text on images"""
        if '<img' in html and 'alt=' not in html:
            self.issues.append(ValidationIssue(
                rule="alt_text",
                severity=SeverityLevel.CRITICAL,
                element="img",
                description="Image missing alt text",
                suggestion="Add descriptive alt text to all images",
                wcag_criterion="1.1.1 Non-text Content"
            ))
    
    def _check_heading_structure(self, html: str):
        """Check for proper heading structure"""
        if '<h1' not in html:
            self.issues.append(ValidationIssue(
                rule="heading_structure",
                severity=SeverityLevel.SERIOUS,
                element="h1",
                description="Page should have exactly one <h1>",
                suggestion="Add a descriptive <h1> heading at the start of content",
                wcag_criterion="1.3.1 Info and Relationships"
            ))
    
    def _check_aria_props(self, code: str):
        """Check for ARIA properties in React"""
        if 'aria-' not in code and 'role=' not in code:
            self.issues.append(ValidationIssue(
                rule="aria_props",
                severity=SeverityLevel.MODERATE,
                element="component",
                description="Component lacks ARIA properties",
                suggestion="Add aria-label, aria-describedby, or role attributes",
                wcag_criterion="1.3.1 Info and Relationships"
            ))
    
    def _check_semantic_elements(self, code: str):
        """Check for semantic elements in React"""
        if '<main' not in code and '<article' not in code:
            self.issues.append(ValidationIssue(
                rule="semantic_elements",
                severity=SeverityLevel.MODERATE,
                element="semantic",
                description="Missing semantic HTML elements",
                suggestion="Use <main>, <article>, <section>, <nav> elements",
                wcag_criterion="1.3.1 Info and Relationships"
            ))
    
    def _check_keyboard_handlers(self, code: str):
        """Check for keyboard event handlers"""
        if 'onKeyDown' not in code and 'onKeyUp' not in code:
            self.issues.append(ValidationIssue(
                rule="keyboard_handlers",
                severity=SeverityLevel.MINOR,
                element="interactive",
                description="Component may lack full keyboard support",
                suggestion="Add onKeyDown/onKeyUp handlers for Enter/Space keys",
                wcag_criterion="2.1.1 Keyboard"
            ))
    
    def _check_role_attributes(self, code: str):
        """Check for proper role attributes"""
        if 'role="button"' in code and '<button' not in code:
            self.issues.append(ValidationIssue(
                rule="role_attributes",
                severity=SeverityLevel.SERIOUS,
                element="role",
                description="role=\"button\" used without <button> element",
                suggestion="Use native <button> element instead of div with role",
                wcag_criterion="4.1.2 Name, Role, Value"
            ))
    
    def _check_css_contrast(self, css: str):
        """Check CSS for contrast issues"""
        if '#fff' in css.lower() or '#ffffff' in css.lower():
            if '#000' not in css.lower() and '#000000' not in css.lower():
                self.issues.append(ValidationIssue(
                    rule="css_contrast",
                    severity=SeverityLevel.MODERATE,
                    element="css",
                    description="Potential contrast issue - white text without black background check",
                    suggestion="Verify background colors provide sufficient contrast",
                    wcag_criterion="1.4.3 Contrast (Minimum)"
                ))
    
    def _check_focus_styles(self, css: str):
        """Check for focus styles in CSS"""
        if ':focus' not in css:
            self.issues.append(ValidationIssue(
                rule="focus_styles",
                severity=SeverityLevel.SERIOUS,
                element="css",
                description="Missing CSS :focus styles",
                suggestion="Add visible focus indicators with :focus or :focus-visible",
                wcag_criterion="2.4.7 Focus Visible"
            ))
    
    def _check_visibility(self, css: str):
        """Check for visibility issues"""
        if 'display: none' in css or 'visibility: hidden' in css:
            self.issues.append(ValidationIssue(
                rule="visibility",
                severity=SeverityLevel.MINOR,
                element="css",
                description="Hidden elements found - verify they're not needed for a11y",
                suggestion="Ensure hidden elements aren't required for screen readers",
                wcag_criterion="4.1.2 Name, Role, Value"
            ))
    
    def generate_report(self) -> str:
        """Generate human-readable accessibility report"""
        report = "# Accessibility Validation Report\n\n"
        
        if not self.issues:
            report += "✅ No accessibility issues found!\n"
            return report
        
        # Group by severity
        by_severity = {}
        for issue in self.issues:
            if issue.severity not in by_severity:
                by_severity[issue.severity] = []
            by_severity[issue.severity].append(issue)
        
        # Sort by severity
        severity_order = [SeverityLevel.CRITICAL, SeverityLevel.SERIOUS, 
                         SeverityLevel.MODERATE, SeverityLevel.MINOR]
        
        for severity in severity_order:
            if severity in by_severity:
                report += f"\n## {severity.value.upper()} Issues ({len(by_severity[severity])})\n\n"
                for issue in by_severity[severity]:
                    report += f"- **{issue.rule}** (WCAG {issue.wcag_criterion})\n"
                    report += f"  - Element: {issue.element}\n"
                    report += f"  - Issue: {issue.description}\n"
                    report += f"  - Fix: {issue.suggestion}\n\n"
        
        return report
