# crontab-gen
Crontab entry generator from presets. Zero dependencies.
## Usage
```bash
python3 crontab_gen.py weekdays-9am /usr/bin/backup.sh
python3 crontab_gen.py --custom "*/10" 9-17 "*" "*" 1-5 python3 check.py
```
