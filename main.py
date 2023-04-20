import model
import thescelosaurus
import velociraptor 
import parameters
import math

velo = velociraptor.Velociraptor([math.pi / 2, [2, 0], 0.3], 5.56)
other_velo = velociraptor.Velociraptor([math.pi / 2, [-2, 0], 0.3], 5.56)

thesce = thescelosaurus.Thescelosaurus([0, [0, 45], 13.8 / 0.5], 4.53)

# Pour ne pas sauvegarder l'animation, il est nécessaire de mettre le premier 
# élément de la liste à False.
# Dans le cas contraire, il est nécessaire de remplacer "path" par le répertoire
# contenant le fichier .exe du module.
sim = model.Model([velo, other_velo], thesce, 4200, True, [True, "path"])

print(sim.simulation())