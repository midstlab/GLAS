import json
import requests

def search_rcsb(ligand, is_loi=True):
    search_params = {
        "query": {
            "type": "group",
            "logical_operator": "and",
            "nodes": [
                {
                    "type": "terminal",
                    "service": "text",
                    "parameters": {
                        "attribute": "rcsb_nonpolymer_entity_annotation.comp_id",
                        "operator": "exact_match",
                        "negation": False,
                        "value": ligand
                    }
                }
            ],
            "label": "nested-attribute"
        },
        "return_type": "entry",
        "request_options": {
            "paginate": {
                "start": 0,
                "rows": 9999
            },
            "results_content_type": [
                "experimental"
            ],
            "sort": [
                {
                    "sort_by": "score",
                    "direction": "desc"
                }
            ],
            "scoring_strategy": "combined"
        }
    }

    if is_loi:
        search_params["query"]["nodes"].append({
            "type": "terminal",
            "service": "text",
            "parameters": {
                "attribute": "rcsb_nonpolymer_entity_annotation.type",
                "operator": "exact_match",
                "value": "SUBJECT_OF_INVESTIGATION",
                "negation": False
            }
        })
    else:
        search_params["query"]["nodes"].append({
            "type": "terminal",
            "service": "text",
            "parameters": {
                "attribute": "rcsb_nonpolymer_instance_feature_summary.type",
                "operator": "exact_match",
                "value": "HAS_COVALENT_LINKAGE",
                "negation": False
            }
        })

    search_request = json.dumps(search_params)
    response = requests.get(f"https://search.rcsb.org/rcsbsearch/v2/query?json={search_request}")
    data = json.loads(response.text)
    result_set = data['result_set']

    identifiers = [entry['identifier'] for entry in result_set]
    return identifiers

def process_ligands(ligands, is_loi=True):
    results = {}
    total_count = 0

    for ligand in ligands:
        ligand = ligand.strip()
        pdb_ids = search_rcsb(ligand, is_loi)
        filtered_ids = [pdb_id for pdb_id in pdb_ids if pdb_id not in {pdb_id for pdb_list in results.values() for pdb_id in pdb_list}]
        total_count += len(filtered_ids)
        results[ligand] = filtered_ids

    print(results)
    return results


