import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    # Inicializa a probabilidade conjunta com 1
    probability = float(1)

    for person in people:
        ## Determina o número de genes da pessoa (0, 1 ou 2)
        genes = (
            2 if person in two_genes 
            else 
            1 if person in one_gene
            else 
            0
        )

        # Determina se a pessoa possui ou não a característica (trait)
        trait = person in have_trait
        mother = people[person]["mother"]
        father = people[person]["father"]

         # Caso a pessoa não tenha pais listados no banco de dados
        if mother is None and father is None:
            probability *= PROBS["gene"][genes]

        #pessoas que tem pais listados
        else:
            gene_pass = {mother: 0, father: 0}
            #probabilidade de pais passarem os genes
            for parent in gene_pass:
                gene_pass[parent] = (
                    #pais com dois genes tem uma certa probabilidade de 1 de passar, a menos que sofra mutacao
                    1 - PROBS["mutation"] if parent in two_genes 
                    else
                    #pais com um gene têm uma probabilidade de 0.5 de passar
                    0.5 if parent in one_gene
                    else
                    #pais sem gene nao pode passar, a menos que sofra mutacao
                    PROBS["mutation"]
                )
            probability *= (
                #ambos pais passarem um gene
                gene_pass[mother] * gene_pass[father] if genes == 2
                else
                #gene da mae e nao do pai ou contrario
                gene_pass[mother] * (1 - gene_pass[father]) + (1 - gene_pass[mother]) * gene_pass[father] if genes == 1
                else
                #gene de nenhum dos pais
                (1 - gene_pass[mother]) * (1 - gene_pass[father])
            )

        #multiplica pela probabilidade de a pessoa ter ou nao uma caracteristica particular, dado gene
        probability *= PROBS["trait"][genes][trait]
    return probability

def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    # Percorre todas as pessoas no dicionário de probabilidades
    for person in probabilities:
        
        # Determina a quantidade de genes da pessoa
        genes = (
            2 if person in two_genes  # Se a pessoa está em `two_genes`, ela tem 2 genes
            else
            1 if person in one_gene  # Se a pessoa está em `one_gene`, ela tem 1 gene
            else
            0  # Caso contrário, tem 0 genes
        )
        
        # Verifica se a pessoa tem a característica (trait)
        trait = person in have_trait
        
        # Atualiza a probabilidade do número de genes da pessoa
        probabilities[person]["gene"][genes] += p
        
        # Atualiza a probabilidade da característica (trait) da pessoa
        probabilities[person]["trait"][trait] += p
    
def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    #obter a soma das probabilidades
    for person in probabilities:
        for field in probabilities[person]:
            total = sum(dict(probabilities[person][field]).values())
            for value in probabilities[person][field]:
                probabilities[person][field][value] /= total


if __name__ == "__main__":
    main()
