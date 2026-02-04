# DocOps Quality Task - CI/CD Demo

This repository is a **demonstration extension** of the Documentation Quality Task. It showcases how the quality check script (`doc_checker.py`) can be integrated into a Continuous Integration (CI) pipeline using **GitHub Actions**.

## 🚀 How to see it in action

1.  **View the Pipeline:** Click on the **[Actions](https://github.com/Wiktor-Potapczyk/doc-quality-ci-demo/actions)** tab in this repository.
2.  **Check the Logs:** Click on the latest workflow run to see the step-by-step execution:
    *   Environment setup (Ubuntu + Python 3.9)
    *   Dependency installation (`beautifulsoup4`, `lxml`)
    *   **Automatic execution** of `doc_checker.py` against the test files.

## 🛠 What does the pipeline do?

The configuration is defined in `.github/workflows/quality-check.yml`. Every time code is pushed to the repository, it automatically:

1.  **Spins up a clean container** (Ubuntu latest).
2.  **Installs dependencies** ensuring the environment is reproducible.
3.  **Runs the Quality Checker** script against the documentation.
4.  **Reports Status:**
    *   ✅ **Success:** If the documentation passes all checks.
    *   ❌ **Failure:** If the script detects errors (e.g., missing meta tags, broken structure), the pipeline fails, preventing bad documentation from being merged.

## 📂 Original Solution

For the standard solution code without the CI/CD layer, please see the [main repository](https://github.com/Wiktor-Potapczyk/doc-quality-checker).
