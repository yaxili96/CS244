
for i in 1; do
    python jellyfish.py -t jf -r ksp -dir results -nse 16 -nsw 20 -np 4
    
    python jellyfish.py -t jf -r ecmp -dir results -nse 16 -nsw 20 -np 4
    
    python jellyfish.py -t ft -r ksp -np 4 -dir results
    
    python jellyfish.py -t ft -r ecmp -np 4 -dir results
done

python plot.py -dir results -o result.png