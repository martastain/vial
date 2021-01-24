Vial
====

Vial is a web nano-framework. Smaller than flask or bottle, just one class with a few convenience methods.

 - Vial is WSGI compliant, you may use Gunicorn or the built-in wsgiref server.
 - There is no router, all requests are handled using one method. Use if statements.
 - Static files should be served by a reverse proxy server such as NGINX or Caddy.