import elasticsearch
es = elasticsearch.Elasticsearch('172.16.37.40:9200')
query_string = r'{ "query": { "match_all": {} }}'
res = es.delete_by_query(index='vpn', doc_type='user_info', body=query_string)
#es.delete_by_query(index='vpn', doc_type='start_used_vpn', body=query_string)
#es.delete_by_query(index='vpn', doc_type='used_vpn', body=query_string)

print(res)