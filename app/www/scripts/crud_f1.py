from scripts.f1_queries import queries

def get_select_options(body=None):
    options = []
    for i, query in enumerate(queries):
        options.append({
            "index": i,
            "title": query["title"],
            "description": query["description"],
            
        })
    return options

if __name__ == "__main__":
    result = get_select_options()
    print(result)


