from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

def search_helper(search_key, query, request):
    if request.args.get('search'):
        search_object = {}
        regex = re.compile(request.args.get('search'), re.IGNORECASE)
        search_object[search_key] = regex
        query = query.where(search_object)
        return query
    return query

def paginate_helper(model, query, request):
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('limit', 6))
    skip = (page - 1) * page_size

    regex = re.compile(request.args.get('search', ''), re.IGNORECASE)
    total = model.count_documents({"title": regex})

    pages = math.ceil(total / page_size)

    query = query.skip(skip).limit(page_size)

    return {
        'query': query,
        'page': page,
        'pages': pages
    }

@app.route('/your_endpoint', methods=['GET'])
def your_endpoint():
    # Connect to your MongoDB database
    client = MongoClient('mongodb://your-mongodb-uri')
    db = client.your_database_name
    collection = db.your_collection_name

    # Example usage of the helpers
    your_query = collection.find({})

    your_query = search_helper("your_search_key", your_query, request)
    pagination_result = paginate_helper(collection, your_query, request)

    return jsonify({
        'your_data': list(pagination_result['query']),
        'page': pagination_result['page'],
        'pages': pagination_result['pages']
    })

if __name__ == '__main__':
    app.run(debug=True)
