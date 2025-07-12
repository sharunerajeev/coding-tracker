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
- [ ] Project Work: <Module or Task Name>
- [ ] Tutorial Followed: <Link or Title>
"""
        ),
        nbf.new_markdown_cell(
            """## 💡 Key Learnings
- Bullet key points here.
  - Use sub-bullets for code tricks or insights
- Keep it short and skimmable
"""
        ),
        nbf.new_markdown_cell(
            """## 🧠 Challenges & Debugging
- What did you struggle with?
- How did you figure it out?
"""
        ),
        nbf.new_markdown_cell(
            """## 📚 Resources

| Topic | Description | Link |
|-------|-------------|------|
| XOR Trick | Used in LC 136 | [LeetCode](https://leetcode.com/problems/single-number) |
"""
        ),
        nbf.new_markdown_cell(
            """## 🧪 Code Experiments
<details>
<summary>Click to expand</summary>

```python
# Sample Python code block
def example():
    pass
```

</details>
"""
        ),
        nbf.new_markdown_cell(
            """## 🔁 To Revisit
- [ ] Re-do LC 136 without hints
- [ ] Debug JS async example again
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
