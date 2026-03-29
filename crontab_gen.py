#!/usr/bin/env python3
"""crontab_gen - Generate crontab expressions from human descriptions."""
import sys, argparse, json, re

PRESETS = {"hourly": "0 * * * *", "daily": "0 0 * * *", "weekly": "0 0 * * 0", "monthly": "0 0 1 * *", "yearly": "0 0 1 1 *", "midnight": "0 0 * * *", "noon": "0 12 * * *", "weekdays": "0 9 * * 1-5", "weekends": "0 10 * * 0,6"}

def parse_desc(desc):
    desc = desc.lower().strip()
    if desc in PRESETS: return PRESETS[desc]
    m = re.match(r"every (\d+) (minute|hour|day|month)s?", desc)
    if m:
        n, unit = int(m.group(1)), m.group(2)
        if unit == "minute": return f"*/{n} * * * *"
        if unit == "hour": return f"0 */{n} * * *"
        if unit == "day": return f"0 0 */{n} * *"
        if unit == "month": return f"0 0 1 */{n} *"
    m = re.match(r"at (\d{1,2}):(\d{2})", desc)
    if m: return f"{int(m.group(2))} {int(m.group(1))} * * *"
    return None

def explain(expr):
    parts = expr.split()
    if len(parts) != 5: return "Invalid expression"
    names = ["minute", "hour", "day of month", "month", "day of week"]
    explanation = []
    for i, (part, name) in enumerate(zip(parts, names)):
        if part == "*": continue
        elif part.startswith("*/"): explanation.append(f"every {part[2:]} {name}s")
        elif "," in part: explanation.append(f"{name}: {part}")
        elif "-" in part: explanation.append(f"{name}: {part}")
        else: explanation.append(f"{name}: {part}")
    return "; ".join(explanation) if explanation else "every minute"

def main():
    p = argparse.ArgumentParser(description="Crontab generator")
    sub = p.add_subparsers(dest="cmd")
    g = sub.add_parser("generate"); g.add_argument("description")
    e = sub.add_parser("explain"); e.add_argument("expression")
    l = sub.add_parser("presets")
    args = p.parse_args()
    if args.cmd == "generate":
        expr = parse_desc(args.description)
        print(json.dumps({"description": args.description, "crontab": expr, "explanation": explain(expr) if expr else None}))
    elif args.cmd == "explain":
        print(json.dumps({"expression": args.expression, "explanation": explain(args.expression)}))
    elif args.cmd == "presets":
        print(json.dumps({"presets": PRESETS}, indent=2))
    else: p.print_help()

if __name__ == "__main__": main()
