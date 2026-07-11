# Configuration Examples

Customize the `organize_mess.py` script for your specific needs.

## Default Configuration

The script comes pre-configured with common file types. You can modify the following:

### 1. File Categories

**Location:** Line 12-20 in `organize_mess.py`

```python
FILE_CATEGORIES = {
    'Documents': ['.pdf', '.doc', '.docx', '.txt', '.xlsx', '.xls', '.pptx', '.ppt'],
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', '.ico'],
    'Videos': ['.mp4', '.avi', '.mkv', '.mov', '.flv', '.wmv', '.m4v'],
    'Audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a', '.wma'],
    'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.iso'],
    'Code': ['.py', '.js', '.ts', '.java', '.cpp', '.c', '.go', '.rs', '.html', '.css'],
    'Other': []
}
```

### 2. Large File Threshold

**Location:** Line 21 in `organize_mess.py`

```python
LARGE_FILE_THRESHOLD = 100 * 1024 * 1024  # 100 MB
```

---

## Common Customizations

### Example 1: Photography Workflow

If you're a photographer, organize by purpose instead of generic types:

```python
FILE_CATEGORIES = {
    'RAW_Originals': ['.raw', '.cr2', '.nef', '.dng'],
    'Edited': ['.jpg', '.png', '.tiff'],
    'Projects': ['.psd', '.xcf', '.ai'],
    'Exports': ['.mp4', '.mov'],
    'Backups': ['.zip', '.rar'],
    'Other': []
}
```

### Example 2: Development Environment

For developers working on multiple projects:

```python
FILE_CATEGORIES = {
    'Source Code': ['.py', '.js', '.ts', '.java', '.cpp', '.c', '.go', '.rs', '.rb', '.php'],
    'Web Assets': ['.html', '.css', '.scss', '.sass', '.less', '.jsx', '.tsx'],
    'Configuration': ['.json', '.yaml', '.yml', '.toml', '.xml', '.ini'],
    'Documentation': ['.md', '.pdf', '.txt', '.rst'],
    'Libraries': ['.jar', '.dll', '.so', '.dylib'],
    'Build Artifacts': ['.o', '.a', '.lib', '.exe', '.app'],
    'Other': []
}
```

### Example 3: Media Production

For video/audio editing:

```python
FILE_CATEGORIES = {
    'Video_Raw': ['.mts', '.mov', '.avi', '.r3d'],
    'Video_Edited': ['.mp4', '.mkv', '.webm'],
    'Audio_Raw': ['.wav', '.aiff'],
    'Audio_Mixed': ['.mp3', '.flac', '.aac'],
    'Project_Files': ['.prproj', '.aep', '.fcpxml'],
    'Graphics': ['.psd', '.png', '.svg'],
    'Archives': ['.zip', '.rar', '.7z'],
    'Other': []
}
```

### Example 4: Academic/Research

```python
FILE_CATEGORIES = {
    'Papers': ['.pdf', '.epub'],
    'Manuscripts': ['.docx', '.doc', '.txt'],
    'Data': ['.csv', '.xlsx', '.json'],
    'Analysis': ['.py', '.r', '.m'],
    'Presentations': ['.pptx', '.ppt'],
    'Notes': ['.md', '.odt'],
    'Citations': ['.bib', '.ris'],
    'Other': []
}
```

### Example 5: Small Business Files

```python
FILE_CATEGORIES = {
    'Invoices': ['.pdf', '.xlsx'],
    'Contracts': ['.pdf', '.docx'],
    'Records': ['.csv', '.xlsx'],
    'Marketing': ['.png', '.jpg', '.psd'],
    'Presentations': ['.pptx'],
    'Backups': ['.zip', '.rar'],
    'Other': []
}
```

---

## Adjusting Thresholds

### Sensitive to Storage

Flag files larger than 50 MB:

```python
LARGE_FILE_THRESHOLD = 50 * 1024 * 1024  # 50 MB
```

### Lenient (Only huge files)

Only flag files over 500 MB:

```python
LARGE_FILE_THRESHOLD = 500 * 1024 * 1024  # 500 MB
```

---

## Performance Tuning

### Skip Hash Calculation (Faster, no duplicate detection)

Modify the `calculate_file_hash()` method:

```python
def calculate_file_hash(self, filepath, chunk_size=8192):
    # Skip hash calculation for speed
    return None  # Won't detect duplicates, but much faster
```

### Only Hash Files Under 100 MB

```python
def calculate_file_hash(self, filepath, chunk_size=8192):
    if filepath.stat().st_size > 100 * 1024 * 1024:
        return None  # Skip hashing large files
    
    hasher = hashlib.md5()
    # ... rest of method
```

### Increase Hash Chunk Size (Faster hashing)

```python
def calculate_file_hash(self, filepath, chunk_size=65536):  # Larger chunks
    # This reads more bytes at once, faster but uses more memory
    # ...
```

---

## Output Customization

### Change Default Output Folder

**Location:** Near line 240 in `organize_mess.py`

```python
# Change this:
output_folder = input("Output path [./organized_files]: ").strip() or "./organized_files"

# To this:
output_folder = input("Output path [~/Desktop/Organized]: ").strip() or "~/Desktop/Organized"
```

### Modify Folder Naming

Change how subdirectories are named:

```python
# Current (uses category name):
dest_folder = Path(output_folder) / category

# Alternative (use date-based):
from datetime import datetime
dest_folder = Path(output_folder) / datetime.now().strftime("%Y-%m-%d") / category

# Alternative (use size-based):
size_category = "Small" if file_info['size'] < 1000000 else "Large"
dest_folder = Path(output_folder) / size_category / category
```

---

## Advanced: Custom Organization Logic

### Organize by Date Modified

Add this to the `generate_organization_plan()` method:

```python
import datetime

def generate_organization_plan(self, output_folder):
    operations = []
    
    for file_info in self.all_files:
        source = file_info['path']
        mtime = datetime.datetime.fromtimestamp(source.stat().st_mtime)
        
        # Organize by year/month
        dest_folder = Path(output_folder) / mtime.strftime("%Y") / mtime.strftime("%B")
        destination = dest_folder / file_info['name']
        
        operations.append({
            'type': 'copy',
            'source': str(source),
            'destination': str(destination),
            'source_rel': str(file_info['relative_path']),
            'category': mtime.strftime("%Y-%m"),
            'size': file_info['size']
        })
    
    return operations
```

### Organize by Size Groups

```python
def get_size_category(self, size):
    if size < 1 * 1024 * 1024:
        return "Small (< 1 MB)"
    elif size < 50 * 1024 * 1024:
        return "Medium (1-50 MB)"
    elif size < 500 * 1024 * 1024:
        return "Large (50-500 MB)"
    else:
        return "Huge (> 500 MB)"
```

### Organize by Name Pattern

```python
def get_name_category(self, filename):
    """Organize by first letter of filename."""
    first_letter = filename[0].upper()
    if first_letter.isalpha():
        return first_letter
    elif first_letter.isdigit():
        return "0-9"
    else:
        return "Symbols"
```

---

## Integration Examples

### PowerShell Wrapper (Windows)

Create `organize.ps1`:

```powershell
param(
    [string]$FolderPath = (Read-Host "Enter folder path"),
    [string]$OutputPath = "./organized_files"
)

python organize_mess.py $FolderPath
```

Usage:
```powershell
.\organize.ps1 C:\Users\You\Downloads
```

### Bash Wrapper (Linux/Mac)

Create `organize.sh`:

```bash
#!/bin/bash

if [ -z "$1" ]; then
    read -p "Enter folder path: " folder
else
    folder=$1
fi

python3 organize_mess.py "$folder"
```

Usage:
```bash
chmod +x organize.sh
./organize.sh ~/Downloads
```

---

## Safe Testing

Before modifying the script:

1. **Make a backup copy:**
   ```bash
   cp organize_mess.py organize_mess.py.backup
   ```

2. **Test with the test folder:**
   ```bash
   python create_test_folder.py
   python organize_mess.py test_messy_folder
   ```

3. **Review results:**
   ```bash
   ls -la organized_files/
   cat organized_files/_organization_report.txt
   ```

4. **Keep the backup** in case you want to revert

---

## Debugging Customizations

To debug your changes:

```python
# Add print statements
print(f"DEBUG: Processing {file_info['name']}")
print(f"DEBUG: Category determined: {category}")

# Or save debug info to file
with open("debug_log.txt", "a") as f:
    f.write(f"{file_info['name']} -> {category}\n")
```

---

## Performance Comparison

| Configuration | Speed | Features |
|--------------|-------|----------|
| Default | 1x | Full analysis, duplicates, large files |
| No hashing | 5x-10x | Fast, but no duplicate detection |
| Skip large files | 2x | Faster, but misses some duplicates |
| Custom categories | 1x | Same speed, better organization |

---

## Recommendations

**For most users:**
- Keep default categories
- Keep default threshold (100 MB)
- Test with test folder first

**For large folders (10k+ files):**
- Consider skipping hash for large files
- Increase chunk size for faster hashing

**For specific domains:**
- Customize categories to your use case
- Test thoroughly before running on real data

**For integration:**
- Create wrapper scripts (PS/Bash)
- Add to scheduled tasks/cron jobs
- Document your customizations

---

Need help? Review the README.md or examine the code comments in organize_mess.py.
