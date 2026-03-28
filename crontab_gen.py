#!/usr/bin/env python3
"""Crontab entry generator from patterns."""
import sys

PRESETS = {
    'every-minute': '* * * * *',
    'every-5min': '*/5 * * * *',
    'every-15min': '*/15 * * * *',
    'every-hour': '0 * * * *',
    'every-day': '0 0 * * *',
    'every-week': '0 0 * * 0',
    'every-month': '0 0 1 * *',
    'every-year': '0 0 1 1 *',
    'weekdays-9am': '0 9 * * 1-5',
    'weekends-noon': '0 12 * * 6,0',
    'mon-wed-fri': '0 0 * * 1,3,5',
    'business-hours': '0 9-17 * * 1-5',
    'midnight': '0 0 * * *',
    'noon': '0 12 * * *',
    'reboot': '@reboot',
}

def generate(minute='*',hour='*',dom='*',month='*',dow='*'):
    return f"{minute} {hour} {dom} {month} {dow}"

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Presets:"); [print(f"  {k:20s} {v}") for k,v in PRESETS.items()]
        print("\nUsage: crontab_gen.py <preset> [command]")
        print("       crontab_gen.py --custom MIN HOUR DOM MON DOW [command]")
        sys.exit(0)
    if sys.argv[1] == '--custom':
        expr = generate(*sys.argv[2:7])
        cmd = ' '.join(sys.argv[7:]) if len(sys.argv) > 7 else 'echo "hello"'
    elif sys.argv[1] in PRESETS:
        expr = PRESETS[sys.argv[1]]
        cmd = ' '.join(sys.argv[2:]) if len(sys.argv) > 2 else 'echo "hello"'
    else:
        print(f"Unknown preset: {sys.argv[1]}"); sys.exit(1)
    print(f"{expr} {cmd}")
