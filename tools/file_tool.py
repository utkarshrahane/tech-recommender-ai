import os

def save_report_to_file(content: str, filename: str = "recommendation_report.md"):
    """
    Saves the final AI analysis to a local Markdown file.
    """
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Successfully saved report to {filename}"
    except Exception as e:
        return f"Error saving file: {str(e)}"
    