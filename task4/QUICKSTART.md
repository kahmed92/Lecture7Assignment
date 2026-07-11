# Quick Start Guide

Get started with Organize the Mess in 5 minutes.

## Step 1: Verify Python

Check Python is installed:

```bash
python --version
```

You need Python 3.7 or higher.

## Step 2: Run the Tool

### Option A: Interactive Mode (Recommended for first-time)

```bash
python organize_mess.py
```

Then follow the prompts:
1. Enter your messy folder path
2. Enter output folder (or press Enter for default)
3. Review the analysis and dry-run plan
4. Type "yes" to proceed

### Option B: Command Line Mode

```bash
python organize_mess.py /path/to/your/messy/folder
```

## Step 3: Understand the Output

The tool shows you:

1. **File Summary**
   - Total files found
   - Total storage used
   - Files by category

2. **Analysis**
   - Duplicate groups with recoverable space
   - Large files (>100 MB)
   - Warning about what will be organized

3. **Dry-Run Preview**
   - List of ALL files that will be organized
   - Where each file will go
   - NO files are actually moved yet

4. **Approval Request**
   - Read the plan carefully
   - Type "yes" only if you approve
   - Type anything else to cancel

## Step 4: Review Results

After running, check:

1. The new `organized_files` folder (or your custom output folder)
2. The `_organization_report.txt` for detailed stats
3. Original files remain untouched in the source folder

## Step 5: Next Actions

Once you're confident:

1. **Keep the organized copy** if you like the structure
2. **Delete duplicates** from the original folder (AFTER verifying)
3. **Backup important files** before deleting anything
4. **Save the script** for future use

---

## Example Walkthrough

### Setup: Create Test Folder

```bash
# Create a test folder with some files
mkdir test_messy_folder
cd test_messy_folder

# Create some sample files (Linux/Mac)
touch document.pdf report.docx presentation.pptx
touch photo1.jpg photo2.jpg photo1.jpg  # duplicate!
touch video.mp4 audio.mp3
touch script.py data.json
```

### Run the Tool

```bash
python organize_mess.py ./test_messy_folder
```

### Review Output

The tool will:
1. Find all files
2. Detect the duplicate photo
3. Organize by type (Documents, Images, Videos, Audio, Code)
4. Show dry-run with all operations
5. Wait for your approval

### Approve

When asked "Do you approve this organization plan?", type:
```
yes
```

### Check Results

```bash
ls -la organized_files/
# You'll see:
# Documents/
# Images/
# Videos/
# Audio/
# Code/
# _organization_report.txt
```

---

## Common Scenarios

### Scenario 1: Clean Downloads Folder

```bash
python organize_mess.py ~/Downloads
```

**Expected:** Find old installers, documents, screenshots
**Action:** Review, approve, then delete old files from Downloads

### Scenario 2: Find Duplicates

```bash
python organize_mess.py ~/Documents
```

**Expected:** Identify identical files with different names
**Action:** Review report, then delete duplicate copies from original

### Scenario 3: Organize Project Folder

```bash
python organize_mess.py /path/to/old/project
```

**Expected:** Group scattered assets by type
**Action:** Use the organized structure as reference for cleanup

---

## Safety Checklist

Before running on important folders:

- [ ] You have a recent backup of the folder
- [ ] No applications are actively using files in the folder
- [ ] You'll review the dry-run plan before approval
- [ ] You understand duplicates will be copied (not deleted)
- [ ] You have enough disk space for copies

---

## Customizing File Categories

Want to add a custom category? Edit the script:

```python
FILE_CATEGORIES = {
    'Documents': ['.pdf', '.doc', '.docx', '.txt', '.xlsx'],
    'Images': ['.jpg', '.png', '.gif', '.svg'],
    'Videos': ['.mp4', '.avi', '.mkv'],
    'Audio': ['.mp3', '.wav', '.flac'],
    'Archives': ['.zip', '.rar', '.7z'],
    'Code': ['.py', '.js', '.java'],
    'MyCustomType': ['.xyz', '.custom'],  # Add your own!
    'Other': []
}
```

---

## Troubleshooting

### "Folder not found"
- Use full paths (e.g., `C:\Users\You\Downloads` on Windows)
- Check path spelling

### "Permission denied"
- Close apps accessing the folder
- Run as administrator if needed
- Check folder permissions

### Script is slow
- Large folders take time (hashing files takes time)
- Let it finish (progress updates every 50 files)
- Try a smaller folder first

### Don't see expected files
- Might be hidden files (script finds all files)
- Check report for error logs
- Verify folder path is correct

---

## Next Steps

1. **Try a small folder first** to get comfortable
2. **Review the main README.md** for detailed docs
3. **Keep the script handy** for regular cleanup
4. **Share with others** who need file organization

---

Need help? Check the README.md or review the code comments in organize_mess.py.
