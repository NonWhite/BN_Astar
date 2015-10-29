sets=( census letter image mushroom sensors steelPlates epigenetics alarm spectf lungCancer )

for i in "${sets[@]}"
do
	wc "../data/${i}_scores.txt" "$IME_HOME/Pesquisas/BN_Initializer/data/${i}_scores.txt"
done
