from dtree import *
from id3 import *
import random
import sys


def get_file():
    """
    Tries to extract a filename from the command line.  If none is present, it
    prompts the user for a filename and tries to open the file.  If the file 
    exists, it returns it, otherwise it prints an error message and ends
    execution. 
    """
    # Get the name of the data file and load it into 
    if len(sys.argv) < 2:
        # Ask the user for the name of the file
        print "Filename: ", 
        filename = sys.stdin.readline().strip()
    else:
        filename = sys.argv[1]

    try:
        fin = open(filename, "r")
    except IOError:
        print "Error: The file '%s' was not found on this system." % filename
        sys.exit(0)

    return fin
    
def split (data, attrs, targ, n, nt):
    ret = [] #List of new data objects.    
    
    attrs = [attr for attr in attrs if attr != targ]
    
    for i in range(nt):
        new_attrs = []
        selected = []
        new_data = {"data": []}
        
        
        for j in range(n):
            attr = int(    round( random.random() * (len(attrs) - 1) )    )

            while attr in selected:
                attr = int(    round( random.random() * (len(attrs) - 1) )    )
                
             
            selected.append(attr)
            new_attrs.append(attrs[attr])
            
            if len(selected) == len(attrs):
                break;
            
        new_attrs.append(targ)
        new_data["attributes"] = new_attrs
        
        for entry in data:
            new_data["data"].append({attr : entry[attr] for attr in entry if attr in new_attrs})

        ret.append(new_data)
        
    return ret
    
    




def create_forest(data, attributes, target_attr, gene):
    """
    This function creates a list of exmaples data (used to learn the d-tree)
    and a list of samples (for classification by the d-tree) from the
    designated file.  It then creates the d-tree and uses it to classify the
    samples.  It prints the classification of each record in the samples list
    and returns the d-tree.
    """
        
    # Copy the data list into the examples list for testing
    examples = data[:]
        
    new_data = split(data, attributes, target_attr, gene["nattrs"], gene["ntrees"])
    forest = {"trees": [], "gene": gene}
    
    for part in new_data:
        # Create the decision tree
        forest["trees"].append(create_decision_tree(part["data"], part["attributes"], target_attr, gain))

    return forest



def create_forests(n, data, attributes, target_attr, genes):
    ret = []

    while n > 0:
        ret.append(create_forest(data, attributes, target_attr, genes[n - 1]))
        n -= 1


    return ret




fin = get_file()

# Create a list of all the lines in the data file
lines = [line.strip() for line in fin.readlines()]

fin.close()

# Remove the attributes from the list of lines and create a list of
# the attributes.
lines.reverse()
attributes = [attr.strip() for attr in lines.pop().split(",")]
target_attr = attributes[-1]
lines.reverse()

# Create a list of the data in the data file
data = []
for line in lines:
    data.append(dict(zip(attributes,
                         [datum.strip() for datum in line.split(",")])))






fin = open("correct_dataset2")

# Create a list of all the lines in the data file
lines = [line.strip() for line in fin.readlines()]

fin.close()

# Remove the attributes from the list of lines and create a list of
# the attributes.
lines.reverse()
attributes = [attr.strip() for attr in lines.pop().split(",")]
target_attr = attributes[-1]
lines.reverse()

# Create a list of the data in the data file
data2 = []
for line in lines:
    data2.append(dict(zip(attributes,
                         [datum.strip() for datum in line.split(",")])))





nf = 30 #Number of forests.
i = 20 #Iterations.
gen = 1

def randomGene():
    return {"nattrs": int(round(7*random.random())), "ntrees": int(round(100*random.random()))}

def get_rand(a, b):
    return int(a + round(random.random()*(b - a)))

def avgGene(gene1, gene2):
    avg = {"nattrs": int(round((gene1["nattrs"] + gene2["nattrs"])/2.0)), "ntrees": int(round((gene1["ntrees"] + gene2["ntrees"])/2.0))}

    gene = {"nattrs": avg["nattrs"] + get_rand(-1, 1), "ntrees": avg["ntrees"] + get_rand(-5, 5)}
    
    if gene["nattrs"] > 7:
        gene["nattrs"] = 7
            
    if gene["nattrs"] < 1:
        gene["nattrs"] = 1
    

    return gene





print "Constructing random generation #1..."

new_genes = []

for bla in range(nf):
    new_genes.append(randomGene())

forests = create_forests(nf, data, attributes, target_attr, new_genes)

evaluations = []

for forest in forests:
    forest["eval"] = evaluateForest(forest["trees"], data2, target_attr)        


forests = sorted(forests, key = lambda el: el["eval"])


print "Done."
print ""
print ""
print ""
print "Starting..."
print ""


best = []
best.append(forests[len(forests) - 1])
best.append(forests[len(forests) - 2])

while i > 0:
    i -= 1
    
    print [forest["eval"] for forest in forests]

    print "Generation " + str(gen) + "#."
    print "Best genome:"
    print best[len(best) - 1]["gene"]
    print evaluateForest(best[len(best) - 1]["trees"], data2, target_attr)
    print ""
    print ""
    
    gen += 1







    new_genes = []
    
    new_genes.append(best[len(best) - 1]["gene"])
    new_genes.append(best[len(best) - 2]["gene"])
    


    for bla in range(nf - 2):
        one = int(round(random.random()*(nf-1)))
        two = int(round(random.random()*(nf-1)))
    
        new_genes.append(avgGene(forests[one]["gene"], forests[two]["gene"]))



    forests = create_forests(nf, data, attributes, target_attr, new_genes)
    
    
    for forest in forests:
        forest["eval"] = evaluateForest(forest["trees"], data2, target_attr)        
        


    forests = sorted(forests, key = lambda el: el["eval"])
    
    
    best.append(forests[len(forests) - 1])
    best = sorted(best, key = lambda el: el["eval"])
        


print ""
print "Done."
print ""
print ""
print "Performance of the best forest:"
print evaluateForest(best[len(best) - 1]["trees"], data2, target_attr)
print ""
print "Final genome:"
print best[len(best) - 1]["gene"]

print ""
print ""
print "Evolution over, initiating test."
print ""



print "Performance of the best forest on the test set:"
print evaluateForest(best[len(best) - 1]["trees"], data2, target_attr)

