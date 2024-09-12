import json
from http.server import BaseHTTPRequestHandler, HTTPServer

books = []

class BooksAPI(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/books':
            self._send_response(200, books)
        elif self.path.startswith('/books/'):
            try:
                book_id = int(self.path.split('/')[-1])
                book = next((book for book in books if book["id"] == book_id), None)
                if book:
                    self._send_response(200, book)
                else:
                    self._send_response(404, {"message": "Livro não encontrado"})
            except ValueError:
                self._send_response(400, {"message": "ID inválido"})
        else:
            self._send_response(404, {"message": "Caminho não encontrado"})

    def do_POST(self):
        if self.path == '/books':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                new_book = json.loads(post_data)
                if "id" in new_book and "title" in new_book and "author" in new_book:
                    books.append(new_book)
                    self._send_response(201, new_book)
                else:
                    self._send_response(400, {"message": "Faltam campos obrigatórios"})
            except json.JSONDecodeError:
                self._send_response(400, {"message": "JSON inválido"})

    def do_PUT(self):
        if self.path.startswith('/books/'):
            try:
                book_id = int(self.path.split('/')[-1])
                content_length = int(self.headers['Content-Length'])
                put_data = self.rfile.read(content_length)
                updated_book = json.loads(put_data)

                for book in books:
                    if book["id"] == book_id:
                        book["title"] = updated_book.get("title", book["title"])
                        book["author"] = updated_book.get("author", book["author"])
                        self._send_response(200, book)
                        return
                self._send_response(404, {"message": "Livro não encontrado"})
            except ValueError:
                self._send_response(400, {"message": "ID inválido"})
            except json.JSONDecodeError:
                self._send_response(400, {"message": "JSON inválido"})

    def do_DELETE(self):
        if self.path.startswith('/books/'):
            try:
                book_id = int(self.path.split('/')[-1])
                global books
                books = [book for book in books if book["id"] != book_id]
                self._send_response(200, {"message": "Livro deletado"})
            except ValueError:
                self._send_response(400, {"message": "ID inválido"})

    def _send_response(self, status, data):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=BooksAPI, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Servindo na porta {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
