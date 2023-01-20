import urllib, urllib.request
import xml.etree.ElementTree as Xet
from xml.etree.ElementTree import fromstring, ElementTree
import requests as r
import pandas as pd


def print_xml_tree(root, level=0):
    for child in root:
        print(''.join(['--' for i in range(level)]), child.tag, '||', child.text)
        print_xml_tree(child, level=level+1)


def get_arxiv_data(q):
    print('fetching data...')
    url = 'http://export.arxiv.org/api/query'
    data = r.get(url, params={
        'search_query': q, 
        'start':0, 
        'max_results':10000
    })
    print('parsing data...')
    data = data.content.decode('utf-8')
    cols = ["title", "published", 'author', "summary",]
    rows = []
    # print(data)
    

    # Parsing the XML file
    root = ElementTree(fromstring(data)).getroot()
    print('meta data: ')
    for row in root[:7]:
        start_ind = row.tag.find('}')
        print('--', row.tag[start_ind+1 if start_ind != -1 else 0 :], ': ', row.text)

    # print_xml_tree(root)

    for child in root:
        if 'entry' in child.tag:
            row = {}
            names = []
            for elem in child:
                for c in cols:
                    if 'author' in elem.tag:
                        for name in elem:
                            names.append(name.text)
                        break
                    elif c in elem.tag:
                        row[c] = elem.text
                        break
            row['author'] = ','.join(names)
            rows.append(row)
 
    df = pd.DataFrame(rows, columns=cols)
    return df


if __name__ == '__main__':
    query = input('search query: ')
    file_name = input('save to file: ')
    print('-------')
    df = get_arxiv_data(query)
    print('saving data...')
    df.to_csv(file_name)
    print('done!')