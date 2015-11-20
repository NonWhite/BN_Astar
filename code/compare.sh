sets=( census voting letter hepatitis image heart mushroom parkinsons autos flag )
RESULTS_DIR="../results/"

for i in "${sets[@]}"
do
	echo " ============================== ${i} ============================== "
	head -n5 "${RESULTS_DIR}${i}_simple.txt" "${RESULTS_DIR}${i}_dynamic_k2.txt" "${RESULTS_DIR}${i}_dynamic_k3.txt" "${RESULTS_DIR}${i}_dynamic_k4.txt" "${RESULTS_DIR}${i}_static_d2.txt" "${RESULTS_DIR}${i}_static_d3.txt"
done
