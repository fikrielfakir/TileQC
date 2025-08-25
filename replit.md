# Overview

This is a comprehensive web-based quality control system for ceramic tile manufacturing, built specifically to monitor and track production parameters across all stages of the ceramic tile production process. The application implements the R2-LABO control plan specifications, managing quality controls from clay preparation through final firing, ensuring compliance with industry standards for ceramic tile production.

The system tracks clay preparation parameters (humidity, granulometry, calcium carbonate), press controls (thickness, weight, surface defects), dryer monitoring (residual humidity), kiln operations (biscuit and email firing), enamel application controls, and various testing procedures including dimensional tests and external laboratory certifications.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Backend Architecture
- **Framework**: Flask (Python) with SQLAlchemy ORM for database operations
- **Database**: SQLite with file-based storage (`ceramic_qc.db`)
- **Authentication**: Flask-Login for user session management with role-based access (controller, quality_manager, admin)
- **Data Models**: Comprehensive models covering all production stages (ClayControl, PressControl, DryerControl, BiscuitKilnControl, EmailKilnControl, etc.)
- **Form Handling**: WTForms with custom validation for quality parameter ranges
- **Route Organization**: Modular blueprint structure separating concerns by production stage

## Frontend Architecture
- **Template Engine**: Jinja2 with Bootstrap 5 for responsive UI
- **Styling**: Custom CSS with manufacturing-specific color schemes and component styling
- **JavaScript**: Vanilla JavaScript with Chart.js for analytics and real-time form validation
- **User Interface**: Dashboard-centric design with stage-specific control panels and comprehensive reporting

## Data Storage Design
- **Primary Database**: SQLite with declarative base models
- **Relationships**: User-linked quality control records with foreign key constraints
- **Validation Logic**: Built-in compliance checking against specification limits
- **Data Integrity**: Automatic compliance status calculation and metadata tracking

## Authentication System
- **User Management**: Role-based system with three levels (controller, quality_manager, admin)
- **Session Handling**: Flask-Login with secure session management
- **Password Security**: Werkzeug password hashing
- **Access Control**: Login required decorators with role-based route protection

## Quality Control Validation
- **Specification Engine**: Automated compliance checking against R2-LABO standards
- **Real-time Validation**: Client-side and server-side parameter validation
- **Status Tracking**: Automatic compliance status assignment (compliant, non_compliant, partial)
- **Defect Analysis**: Surface defect percentage tracking with configurable limits

## Reporting and Analytics
- **Dashboard System**: Real-time quality metrics and trend analysis
- **Statistical Analysis**: Helper functions for dashboard statistics and trend data
- **Export Functionality**: Daily, weekly, and monthly report generation
- **Charts and Visualization**: Chart.js integration for compliance trends and defect analysis

# External Dependencies

- **Flask Framework**: Core web framework with extensions (Flask-SQLAlchemy, Flask-Login, Flask-WTF)
- **Bootstrap 5**: Frontend CSS framework for responsive design
- **Chart.js**: JavaScript charting library for analytics visualization
- **Bootstrap Icons**: Icon library for UI elements
- **WTForms**: Form handling and validation library
- **Werkzeug**: WSGI utilities including password hashing and security middleware
- **SQLAlchemy**: Database ORM with declarative base for model definitions
- **Python Standard Libraries**: datetime, os, logging, json for core functionality

The application is designed for deployment on Replit with SQLite as the primary database, though the architecture supports migration to PostgreSQL for production environments through minimal configuration changes.