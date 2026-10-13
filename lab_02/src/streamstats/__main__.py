import argparse

import streamstats.analysis

parser = argparse.ArgumentParser(
    prog="python -m toolkit",
    description="TODO",
)
commands = parser.add_subparsers(dest="command", required=True)

analyze = commands.add_parser("analyze", help="TODO")
analyze.add_argument("INPUT", nargs="+", help="TODO")
analyze.add_argument("--format", choices=["csv", "jsonl"], required=True, help="TODO")
analyze.add_argument("--output", required=True, help="TODO")
analyze.add_argument("--skip-invalid", action="store_true", help="TODO")

args = parser.parse_args()
streamstats.analysis.analyze_files(args.INPUT, args.format, args.output, args.skip_invalid)