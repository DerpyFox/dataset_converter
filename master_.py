import os
import subprocess
subprocess.run(["python3", "resourses/script1.py", "resourses/mammals.tsv"])
subprocess.run(["Rscript", "resourses/script2.R", 
               "resourses/taxa_for_script.txt", "taxid", "resourses/res_for_script3"])
subprocess.run(["python3", "resourses/script3.py", 
               "resourses/mammals.tsv", "resourses/res_for_script3_taxid.csv"])