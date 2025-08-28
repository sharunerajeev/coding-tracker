import argparse
from datetime import datetime
import nbformat
from nbformat import v4 as nbf
import os
import json

try:
    import yaml
except ImportError:
    yaml = None


def prompt_problem():
    print("Enter new problem details:")
    name = input("Problem name: ").strip()
    link = input("Problem link: ").strip()
    description = input("Problem description: ").strip()
    test_input = input("Test input (Python literal, e.g. 5 or [1,2,3]): ").strip()
    try:
        test_input_eval = eval(test_input)
    except Exception:
        test_input_eval = test_input
    return {
        "name": name or "<Name>",
        "link": link or "#",
        "description": description or "<Problem description here>",
        "test_input": test_input_eval if test_input else "<test_input>",
    }


def add_problem_to_log(date_str, output_dir):
    filename = f"{date_str}.ipynb"
    output_path = os.path.join(output_dir, filename)
    if not os.path.exists(output_path):
        print(f"Log file {output_path} does not exist. Please create it first.")
        return

    nb = nbformat.read(output_path, as_version=4)
    problem = prompt_problem()

    # Count existing problems to determine next problem number
    problem_number = 1
    for cell in nb.cells:
        if (
            cell.cell_type == "markdown"
            and cell.source.strip().startswith("### Problem")
        ):
            # Accept both "### Problem N:" and "### Problem: "
            if cell.source.strip().startswith("### Problem "):
                try:
                    after = cell.source.strip()[len("### Problem "):]
                    if after[0].isdigit():
                        num = ""
                        for c in after:
                            if c.isdigit():
                                num += c
                            else:
                                break
                        if num:
                            problem_number = max(problem_number, int(num) + 1)
                except Exception:
                    continue
            elif cell.source.strip().startswith("### Problem:"):
                problem_number += 1

    # Update the Tasks Overview section
    for cell in nb.cells:
        if (
            cell.cell_type == "markdown"
            and cell.source.strip().startswith("## ✅ Tasks Completed")
        ):
            # Find the last "- Problem N:" line and append the new one after it
            lines = cell.source.splitlines()
            # Find the last problem line index
            last_idx = 0
            for idx, line in enumerate(lines):
                if line.strip().startswith("- Problem "):
                    last_idx = idx
            # Insert new problem line after the last problem
            new_problem_line = f"- Problem {problem_number}: {problem['name']} ([Link]({problem['link']}))"
            # Insert before any trailing blank lines
            insert_at = last_idx + 1
            while insert_at < len(lines) and lines[insert_at].strip() == "":
                insert_at += 1
            lines.insert(insert_at, new_problem_line)
            cell.source = "\n".join(lines)
            break

    # Find the insertion index (before revision log/personal notes)
    insert_idx = len(nb.cells)
    for i, cell in enumerate(nb.cells):
        if cell.cell_type == "markdown" and (
            cell.source.strip().startswith("## 🔄 Revision Log")
            or cell.source.strip().startswith("## 📝 Personal Notes")
        ):
            insert_idx = i
            break

    # Use the correct heading format for the new problem
    nb.cells.insert(
        insert_idx,
        nbf.new_markdown_cell(
            f"### Problem {problem_number}: {problem['name']}\n{problem['description']}\n"
        ),
    )
    nb.cells.insert(
        insert_idx + 1,
        nbf.new_code_cell(
            "# Paste your solution here\nclass Solution:\n"
            "    # @param A : integer\n"
            "    def solve(self, A):\n"
            "        pass\n\n"
            f"Solution().solve({repr(problem['test_input'])})"
        ),
    )

    nbformat.write(nb, output_path)
    print(f"✅ Problem {problem_number} added to {output_path}")


def create_log(
    date_str,
    output_dir,
    num_problems=4,
    add_revision_log=True,
    add_personal_notes=True,
):
    # Title cell
    title_cell = nbf.new_markdown_cell(f"# 📅 Date: {date_str}")

    # Focus area cell
    focus_area_cell = nbf.new_markdown_cell(
        "## 🔍 Focus Area\n- <e.g., Recursion, Arrays, Sliding Window>\n"
    )

    # Use placeholders
    problems = []
    for i in range(1, num_problems + 1):
        problems.append(
            {
                "name": "<Name>",
                "link": "#",
                "description": "<Problem description here>",
                "test_input": "<test_input>",
            }
        )

    # Tasks completed cell
    tasks_completed_lines = ["## ✅ Tasks Completed"]
    for idx, prob in enumerate(problems, 1):
        tasks_completed_lines.append(
            f"- Problem {idx}: {prob['name']} ([Link]({prob['link']}))"
        )
    tasks_completed_cell = nbf.new_markdown_cell("\n".join(tasks_completed_lines))

    # Code experiments section header
    code_experiments_cell = nbf.new_markdown_cell("## 🧪 Code Experiments\n")

    # Problem cells
    problem_cells = []
    for idx, prob in enumerate(problems, 1):
        problem_cells.append(
            nbf.new_markdown_cell(
                f"### Problem {idx}: {prob['name']}\n{prob['description']}\n"
            )
        )
        test_input = prob.get("test_input", "<test_input>")
        problem_cells.append(
            nbf.new_code_cell(
                "# Paste your solution here\nclass Solution:\n"
                "    # @param A : integer\n"
                "    def solve(self, A):\n"
                "        pass\n\n"
                f"Solution().solve({test_input})"
            )
        )

    # Optionally, add revision log and personal notes
    cells = [
        title_cell,
        focus_area_cell,
        tasks_completed_cell,
        code_experiments_cell,
        *problem_cells,
    ]
    if add_revision_log:
        cells.append(
            nbf.new_markdown_cell(
                "## 🔄 Revision Log\n"
                "- <Date>: First attempt, reviewed solution and code.\n"
                "- [ ] Next revision: <Next Date> (Schedule a revisit for spaced repetition)\n"
            )
        )
    if add_personal_notes:
        cells.append(
            nbf.new_markdown_cell("## 📝 Personal Notes\n- <Your notes here>\n")
        )

    nb = nbf.new_notebook(cells=cells)

    filename = f"{date_str}.ipynb"
    output_path = os.path.join(output_dir, filename)

    with open(output_path, "w") as f:
        nbformat.write(nb, f)

    print(f"📁 New log created: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a new daily coding log notebook or add a problem interactively."
    )
    parser.add_argument(
        "-d",
        "--date",
        type=str,
        default=datetime.now().strftime("%d-%m-%Y"),
        help="Date for the log (format: DD-MM-YYYY)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default=".",
        help="Output directory for the notebook",
    )
    parser.add_argument(
        "-n",
        "--num-problems",
        type=int,
        default=4,
        help="Number of problems to include",
    )
    parser.add_argument(
        "--no-revision-log",
        "-r",
        action="store_true",
        help="Do not include revision log section",
    )
    parser.add_argument(
        "--no-personal-notes",
        "-t",
        action="store_true",
        help="Do not include personal notes section",
    )
    parser.add_argument(
        "-a",
        "--add-problem",
        action="store_true",
        help="Interactively add a new problem to the log for the given date",
    )

    args = parser.parse_args()
    if args.add_problem:
        add_problem_to_log(args.date, args.output)
    else:
        create_log(
            args.date,
            args.output,
            num_problems=args.num_problems,
            add_revision_log=not args.no_revision_log,
            add_personal_notes=not args.no_personal_notes,
        )
