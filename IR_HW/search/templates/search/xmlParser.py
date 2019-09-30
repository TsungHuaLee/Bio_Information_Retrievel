import xml.etree.ElementTree as ET
import sys
import re

PATH = "./PubmedArticleSet/PubmedArticle/MedlineCitation/Article"

tree = ET.parse('./data/pubmed19n.xml')
root = tree.getroot()
print(root.tag)
for country in root.findall('./PubmedArticle/MedlineCitation/Article'):
    rank = country.find('ArticleTitle').text
    print(rank)
