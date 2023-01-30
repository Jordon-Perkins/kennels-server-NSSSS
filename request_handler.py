import json
from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer
from views import (get_all_animals, get_single_animal, get_all_customers, 
get_single_customer, get_all_employees, get_all_locations, get_single_employee, 
get_single_location, create_animal, create_customer, create_employee, create_location, 
delete_animal, delete_customer, delete_employee, delete_location, update_animal, 
update_location, update_customer, update_employee, get_customers_by_email, get_animals_by_location_id,
get_employees_by_location_id, get_animals_by_status)





# Here's a class. It inherits from another class.
# For now, think of a class as a container for functions that
# work together for a common purpose. In this case, that
# common purpose is to respond to HTTP requests from a client.
class HandleRequests(BaseHTTPRequestHandler):
    # This is a Docstring it should be at the beginning of all classes and functions
    # It gives a description of the class or function
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server
    """

    def parse_url(self, path):
        url_components = urlparse(path)
        path_params = url_components.path.strip("/").split("/")
        query_params = []

        if url_components.query != '':
            query_params = url_components.query.split("&")

        resource = path_params[0]
        id = None

        try:
            id = int(path_params[1])
        except IndexError:
            pass  # No route parameter exists: /animals
        except ValueError:
            pass  # Request had trailing slash: /animals/

        return (resource, id, query_params)

    def do_GET(self):
        self._set_headers(200)

        response = {}

        # Parse URL and store entire tuple in a variable
        parsed = self.parse_url(self.path)

        # If the path does not include a query parameter, continue with the original if block
        # if '?' not in self.path:
        (resource, id, query_params) = parsed

        if resource == "animals":
            if id is not None:
                response = get_single_animal(id)
            else:
                response = get_all_animals(query_params)
        elif resource == "customers":
            if id is not None:
                response = get_single_customer(id)
            else:
                response = get_all_customers()
        elif resource == "employees":
            if id is not None:
                response = get_single_employee(id)
            else:
                response = get_all_employees()
        elif resource == "locations":
            if id is not None:
                response = get_single_location(id)
            else:
                response = get_all_locations()

        # else: # There is a ? in the path, run the query param functions
        #     (resource, id, query) = parsed

        #     # see if the query dictionary has an email key
        #     if query.get('email') and resource == 'customers':
        #         response = get_customers_by_email(query['email'][0])
        #     elif query.get('location_id') and resource == 'animals':
        #         response = get_animals_by_location_id(query['location_id'][0])
        #     elif query.get('location_id') and resource == 'employees':
        #         response = get_employees_by_location_id(query['location_id'][0])
        #     elif query.get('status') and resource == 'animals':
        #         response = get_animals_by_status(query['status'][0])


        self.wfile.write(json.dumps(response).encode())



    

    def do_PUT(self):
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id, query_params) = self.parse_url(self.path)

        success = False

        if resource == "animals":
            success = update_animal(id, post_body)
        # rest of the elif's

        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)

        self.wfile.write("".encode())


    def do_POST(self):
        status_code = 201
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id, query_params) = self.parse_url(self.path)

        # Add a new animal to the list. Don't worry about
        # the orange squiggle, you'll define the create_animal
        # function next.
        if resource == "animals":
            new_animal = None
            new_animal = create_animal(post_body)
            self._set_headers(status_code)
            self.wfile.write(json.dumps(new_animal).encode())

        elif resource == "customers":
            new_customer = None
            new_customer = create_customer(post_body)
            self._set_headers(status_code)
            self.wfile.write(json.dumps(new_customer).encode())

        elif resource == "employees":
            new_employee = None
            new_employee = create_employee(post_body)
            self._set_headers(status_code)
            self.wfile.write(json.dumps(new_employee).encode())

        elif resource == "locations":
            address_does_exist = "address" in post_body.keys()
            name_does_exist = "name" in post_body.keys()
            if not name_does_exist:
                response = {"message": "name is required"}
                status_code = 400
            elif not address_does_exist:
                response = {"message": "address is required"}
                status_code = 400
            else:
                response = create_location(post_body)

            self._set_headers(status_code)
            self.wfile.write(json.dumps(response).encode())



    def _set_headers(self, status):
        # Notice this Docstring also includes information about the arguments passed to the function
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.
    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    def do_DELETE(self):
    # Set a 204 response code
        status_code = 204
        response = {}

    # Parse the URL
        (resource, id, query_params) = self.parse_url(self.path)

    # Delete a single animal from the list
        if resource == "animals":
            delete_animal(id)

        elif resource == "customers":
            if id is not None:
                status_code = 405
                response = { "message": "Please contact the company directly to authorize the deletion of a customer" }
            #delete_customer(id)

        elif resource == "employees":
            delete_employee(id)

        elif resource == "locations":
            delete_location(id)

        self._set_headers(status_code)
        self.wfile.write(json.dumps(response).encode())


# This function is not inside the class. It is the starting
# point of this application.
def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
