
for i in 1 2 3; do
    python jellyfish.py -t jf -r ksp -nse 16 -nsw 20 -np 4
    
    python jellyfish.py -t jf -r ecmp -nse 16 -nsw 20 -np 4
    
    python jellyfish.py -t ft -r ksp -np 4
    
    python jellyfish.py -t ft -r ecmp -np 4
done