import argparse

import streamstats.report

parser = argparse.ArgumentParser(
    prog="python -m streamstats",
    description="Анализатор лог-файлов",
)
commands = parser.add_subparsers(dest="command", required=True)

analyze = commands.add_parser("analyze", help="Анализирует лог-файлы и создает отчет")
analyze.add_argument("INPUT", nargs="+", help="Анализируемыйые файлы")
analyze.add_argument("--format", choices=["csv", "jsonl"], required=True, help="Формат файлаов")
analyze.add_argument("--output", required=True, help="Путь к файлу отчета")
analyze.add_argument("--skip-invalid", action="store_true", help="Пропускать неверные строки")

args = parser.parse_args()
streamstats.report.write_report_from_files(args.INPUT, args.format, args.output, args.skip_invalid)