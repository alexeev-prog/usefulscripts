#!/usr/bin/env python3
import re
import subprocess
from pathlib import Path
from typing import Optional


class GitVersion:
    """Retrieves version information from the current Git repository."""

    def __init__(self, repo_path: Optional[Path] = None):
        """Initialize GitVersion with optional repository path."""
        self._default_version = "0.1.0"
        self._repo_path = Path.cwd() if repo_path is None else Path(repo_path).resolve()

    def _run_git_command(self, command: list) -> str:
        """Execute a git command and return the output."""
        try:
            result = subprocess.run(
                command, cwd=self._repo_path, capture_output=True, text=True, check=True
            )
            return result.stdout.strip()
        except (subprocess.CalledProcessError, FileNotFoundError):
            return ""

    @property
    def tag(self) -> str:
        """Get the most recent version tag."""
        return self._run_git_command(
            ["git", "describe", "--match", "v[0-9]*", "--abbrev=0", "--tags"]
        )

    @property
    def version(self) -> str:
        """Get the full version string with build number."""
        if not self.tag:
            return self._default_version
        version = f"{self.tag[1:]}.{self.build}"
        return version if version != "." else self._default_version

    @property
    def default_branch(self) -> str:
        """Get the default branch name."""
        branch = self._run_git_command(["git", "config", "--get", "init.defaultBranch"])
        return branch if branch else "main"

    @property
    def build(self) -> str:
        """Get the number of commits since the last tag."""
        if not self.tag:
            return "0"
        return self._run_git_command(["git", "rev-list", f"{self.tag}..", "--count"])

    @property
    def branch(self) -> str:
        """Get the current branch name."""
        return self._run_git_command(["git", "branch", "--show-current"])

    @property
    def full(self) -> str:
        """Get the full version with branch name."""
        return f"{self.version}-{self.branch}" if self.branch else self.version

    @property
    def standard(self) -> str:
        """Get the standardized version string."""
        if not self.branch:
            return self.version
        if self.branch == self.default_branch or re.match(r"release/.*", self.branch):
            return self.version
        return f"{self.version}-{self.branch}"

    @property
    def commit(self) -> str:
        """Get the full commit hash."""
        return self._run_git_command(["git", "rev-parse", "HEAD"])

    @property
    def commit_hash(self) -> str:
        """Get the short commit hash."""
        return self._run_git_command(["git", "rev-parse", "--short", "HEAD"])

    def __str__(self) -> str:
        """Return a formatted string with all version information."""
        return f"""
Tag: {self.tag}
Version: {self.version}
Full: {self.full}
Branch: {self.branch}
Build: {self.build}
Standard: {self.standard}
Commit: {self.commit}

GitRepo {self.full} {self.commit_hash}
"""


if __name__ == "__main__":
    git_version = GitVersion()
    print(git_version)
