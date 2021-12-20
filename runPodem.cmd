python src/PODEM.py --cktFile files/s27.txt --faultFile PODEMTests/s27.fault.txt  > PODEMTests/s27.output.txt
python src/PODEM.py --cktFile files/s298f_2.txt --faultFile PODEMTests/s298f_2.fault.txt  > PODEMTests/s298f_2.output.txt
python src/PODEM.py --cktFile files/s344f_2.txt --faultFile PODEMTests/s344f_2.fault.txt  > PODEMTests/s344f_2.output.txt
python src/PODEM.py --cktFile files/s349f_2.txt --faultFile PODEMTests/s349f_2.fault.txt  > PODEMTests/s349f_2.output.txt

python src/PODEM.py --dfs --cktFile files/s27.txt --faultFile PODEMTests/s27.fault.txt  > PODEMTests/all.output.txt
python src/PODEM.py --dfs --cktFile files/s298f_2.txt --faultFile PODEMTests/s298f_2.fault.txt  >> PODEMTests/all.output.txt
python src/PODEM.py --dfs --cktFile files/s344f_2.txt --faultFile PODEMTests/s344f_2.fault.txt  >> PODEMTests/all.output.txt
python src/PODEM.py --dfs --cktFile files/s349f_2.txt --faultFile PODEMTests/s349f_2.fault.txt  >> PODEMTests/all.output.txt