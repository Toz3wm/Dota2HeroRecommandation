echo "====================================="
echo "== voc size 1000 "
echo "====================================="
python gensim_models.py testgensim_1 1000
echo "====================================="
echo "== voc size 50000 "
echo "====================================="
python gensim_models.py testgensim_2 50000
echo "====================================="
echo "== voc size 500000 "
echo "====================================="
python gensim_models.py testgensim_3 500000
echo "====================================="
echo "== voc size 2000000 "
echo "====================================="
python gensim_models.py testgensim_4 2000000

