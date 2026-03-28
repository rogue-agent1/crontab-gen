#!/usr/bin/env python3
"""crontab_gen - Generate crontab expressions from human descriptions."""
import sys
PRESETS={
    "hourly":"0 * * * *","daily":"0 0 * * *","weekly":"0 0 * * 0",
    "monthly":"0 0 1 * *","yearly":"0 0 1 1 *","midnight":"0 0 * * *",
    "noon":"0 12 * * *","weekdays":"0 9 * * 1-5","weekends":"0 10 * * 0,6",
    "every5min":"*/5 * * * *","every15min":"*/15 * * * *","every30min":"*/30 * * * *",
}
def build(minute="*",hour="*",dom="*",month="*",dow="*"):
    return f"{minute} {hour} {dom} {month} {dow}"
def explain(expr):
    parts=expr.split(); names=["minute","hour","day of month","month","day of week"]
    for p,n in zip(parts,names):
        if p=="*": print(f"  {n}: every {n}")
        elif "/" in p: base,step=p.split("/"); print(f"  {n}: every {step} {n}s" + (f" from {base}" if base!="*" else ""))
        elif "-" in p: lo,hi=p.split("-"); print(f"  {n}: {lo} through {hi}")
        elif "," in p: print(f"  {n}: {p}")
        else: print(f"  {n}: {p}")
if __name__=="__main__":
    if len(sys.argv)<2:
        print("Presets:"); [print(f"  {k:15s} → {v}") for k,v in PRESETS.items()]
    elif sys.argv[1] in PRESETS:
        expr=PRESETS[sys.argv[1]]; print(f"{sys.argv[1]}: {expr}"); explain(expr)
    elif len(sys.argv)==6:
        expr=build(*sys.argv[1:6]); print(f"Expression: {expr}"); explain(expr)
    else:
        expr=sys.argv[1]; print(f"Expression: {expr}"); explain(expr)
