import argparse
from datetime import datetime
import nbformat
from nbformat import v4 as nbf
import os


def create_log(date_str, output_dir):
    title_cell = f"# 📅 Date: {date_str}"

    template_cells = [
        nbf.new_markdown_cell(title_cell),
        nbf.new_markdown_cell(
            """## 🔍 Focus Area
- (e.g., Arrays, Sliding Window, Binary Search)
"""
        ),
        nbf.new_markdown_cell(
            """## ✅ Tasks Completed
- [ ] Problem 1: <Name> ([Link](#))
"""
        ),
        nbf.new_markdown_cell(
            """## 📈 Progress Tracker
| Problem | Status | Date | Notes |
|---------|--------|------|-------|
| <Name>  | ⬜/✅   | <Date> | <Notes> |
"""
        ),
        nbf.new_markdown_cell(
            """## 🧪 Code Experiments
"""
        ),
        nbf.new_markdown_cell(
            """### Problem 1: <Name>
<Problem description here>
"""
        ),
        nbf.new_markdown_cell(
            """#### Solution Walkthrough
1. <Step 1>
2. <Step 2>
3. <Step 3>
"""
        ),
        nbf.new_code_cell(
            """# Paste your solution here
def solution():
    pass
    

print(solution())
"""
        ),
        nbf.new_markdown_cell(
            """## 🔄 Revision Log
- <Date>: First attempt, reviewed solution and code.
- [ ] Next revision: <Next Date> (Schedule a revisit for spaced repetition)
"""
        ),
        nbf.new_markdown_cell(
            """## 📝 Personal Notes
- <Your notes here>
"""
        ),
    ]

    nb = nbf.new_notebook(cells=template_cells)

    filename = f"{date_str}.ipynb"
    output_path = os.path.join(output_dir, filename)

    with open(output_path, "w") as f:
        nbformat.write(nb, f)

    print(f"📁 New log created: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a new daily coding log notebook."
    )
    parser.add_argument(
        "--date",
        type=str,
        default=datetime.now().strftime("%d-%m-%Y"),
        help="Date for the log (format: DD-MM-YYYY)",
    )
    parser.add_argument(
        "--output", type=str, default=".", help="Output directory for the notebook"
    )

    args = parser.parse_args()
    create_log(args.date, args.output)
