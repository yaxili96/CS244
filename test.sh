for i in 0.5 0.75 1.0; do
    python jellyfish.py -t jf -r ksp -dir results -nse 16 -nsw 20 -np 4 -p $i
    python jellyfish.py -t jf -r ecmp -dir results -nse 16 -nsw 20 -np 4 -p $i
    
#    python jellyfish.py -t ft -r ksp -np 4 -dir results
    
#    python jellyfish.py -t ft -r ecmp -np 4 -dir results

    python plot_links.py -dir results -o result-$i.png -p $i
done