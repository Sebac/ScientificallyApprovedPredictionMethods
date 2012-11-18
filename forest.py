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
    
def split (data, attrs, targ):
    ret = [] #List of new data objects.    
    n = 3#int(round(math.sqrt(len(data[0]) - 1)))
    
    attrs = [attr for attr in attrs if attr != targ]
    
    for i in range(100):
        new_attrs = []
        selected = []
        new_data = {"data": []}
        
        
        for j in range(n):
            attr = int(    round( random.random() * (len(attrs) - 1) )    )

            while attr in selected:
                attr = int(    round( random.random() * (len(attrs) - 1) )    )
             
            selected.append(attr)
            new_attrs.append(attrs[attr])
            
        new_attrs.append(targ)
        new_data["attributes"] = new_attrs
        
        for entry in data:
            new_data["data"].append({attr : entry[attr] for attr in entry if attr in new_attrs})

        ret.append(new_data)
        
    return ret
    
    
    
def tree(data, attributes, target_attr):
    """
    This function creates a list of exmaples data (used to learn the d-tree)
    and a list of samples (for classification by the d-tree) from the
    designated file.  It then creates the d-tree and uses it to classify the
    samples.  It prints the classification of each record in the samples list
    and returns the d-tree.
    """
        
    # Copy the data list into the examples list for testing
    examples = data[:]
    
    # Create the decision tree
    tree = create_decision_tree(data, attributes, target_attr, gain)

    return classify(tree, examples)




def forest(data, attributes, target_attr):
    """
    This function creates a list of exmaples data (used to learn the d-tree)
    and a list of samples (for classification by the d-tree) from the
    designated file.  It then creates the d-tree and uses it to classify the
    samples.  It prints the classification of each record in the samples list
    and returns the d-tree.
    """
        
    # Copy the data list into the examples list for testing
    examples = data[:]
    
    new_data = split(data, attributes, target_attr)
    forest = []
    
    for part in new_data:
        # Create the decision tree
        forest.append(create_decision_tree(part["data"], part["attributes"], target_attr, gain))

    # Classify the records in the examples list
    return vote(forest, examples)    




def print_tree(tree, str):
    """
    This function recursively crawls through the d-tree and prints it out in a
    more readable format than a straight print of the Python dict object.  
    """
    if type(tree) == dict:
        #print "%s%s" % (str, tree.keys()[0])
        for item in tree.values()[0].keys():
            #print "%s\t%s" % (str, item)
            print_tree(tree.values()[0][item], str + "\t")
    else:
        pass
        #print "%s\t->\t%s" % (str, tree)



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


forest = forest(data, attributes, target_attr)


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
data = []
for line in lines:
    data.append(dict(zip(attributes,
                         [datum.strip() for datum in line.split(",")])))



print mistakes(forest, data, target_attr)



