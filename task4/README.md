# Organize the Mess - Safe File Organization Tool

A Python program that safely identifies, analyzes, and organizes files in messy folders with **zero risk to your originals**.

## Features

✅ **Safe by Design**
- Creates copies in a new folder (originals remain untouched)
- Shows a dry-run preview before any changes
- Requires explicit approval before execution
- Generates detailed reports

✅ **Intelligent Analysis**
- Detects duplicate files by content (MD5 hash)
- Identifies large files (>100 MB)
- Organizes by file type (Documents, Images, Videos, Code, etc.)
- Shows storage recovery opportunities

✅ **User-Friendly**
- Step-by-step approval workflow
- Clear, readable analysis reports
- Progress indicators
- Detailed logging of all operations

## Requirements

- Python 3.7+
- No external dependencies (uses only standard library)

## Installation

1. Clone or download this repository
2. Ensure Python 3.7+ is installed:
   ```bash
   python --version
   ```

## Usage

### Basic Usage

```bash
python organize_mess.py
```

Then enter the path to your messy folder when prompted.

### Command Line Usage

```bash
python organize_mess.py /path/to/messy/folder
```

### Step-by-Step Workflow

1. **Provide Source Folder**
   - Script validates folder access
   - Scans all files recursively

2. **Review Analysis**
   - See file count and total size
   - View files by category
   - Review duplicate groups and large files

3. **Set Output Folder**
   - Where organized copies will go
   - Default: `./organized_files`

4. **Review Dry-Run Plan**
   - See preview of all files to be organized
   - Files organized by category
   - No files are touched at this stage

5. **Approve & Execute**
   - Type "yes" to proceed
   - Files are copied and organized
   - Progress indicators show completion

6. **Review Results**
   - Check the organized folder
   - Read the generated report
   - Decide what to do with originals

## File Categories

Files are automatically organized into these categories:

| Category | Extensions |
|----------|-----------|
| **Documents** | .pdf, .doc, .docx, .txt, .xlsx, .xls, .pptx, .ppt |
| **Images** | .jpg, .jpeg, .png, .gif, .bmp, .svg, .webp, .ico |
| **Videos** | .mp4, .avi, .mkv, .mov, .flv, .wmv, .m4v |
| **Audio** | .mp3, .wav, .flac, .aac, .ogg, .m4a, .wma |
| **Archives** | .zip, .rar, .7z, .tar, .gz, .bz2, .iso |
| **Code** | .py, .js, .ts, .java, .cpp, .c, .go, .rs, .html, .css |
| **Other** | Everything else |

## Example Output

```
╔════════════════════════════════════════════════════════════════╗
║       ORGANIZE THE MESS - Safe File Organization Tool         ║
╚════════════════════════════════════════════════════════════════╝

✓ Folder accessible: /Users/you/Downloads
📁 Scanning folder...
✓ Found 523 files

📊 Analyzing files...

======================================================================
📋 FILE ORGANIZATION ANALYSIS REPORT
======================================================================

📊 SUMMARY:
  Total files: 523
  Total size: 8.5 GB

📂 FILES BY CATEGORY:
  Documents: 156 files (2.1 GB)
  Images: 287 files (5.2 GB)
  Videos: 42 files (0.8 GB)
  Other: 38 files (0.4 GB)

🔄 DUPLICATE FILES (5 groups):
  Recoverable space: 1.2 GB
  
  Group (count=3, 256.0 MB recoverable):
    - old_photo.jpg
    - old_photo (1).jpg
    - Backup/old_photo.jpg
    ... and 0 more

📦 LARGE FILES (>100.0 MB):
  512.0 MB: project_archive.zip
  256.0 MB: video_export.mp4
  ... and 2 more
```

## Generated Report

After organization, a `_organization_report.txt` is created with:
- Source and destination folders
- Statistics (files count, sizes)
- Category breakdown
- Duplicate information
- Large files list
- Success/failure counts

## Safety Tips

1. **Always Review First**
   - Read the dry-run plan completely
   - Check the duplicate groups
   - Verify large files you want to keep

2. **Start with a Test Folder**
   - Try the tool on a small folder first
   - Verify results before using on important data

3. **Keep a Backup**
   - Although originals are never modified
   - Always have backups of important files

4. **Review Duplicates Carefully**
   - Duplicates are detected by content (hash)
   - Same content might have different names
   - Decide which copies to keep/delete

## Customization

To modify file categories, edit the `FILE_CATEGORIES` dictionary in the script:

```python
FILE_CATEGORIES = {
    'Documents': ['.pdf', '.doc', '.docx', ...],
    'Images': ['.jpg', '.png', ...],
    # Add or modify categories here
}
```

To change the large file threshold (currently 100 MB):

```python
LARGE_FILE_THRESHOLD = 100 * 1024 * 1024  # Change this value
```

## Troubleshooting

### "Folder not found" Error
- Check the path is correct
- Use absolute paths (full path from root)
- On Windows: Use forward slashes or raw strings

### Permission Denied
- Ensure you have read access to the folder
- Close any applications using files in the folder
- Run as administrator if needed

### Slow Scanning
- Large folders or slow storage may take time
- The tool calculates hashes to detect duplicates
- Progress updates appear every 50 files

## Advanced Usage

### Dry-Run Without Execution

The script always shows a dry-run first. To cancel:
- Type anything except "yes" when asked for approval
- No files will be modified

### Custom Organize Script

Save the script for future use:

```bash
# Create a shortcut script
echo 'python /path/to/organize_mess.py "$@"' > organize.sh
chmod +x organize.sh
./organize.sh /path/to/folder
```

## FAQ

**Q: Will this delete my files?**
A: No. Files are only copied to a new folder. Originals remain untouched.

**Q: How does duplicate detection work?**
A: Files are compared by MD5 hash (file content). Same content = duplicate, regardless of filename.

**Q: What if there are permission errors?**
A: The script logs errors and continues. Check the report for files that failed.

**Q: Can I run this on network drives?**
A: Yes, but it will be slower. Ensure you have read permissions.

**Q: How do I delete the duplicates after?**
A: Review the report, then manually delete duplicates from the original folder.

## Performance

- Small folders (< 1,000 files): ~10-30 seconds
- Medium folders (1,000-10,000 files): ~1-5 minutes
- Large folders (10,000+ files): ~5-30 minutes

*Times depend on disk speed and file sizes (hash calculation takes time)*

## Example Use Cases

1. **Clean Downloads Folder**
   ```bash
   python organize_mess.py ~/Downloads
   ```

2. **Organize Old Project Folder**
   ```bash
   python organize_mess.py /Volumes/Archive/old_projects
   ```

3. **Find Duplicates Before Backup**
   ```bash
   python organize_mess.py ~/Documents
   ```

## License

MIT License - Use freely for personal or professional projects.

## Support

If you encounter issues:
1. Check the generated report in the output folder
2. Review the error messages in the console
3. Ensure you have adequate disk space
4. Try with a smaller folder first

---

**Remember:** This tool creates copies only. Always review the dry-run plan before approval!
