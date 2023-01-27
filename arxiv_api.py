import requests as r
import pandas as pd
import json
import xmltodict

def print_xml_tree(root, level=0):
    for child in root:
        print(''.join(['--' for i in range(level)]), child.tag, '||', child.text)
        print_xml_tree(child, level=level+1)




def parse_dict_or_list(obj, key):
    string = ''
    if type(obj) == type([]):
        string = ', '.join([a.get(key, '') for a in obj])
    else:
        string = obj.get(key, '')
    return string


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
    data = xmltodict.parse(data)
    
    print(json.dumps(data, indent=4))

    rows = []

    entries = data['feed']['entry']
    for entry in entries:

        rows.append({
            "id": entry["id"],
            "title": entry["title"], 
            "published": entry["published"],
            "author": parse_dict_or_list(entry['author'], 'name'),#author,
            "summary": entry['summary'],
            "link": entry["id"],
            "category": parse_dict_or_list(entry['category'], '@term'),
        })
    
    print(rows)
    

 
    df = pd.DataFrame(rows)
    return df


if __name__ == '__main__':
    query = input('search query: ')
    file_name = input('save to file: ')
    print('-------')
    df = get_arxiv_data(query)
    print('saving data...')
    df.to_csv(file_name)
    print('done!')
