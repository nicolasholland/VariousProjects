ocropus-rpred -n 'preprocessed/0032/??????.bin.png' -m $1
cat preprocessed/0032/??????.txt > set2__p32_tmp.txt
python loss.py set2__p32_tmp.txt 32.gt.txt >> total_loss_page32_set2.txt
