import json

books = []

def handler(event, context):
    method = event.get('httpMethod', 'GET')
    path = event.get('path', '')

    if method == 'GET':
        if path == '/books':
            return _response(200, books)
        elif path.startswith('/books/'):
            try:
                book_id = int(path.split('/')[-1])
                book = next((book for book in books if book["id"] == book_id), None)
                if book:
                    return _response(200, book)
                else:
                    return _response(404, {"message": "Livro não encontrado"})
            except ValueError:
                return _response(400, {"message": "ID inválido"})
        else:
            return _response(404, {"message": "Caminho não encontrado"})

    elif method == 'POST':
        try:
            body = json.loads(event['body'])
            if "id" in body and "title" in body and "author" in body:
                books.append(body)
                return _response(201, body)
            else:
                return _response(400, {"message": "Faltam campos obrigatórios"})
        except json.JSONDecodeError:
            return _response(400, {"message": "JSON inválido"})

    elif method == 'PUT' and path.startswith('/books/'):
        try:
            book_id = int(path.split('/')[-1])
            body = json.loads(event['body'])
            for book in books:
                if book["id"] == book_id:
                    book["title"] = body.get("title", book["title"])
                    book["author"] = body.get("author", book["author"])
                    return _response(200, book)
            return _response(404, {"message": "Livro não encontrado"})
        except ValueError:
            return _response(400, {"message": "ID inválido"})
        except json.JSONDecodeError:
            return _response(400, {"message": "JSON inválido"})

    elif method == 'DELETE' and path.startswith('/books/'):
        try:
            book_id = int(path.split('/')[-1])
            global books
            books = [book for book in books if book["id"] != book_id]
            return _response(200, {"message": "Livro deletado"})
        except ValueError:
            return _response(400, {"message": "ID inválido"})

    return _response(404, {"message": "Caminho não encontrado"})

def _response(status, body):
    return {
        'statusCode': status,
        'body': json.dumps(body),
        'headers': {
            'Content-Type': 'application/json'
        }
    }
