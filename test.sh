
for i in 1; do
    python jellyfish.py -t jf -r ksp -dir results -nse 32 -nsw 40 -np 4 -p 0.5
    python jellyfish.py -t jf -r ecmp -dir results -nse 32 -nsw 40 -np 4 -p 0.5
    
    python jellyfish.py -t ft -r ksp -np 4 -dir results
    
    python jellyfish.py -t ft -r ecmp -np 4 -dir results
done

python plot.py -dir results -o result.png
