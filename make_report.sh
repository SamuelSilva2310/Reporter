 #!/bin/bash
pwd
source ../../venv/bin/activate 
python3 ../../report_maker/main.py -i ../exports/$1 -o $2