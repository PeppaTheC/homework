import re
from collections import Counter
import matplotlib.pyplot as plt


def translate_from_dna_to_rna(dna: str) -> str:
    """Функция переводит последовательность ДНК
        в последовательность РНК"""
    base_complement = {'C': 'G', 'G': 'C', 'T': 'A', 'A': 'U'}
    rna = ''
    for nucleobase in dna:
        rna += base_complement[nucleobase]
    return rna


def translate_rna_to_protein(rna: str) -> list:
    """Функция на информационной матрицы последовательности РНК
    находит подпоследовательности белков.Учтено что каждая подпоследовательность
    беклов должна начинать с кодона AUG и заканчиваться Stop кодоном, остальные
    нуклеотиды считаются соеденительными"""
    global codon2amin_table
    pattern = r'(AUG([ACGU]{3})*?(UAA|UGA|UAG))'
    codons_sequences = [groups[0] for groups in re.findall(pattern, rna)]
    proteins = []
    for sequence in codons_sequences:
        protein = ''
        while sequence:
            codon = sequence[0:3]
            sequence = sequence[3:]
            protein += codon2amin_table[codon]
        proteins.append(protein)
    return proteins


def count_nucleotides(dna: str) -> Counter:
    """ Функция считатет количество вхождений
    нуклеотидов в последоваетльность ДНК"""
    return Counter(dna)


codon2amin_table = {}
with open(r'files/rna_codon_table.txt', 'r') as codon_file:
    for table_line in codon_file:
        table_line = table_line.rstrip().split()
        for i in range(0, len(table_line), 2):
            codon2amin_table[table_line[i]] = table_line[i + 1]

genes = []
with open(r'files/dna.fasta', 'r') as fasta_file:
    for line in fasta_file:
        line = line.rstrip()
        if line[0] == '>':
            current_gene = {'name': line[1:],
                            'dna_sequence': ''}
            genes.append(current_gene)
        else:
            current_gene['dna_sequence'] += line

with open('statistic.data', 'w') as statistic_file:
    for gene in genes:
        statistic_file.write(f'{gene["name"]}: \n')
        gene['statistic'] = dict(count_nucleotides(gene['dna_sequence']))
        statistic_file.writelines(f'{gene["statistic"]}\n')

# Отображение статистики
for gene in genes:
    fig1 = plt.figure()
    for name in gene['statistic']:
        plt.bar(x=name, height=(gene['statistic'][name]))
    plt.title(f'Статистика генома: {gene["name"]}')
    plt.xlabel('Нуклеотид')
    plt.ylabel('Частота')
    # plt.show()
    plt.savefig(f'Статистика генома-{gene["name"]}', dpi=600)

with open('rna.data', 'w') as rna_file:
    for gene in genes:
        rna_file.write(f'{gene["name"]}: \n')
        gene['rna_sequence'] = translate_from_dna_to_rna(gene['dna_sequence'])
        rna_file.write(gene['rna_sequence'] + '\n')

with open('protein.data', 'w') as protein_file:
    for gene in genes:
        protein_file.write(f'{gene["name"]}: \n')
        gene['proteins'] = translate_rna_to_protein(gene['rna_sequence'])
        for number, protein in enumerate(gene['proteins']):
            protein_file.write(f'protein{number}: {protein}\n')
