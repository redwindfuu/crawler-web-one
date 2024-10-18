from flask import Flask, request, jsonify
import src.services.category as category_service

app = Flask(__name__)


@app.route('/category', methods=['GET'])
def get_category():
    result = category_service.get_category()
    return jsonify({'category': result , 'status': 200})

@app.route('/category/posts', methods=['GET'])
def get_category_by_name():
    # query parameter
    category_name = request.args.get('url_name')
    page = request.args.get('page') or 0
    result = category_service.get_post_by_category(category_name , page)
    return jsonify({'category': result , 'status': 200})

@app.route('/category/posts/detail', methods=['GET'])
def get_post_detail():
    # query parameter
    post_url = request.args.get('url')
    result = category_service.get_post_detail(post_url)
    return jsonify({'data': result , 'status': 200})



if __name__ == '__main__':
    app.run(debug=True)