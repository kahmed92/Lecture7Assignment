#!/usr/bin/env python3
"""
Create a sample messy folder for testing organize_mess.py
This safely creates a test environment without affecting real files.
"""

import os
from pathlib import Path
import random

def create_test_folder(folder_name="test_messy_folder"):
    """Create a test folder with sample files."""

    test_dir = Path(folder_name)
    test_dir.mkdir(exist_ok=True)

    print(f"📁 Creating test folder: {test_dir}")

    # Sample document content
    doc_content = "This is a sample document for testing.\n" * 50
    image_content = b"FAKE_IMAGE_DATA" * 1000
    code_content = """
def hello_world():
    print("Hello, World!")

if __name__ == "__main__":
    hello_world()
"""

    # Create various files
    files_created = []

    # Documents
    (test_dir / "document1.txt").write_text(doc_content)
    files_created.append("document1.txt")

    (test_dir / "report.txt").write_text(doc_content)
    files_created.append("report.txt")

    (test_dir / "notes.txt").write_text(doc_content)  # Duplicate content!
    files_created.append("notes.txt")

    # Images
    (test_dir / "photo1.jpg").write_bytes(image_content)
    files_created.append("photo1.jpg")

    (test_dir / "photo2.jpg").write_bytes(image_content)  # Duplicate!
    files_created.append("photo2.jpg")

    (test_dir / "screenshot.png").write_bytes(image_content + b"_PNG")
    files_created.append("screenshot.png")

    # Code
    (test_dir / "script.py").write_text(code_content)
    files_created.append("script.py")

    (test_dir / "main.py").write_text(code_content)  # Duplicate!
    files_created.append("main.py")

    # Create nested subdirectory with more files
    subdir = test_dir / "old_stuff"
    subdir.mkdir(exist_ok=True)

    (subdir / "backup_photo.jpg").write_bytes(image_content)  # Another duplicate!
    files_created.append("old_stuff/backup_photo.jpg")

    (subdir / "archive.txt").write_text(doc_content + "\nArchived version")
    files_created.append("old_stuff/archive.txt")

    # Large file (simulate)
    large_content = "x" * (50 * 1024 * 1024)  # 50 MB
    large_file = test_dir / "large_file.bin"
    with open(large_file, 'w') as f:
        f.write(large_content)
    files_created.append("large_file.bin")

    # Create a few more miscellaneous files
    (test_dir / "config.json").write_text('{"key": "value"}')
    files_created.append("config.json")

    (test_dir / "data.csv").write_text("name,age\nAlice,30\nBob,25\n")
    files_created.append("data.csv")

    (test_dir / "music.mp3").write_bytes(b"FAKE_AUDIO_DATA" * 100)
    files_created.append("music.mp3")

    print(f"\n✅ Test folder created with {len(files_created)} files:")
    for f in sorted(files_created):
        print(f"  - {f}")

    print(f"\n📊 Test folder includes:")
    print(f"  • Documents: {len([f for f in files_created if f.endswith(('.txt', '.csv', '.json'))])}")
    print(f"  • Images: {len([f for f in files_created if f.endswith(('.jpg', '.png'))])}")
    print(f"  • Code: {len([f for f in files_created if f.endswith('.py')])}")
    print(f"  • Audio: {len([f for f in files_created if f.endswith('.mp3')])}")
    print(f"  • Duplicates: 3 groups (photo, code, document)")
    print(f"  • Large file: 50 MB")

    print(f"\n🧪 Now you can test the organizer:")
    print(f"   python organize_mess.py {test_dir}")

    return test_dir

if __name__ == "__main__":
    try:
        test_folder = create_test_folder()
        print(f"\n✓ Ready to organize! Run: python organize_mess.py {test_folder}")
    except Exception as e:
        print(f"❌ Error: {e}")
