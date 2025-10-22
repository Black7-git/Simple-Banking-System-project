#!/usr/bin/env python
"""
Verification script to check if PetRescue is properly set up
"""

import os
import sys

def check_file(filepath, description):
    """Check if a file exists"""
    if os.path.exists(filepath):
        print(f"✓ {description}: Found")
        return True
    else:
        print(f"✗ {description}: Missing")
        return False

def check_directory(dirpath, description):
    """Check if a directory exists"""
    if os.path.isdir(dirpath):
        print(f"✓ {description}: Found")
        return True
    else:
        print(f"✗ {description}: Missing")
        return False

def main():
    print("="*60)
    print("PetRescue Setup Verification")
    print("="*60)
    print()
    
    errors = []
    
    # Check Python version
    print("Checking Python Version...")
    py_version = sys.version_info
    if py_version >= (3, 8):
        print(f"✓ Python {py_version.major}.{py_version.minor}.{py_version.micro}")
    else:
        print(f"✗ Python version {py_version.major}.{py_version.minor} (3.8+ required)")
        errors.append("Python version")
    print()
    
    # Check core files
    print("Checking Core Files...")
    core_files = [
        ("manage.py", "Django management script"),
        ("requirements.txt", "Dependencies file"),
        ("petrescue/settings.py", "Django settings"),
        ("petrescue/urls.py", "Main URL configuration"),
        ("pets/models.py", "Database models"),
        ("pets/views.py", "View functions"),
        ("pets/forms.py", "Form definitions"),
        ("pets/urls.py", "App URLs"),
    ]
    
    for filepath, description in core_files:
        if not check_file(filepath, description):
            errors.append(filepath)
    print()
    
    # Check directories
    print("Checking Directories...")
    directories = [
        ("petrescue", "Project configuration"),
        ("pets", "Main application"),
        ("pets/templates", "Templates directory"),
        ("pets/templates/pets", "Pet templates"),
        ("pets/static", "Static files"),
        ("pets/static/css", "CSS directory"),
        ("media", "Media files"),
        ("media/pet_photos", "Pet photos"),
    ]
    
    for dirpath, description in directories:
        if not check_directory(dirpath, description):
            errors.append(dirpath)
    print()
    
    # Check templates
    print("Checking Templates...")
    templates = [
        "pets/templates/pets/base.html",
        "pets/templates/pets/home.html",
        "pets/templates/pets/login.html",
        "pets/templates/pets/register.html",
        "pets/templates/pets/pet_list.html",
        "pets/templates/pets/pet_detail.html",
        "pets/templates/pets/report_pet.html",
    ]
    
    for template in templates:
        if not check_file(template, os.path.basename(template)):
            errors.append(template)
    print()
    
    # Check static files
    print("Checking Static Files...")
    if not check_file("pets/static/css/style.css", "Main stylesheet"):
        errors.append("style.css")
    print()
    
    # Check documentation
    print("Checking Documentation...")
    docs = [
        ("README.md", "Main documentation"),
        ("INSTALLATION.md", "Installation guide"),
        ("QUICK_START.md", "Quick start guide"),
        ("TESTING.md", "Testing guide"),
        ("PROJECT_STRUCTURE.md", "Project structure"),
    ]
    
    for filepath, description in docs:
        if not check_file(filepath, description):
            errors.append(filepath)
    print()
    
    # Try importing Django
    print("Checking Django Installation...")
    try:
        import django
        print(f"✓ Django {django.get_version()} installed")
    except ImportError:
        print("✗ Django not installed")
        errors.append("Django")
    print()
    
    # Summary
    print("="*60)
    if errors:
        print(f"ISSUES FOUND: {len(errors)} item(s) need attention")
        print("\nMissing items:")
        for error in errors:
            print(f"  - {error}")
        print("\nPlease run: pip install -r requirements.txt")
        print("Or see INSTALLATION.md for detailed setup instructions")
    else:
        print("✓ ALL CHECKS PASSED!")
        print("\nYour PetRescue installation looks good!")
        print("\nNext steps:")
        print("1. Run migrations: python manage.py migrate")
        print("2. Create superuser: python manage.py createsuperuser")
        print("3. Start server: python manage.py runserver")
        print("\nSee QUICK_START.md for detailed instructions")
    print("="*60)
    
    return len(errors) == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
