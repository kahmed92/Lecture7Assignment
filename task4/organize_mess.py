#!/usr/bin/env python3
"""
Organize the Mess - Safe File Organization Tool
Safely identifies and organizes files with user approval before any changes.
"""

import os
import sys
import shutil
import hashlib
from pathlib import Path
from collections import defaultdict
from datetime import datetime
import json

class FileOrganizer:
    """Safely organize messy folders with dry-run preview."""

    FILE_CATEGORIES = {
        'Documents': ['.pdf', '.doc', '.docx', '.txt', '.xlsx', '.xls', '.pptx', '.ppt'],
        'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', '.ico'],
        'Videos': ['.mp4', '.avi', '.mkv', '.mov', '.flv', '.wmv', '.m4v'],
        'Audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a', '.wma'],
        'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.iso'],
        'Code': ['.py', '.js', '.ts', '.java', '.cpp', '.c', '.go', '.rs', '.html', '.css'],
        'Other': []
    }

    LARGE_FILE_THRESHOLD = 100 * 1024 * 1024  # 100 MB

    def __init__(self, source_folder):
        self.source_folder = Path(source_folder)
        self.files_by_hash = defaultdict(list)
        self.files_by_size = defaultdict(list)
        self.files_by_type = defaultdict(list)
        self.all_files = []

    def validate_folder(self):
        """Check if folder exists and is accessible."""
        if not self.source_folder.exists():
            raise FileNotFoundError(f"Folder not found: {self.source_folder}")
        if not self.source_folder.is_dir():
            raise NotADirectoryError(f"Not a directory: {self.source_folder}")
        if not os.access(self.source_folder, os.R_OK):
            raise PermissionError(f"Cannot read folder: {self.source_folder}")
        print(f"✓ Folder accessible: {self.source_folder}")

    def get_file_category(self, filepath):
        """Determine category based on file extension."""
        ext = Path(filepath).suffix.lower()
        for category, extensions in self.FILE_CATEGORIES.items():
            if ext in extensions:
                return category
        return 'Other'

    def calculate_file_hash(self, filepath, chunk_size=8192):
        """Calculate MD5 hash of file for duplicate detection."""
        hasher = hashlib.md5()
        try:
            with open(filepath, 'rb') as f:
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    hasher.update(chunk)
            return hasher.hexdigest()
        except Exception as e:
            return None

    def scan_folder(self):
        """Scan folder and categorize files."""
        print("\n📁 Scanning folder...")

        for filepath in self.source_folder.rglob('*'):
            if filepath.is_file():
                try:
                    size = filepath.stat().st_size
                    file_hash = self.calculate_file_hash(filepath)
                    category = self.get_file_category(filepath)

                    file_info = {
                        'path': filepath,
                        'name': filepath.name,
                        'size': size,
                        'hash': file_hash,
                        'category': category,
                        'relative_path': filepath.relative_to(self.source_folder)
                    }

                    self.all_files.append(file_info)
                    self.files_by_type[category].append(file_info)

                    if file_hash:
                        self.files_by_hash[file_hash].append(file_info)
                    self.files_by_size[size].append(file_info)

                except Exception as e:
                    print(f"  ⚠️  Error processing {filepath}: {e}")

        print(f"✓ Found {len(self.all_files)} files")

    def analyze_files(self):
        """Analyze files for duplicates, large files, and organization."""
        print("\n📊 Analyzing files...")

        analysis = {
            'total_files': len(self.all_files),
            'total_size': sum(f['size'] for f in self.all_files),
            'by_category': {},
            'duplicates': [],
            'large_files': []
        }

        # Category analysis
        for category, files in self.files_by_type.items():
            if files:
                analysis['by_category'][category] = {
                    'count': len(files),
                    'size': sum(f['size'] for f in files)
                }

        # Find duplicates by content hash
        for file_hash, files in self.files_by_hash.items():
            if len(files) > 1 and file_hash:  # More than one file with same hash
                duplicates = {
                    'hash': file_hash,
                    'count': len(files),
                    'size_per_file': files[0]['size'],
                    'total_duplicate_size': files[0]['size'] * (len(files) - 1),
                    'files': [str(f['relative_path']) for f in files]
                }
                analysis['duplicates'].append(duplicates)

        # Find large files
        for file_info in self.all_files:
            if file_info['size'] > self.LARGE_FILE_THRESHOLD:
                analysis['large_files'].append({
                    'name': file_info['name'],
                    'path': str(file_info['relative_path']),
                    'size': file_info['size']
                })

        analysis['duplicates'].sort(key=lambda x: x['total_duplicate_size'], reverse=True)
        analysis['large_files'].sort(key=lambda x: x['size'], reverse=True)

        return analysis

    def format_size(self, size):
        """Format bytes to human-readable size."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"

    def print_analysis(self, analysis):
        """Print analysis report."""
        print("\n" + "="*70)
        print("📋 FILE ORGANIZATION ANALYSIS REPORT")
        print("="*70)

        # Summary
        print(f"\n📊 SUMMARY:")
        print(f"  Total files: {analysis['total_files']}")
        print(f"  Total size: {self.format_size(analysis['total_size'])}")

        # By category
        print(f"\n📂 FILES BY CATEGORY:")
        for category, info in sorted(analysis['by_category'].items()):
            print(f"  {category}: {info['count']} files ({self.format_size(info['size'])})")

        # Duplicates
        if analysis['duplicates']:
            print(f"\n🔄 DUPLICATE FILES ({len(analysis['duplicates'])} groups):")
            recoverable_size = sum(d['total_duplicate_size'] for d in analysis['duplicates'])
            print(f"  Recoverable space: {self.format_size(recoverable_size)}")
            for dup in analysis['duplicates'][:10]:  # Show top 10
                print(f"\n  Group (count={dup['count']}, {self.format_size(dup['total_duplicate_size'])} recoverable):")
                for filepath in dup['files'][:3]:
                    print(f"    - {filepath}")
                if len(dup['files']) > 3:
                    print(f"    ... and {len(dup['files']) - 3} more")
            if len(analysis['duplicates']) > 10:
                print(f"\n  ... and {len(analysis['duplicates']) - 10} more duplicate groups")

        # Large files
        if analysis['large_files']:
            print(f"\n📦 LARGE FILES (>{self.format_size(self.LARGE_FILE_THRESHOLD)}):")
            for large_file in analysis['large_files'][:10]:
                print(f"  {self.format_size(large_file['size'])}: {large_file['path']}")
            if len(analysis['large_files']) > 10:
                print(f"\n  ... and {len(analysis['large_files']) - 10} more")

        print("\n" + "="*70)

    def generate_organization_plan(self, output_folder):
        """Generate a plan to organize files."""
        print(f"\n📋 GENERATING ORGANIZATION PLAN...")

        operations = []

        for file_info in self.all_files:
            category = file_info['category']
            source = file_info['path']
            dest_folder = Path(output_folder) / category
            destination = dest_folder / file_info['name']

            # Avoid overwriting files in same folder
            if source != destination:
                operations.append({
                    'type': 'copy',
                    'source': str(source),
                    'destination': str(destination),
                    'source_rel': str(file_info['relative_path']),
                    'category': category,
                    'size': file_info['size']
                })

        return operations

    def print_dry_run(self, operations):
        """Print a detailed dry-run preview."""
        print("\n" + "="*70)
        print("🔍 DRY RUN PREVIEW - FILES THAT WOULD BE ORGANIZED")
        print("="*70)

        by_category = defaultdict(list)
        for op in operations:
            by_category[op['category']].append(op)

        total_operations = 0
        for category in sorted(by_category.keys()):
            ops = by_category[category]
            print(f"\n📂 {category}: ({len(ops)} files)")
            for op in sorted(ops, key=lambda x: x['size'], reverse=True)[:5]:
                print(f"  ✓ {op['source_rel']}")
                print(f"    → {op['category']}/{op['destination'].split(os.sep)[-1]}")
                print(f"    Size: {self.format_size(op['size'])}")
            if len(ops) > 5:
                print(f"  ... and {len(ops) - 5} more files")
            total_operations += len(ops)

        print("\n" + "-"*70)
        print(f"Total operations: {total_operations} files to organize")
        print("All files will be COPIED (originals remain untouched)")
        print("="*70)

    def execute_organization(self, operations, output_folder):
        """Execute the organization plan."""
        print(f"\n⏳ Organizing files...")

        success_count = 0
        error_count = 0

        for i, op in enumerate(operations, 1):
            try:
                dest_path = Path(op['destination'])
                dest_path.parent.mkdir(parents=True, exist_ok=True)

                shutil.copy2(op['source'], op['destination'])
                success_count += 1

                if i % 50 == 0:
                    print(f"  Progress: {i}/{len(operations)}")

            except Exception as e:
                print(f"  ❌ Error copying {op['source']}: {e}")
                error_count += 1

        print(f"\n✓ Completed: {success_count} files organized")
        if error_count > 0:
            print(f"⚠️  Errors: {error_count} files failed")

        return success_count, error_count

    def generate_report(self, output_folder, analysis, operations, success_count, error_count):
        """Generate a detailed report file."""
        report_path = Path(output_folder) / "_organization_report.txt"

        with open(report_path, 'w') as f:
            f.write("="*70 + "\n")
            f.write("FILE ORGANIZATION REPORT\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*70 + "\n\n")

            f.write("SOURCE FOLDER:\n")
            f.write(f"  {self.source_folder}\n\n")

            f.write("DESTINATION FOLDER:\n")
            f.write(f"  {output_folder}\n\n")

            f.write("SUMMARY:\n")
            f.write(f"  Total files found: {analysis['total_files']}\n")
            f.write(f"  Total size: {self.format_size(analysis['total_size'])}\n")
            f.write(f"  Successfully organized: {success_count}\n")
            f.write(f"  Failed operations: {error_count}\n\n")

            f.write("ORGANIZATION BY CATEGORY:\n")
            for category, info in sorted(analysis['by_category'].items()):
                f.write(f"  {category}: {info['count']} files ({self.format_size(info['size'])})\n")

            if analysis['duplicates']:
                f.write(f"\nDUPLICATES FOUND:\n")
                recoverable = sum(d['total_duplicate_size'] for d in analysis['duplicates'])
                f.write(f"  Total groups: {len(analysis['duplicates'])}\n")
                f.write(f"  Recoverable space: {self.format_size(recoverable)}\n")

            if analysis['large_files']:
                f.write(f"\nLARGE FILES (>{self.format_size(self.LARGE_FILE_THRESHOLD)}):\n")
                f.write(f"  Count: {len(analysis['large_files'])}\n")

        return report_path

def main():
    """Main entry point."""
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║       ORGANIZE THE MESS - Safe File Organization Tool         ║")
    print("╚════════════════════════════════════════════════════════════════╝")

    # Get source folder
    if len(sys.argv) > 1:
        source_folder = sys.argv[1]
    else:
        print("\n📁 Enter the path to the messy folder:")
        source_folder = input("Path: ").strip()

    if not source_folder:
        print("❌ No folder specified. Exiting.")
        return

    # Initialize organizer
    try:
        organizer = FileOrganizer(source_folder)
        organizer.validate_folder()
    except Exception as e:
        print(f"❌ Error: {e}")
        return

    # Scan and analyze
    organizer.scan_folder()
    analysis = organizer.analyze_files()
    organizer.print_analysis(analysis)

    # Get output folder
    print("\n📂 Enter output folder for organized files:")
    print("   (This creates a new folder with organized copies - originals stay untouched)")
    output_folder = input("Output path [./organized_files]: ").strip() or "./organized_files"

    # Generate plan
    operations = organizer.generate_organization_plan(output_folder)
    organizer.print_dry_run(operations)

    # Request approval
    print("\n⚠️  REVIEW THE PLAN ABOVE CAREFULLY")
    print("\nDo you approve this organization plan?")
    approval = input("Type 'yes' to proceed, or anything else to cancel: ").strip().lower()

    if approval != 'yes':
        print("\n❌ Operation cancelled. No files were modified.")
        return

    # Execute
    print("\n🔄 Starting file organization...")
    print(f"   Source: {organizer.source_folder}")
    print(f"   Output: {output_folder}")

    success_count, error_count = organizer.execute_organization(operations, output_folder)

    # Generate report
    report_path = organizer.generate_report(output_folder, analysis, operations, success_count, error_count)

    # Summary
    print("\n" + "="*70)
    print("✓ ORGANIZATION COMPLETE")
    print("="*70)
    print(f"\n📊 Results:")
    print(f"  Organized folder: {output_folder}")
    print(f"  Files organized: {success_count}")
    if error_count > 0:
        print(f"  Errors: {error_count}")
    print(f"  Report saved: {report_path}")
    print(f"\n📋 Next steps:")
    print(f"  1. Review the organized files in: {output_folder}")
    print(f"  2. Check the report: {report_path}")
    print(f"  3. Delete duplicates from original folder if desired")
    print(f"  4. Backup the script for future use")

    print("\n" + "="*70)

if __name__ == "__main__":
    main()
