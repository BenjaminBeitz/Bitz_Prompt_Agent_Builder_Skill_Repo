#!/usr/bin/env python3
"""
OKF v0.2 Knowledge Base & Graph Validator for Bitz Prompt & Agent Builder Suite
Validates YAML frontmatter integrity, mandatory keys, and relative link resolution
across all documentation, research, and skill index cards.
"""

import os
import re
import sys
from pathlib import Path

# Ensure UTF-8 output on Windows console
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

LINK_KEYS = [
    "implements_prd", "architected_by", "references_context",
    "referenced_in_prd", "enforces_invariants", "enforced_by_arch",
    "implements_terms", "modeled_in_arch", "governed_by_adr",
    "grounds_prd_hypothesis", "informs_arch_approach"
]

def is_okf_target_file(file_path, base_path):
    rel_str = str(file_path.relative_to(base_path)).replace("\\", "/")
    
    # Root index.md or any index.md is an OKF target
    if file_path.name == "index.md":
        return True

    # Any file in research references/ or docs/
    if "research references/" in rel_str or "docs/" in rel_str:
        return True

    # Check if the file has explicit OKF frontmatter
    try:
        head = file_path.read_text(encoding="utf-8-sig")[:400]
        if head.startswith("---") and re.search(r"^type:\s*(?:concept|arch|context|index|architecture-spec|guide)", head, re.MULTILINE):
            return True
    except Exception:
        pass

    return False

def validate_knowledge_base(target_dir):
    target_path = Path(target_dir).resolve()
    if not target_path.exists():
        print(f"[ERROR] Target directory '{target_dir}' does not exist.")
        return 1

    all_md = list(target_path.rglob("*.md"))
    md_files = [f for f in all_md if is_okf_target_file(f, target_path)]
    
    if not md_files:
        print(f"[*] No active OKF bundle cards found in '{target_path}'.")
        return 0

    print(f"[*] Validating {len(md_files)} OKF Knowledge cards in '{target_path.name}'...\n")

    errors = []
    link_checks = 0

    for file_path in md_files:
        try:
            rel_path = str(file_path.relative_to(target_path)).replace("\\", "/")
        except ValueError:
            rel_path = file_path.name
            
        content = file_path.read_text(encoding="utf-8-sig")

        # 1. Check YAML Frontmatter
        if not content.startswith("---"):
            errors.append(f"[{rel_path}] Missing starting YAML frontmatter delimiter (---).")
            continue

        parts = content.split("---", 2)
        if len(parts) < 3:
            errors.append(f"[{rel_path}] Incomplete or malformed YAML frontmatter.")
            continue

        frontmatter = parts[1]
        
        # 2. Check 'type:' key
        if not re.search(r"^type:\s*\S+", frontmatter, re.MULTILINE):
            errors.append(f"[{rel_path}] Missing mandatory 'type:' key in frontmatter.")

        # 3. Check 'title:' or 'name:' key
        has_title = bool(re.search(r"^title:\s*", frontmatter, re.MULTILINE))
        has_name = bool(re.search(r"^name:\s*", frontmatter, re.MULTILINE))
        if not (has_title or has_name):
            errors.append(f"[{rel_path}] Missing 'title:' in frontmatter.")

        # 4. Check Markdown Relative Links in Body
        # Handles [text](link)
        links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", parts[2])
        for text, link in links:
            if link.startswith("http") or link.startswith("#") or link.startswith("mailto"):
                continue
            
            link_target = link.split("#")[0]
            if not link_target:
                continue

            # Unquote URL encodings if present (e.g., %20)
            import urllib.parse
            decoded_target = urllib.parse.unquote(link_target)
            target_res = (file_path.parent / decoded_target).resolve()
            link_checks += 1
            if not target_res.exists():
                errors.append(f"[{rel_path}] Broken markdown link: '{link}' -> Missing file: '{target_res}'")

        # 5. Check Frontmatter Typed Graph Links
        for lk in LINK_KEYS:
            pattern = rf"^{re.escape(lk)}:\s*\n((?:[ \t]*-[ \t]*[^\n]+\n*)*)"
            match = re.search(pattern, frontmatter, re.MULTILINE)
            if match:
                for line in match.group(1).strip().split("\n"):
                    line = line.strip()
                    if line.startswith("-"):
                        target_file = line.lstrip("- ").strip(' "\'')
                        if target_file:
                            import urllib.parse
                            decoded_file = urllib.parse.unquote(target_file)
                            target_res = (file_path.parent / decoded_file).resolve()
                            link_checks += 1
                            if not target_res.exists():
                                errors.append(f"[{rel_path}] Broken frontmatter '{lk}' link: '{target_file}' -> Missing: '{target_res}'")

    print(f"[*] Verified {link_checks} graph and navigation links.")

    if errors:
        print(f"\n[ERROR] OKF Validation Failed with {len(errors)} error(s):")
        for err in errors:
            print(f"  - {err}")
        return 1
    else:
        print(f"\n[OK] OKF Graph is 100% HEALTHY! All {len(md_files)} OKF cards and {link_checks} links verified.")
        return 0

if __name__ == "__main__":
    if len(sys.argv) > 1:
        check_dir = Path(sys.argv[1]).resolve()
    else:
        check_dir = Path(__file__).resolve().parent.parent
    sys.exit(validate_knowledge_base(check_dir))
