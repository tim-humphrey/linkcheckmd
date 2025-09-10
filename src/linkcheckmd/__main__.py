"""
check links in Markdown files (as used for Static site generation)

linkcheckMarkdown ~/myHugosite/content/posts github.com

linkcheckMarkdown ~/myJekyllsite/_posts
"""

import argparse
import logging
import time
import json

from .base import check_links


def main():
    p = argparse.ArgumentParser(description="check links in markdown sites")
    p.add_argument("path", help="path to Markdown files")
    p.add_argument(
        "domain",
        help="check only links to this domain (say github.com without https etc.)",
        nargs="?",
    )
    p.add_argument("-ext", help="file extension to scan", default=".md")
    p.add_argument(
        "-m",
        "--method",
        choices=["get", "head"],
        help="head is faster but gives false positives. Get is reliable but slower",
        default="get",
    )
    p.add_argument("--headers", help="add custom headers dictionary", type=json.loads)
    p.add_argument("-v", "--verbose", action="store_true")
    p.add_argument("--sync", help="don't use asyncio", action="store_true")
    p.add_argument("-local", help="only check local files", action="store_true")
    p.add_argument(
        "-r", "--recurse", help="recurse directories under path", action="store_true"
    )
    p.add_argument("-noverify", help="don't verify SSL certificates", action="store_true")
    P = p.parse_args()

    if P.verbose:
        logging.basicConfig(level=logging.INFO)

    tic = time.monotonic()
    bad, stats = check_links(
        P.path,
        ext=P.ext,
        domain=P.domain,
        method=P.method,
        hdr=P.headers,
        use_async=not P.sync,
        local=P.local,
        recurse=P.recurse,
        ssl_verify=not P.noverify,
    )

    elapsed_time = time.monotonic() - tic
    
    # Calculate totals
    total_checked = stats["local_checked"] + stats["remote_checked"]
    
    # ASCII Report
    print("\n" + "=" * 50)
    print("          LINKCHECK SUMMARY REPORT")
    print("=" * 50)
    print(f"Local links checked:      {stats['local_checked']:>8}")
    print(f"Remote links checked:     {stats['remote_checked']:>8}")
    if P.exclude and stats["remote_excluded"] > 0:
        print(f"Remote links excluded:    {stats['remote_excluded']:>8}")
    print("-" * 50)
    print(f"Total links checked:      {total_checked:>8}")
    print("-" * 50)
    print(f"Time elapsed:           {elapsed_time:>8.3f}s")
    
    if bad:
        print(f"Status:               {'FAILED':>8}")
        print(f"Broken links found:     {len(bad):>8}")
        print("=" * 50)
        # using 22 following cURL
        # https://everything.curl.dev/usingcurl/returns
        raise SystemExit(22)
    else:
        print(f"Status:             {'SUCCESS':>8}")
        print("All links are valid! ✓")
        print("=" * 50)


if __name__ == "__main__":
    main()
