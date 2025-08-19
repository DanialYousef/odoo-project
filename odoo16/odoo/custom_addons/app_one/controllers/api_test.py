from odoo import http

class ApiTest(http.Controller):

    @http.route("/api/test" , methods=["GET"] , type="http" , auth="none" , csrf=False)
    def test_end_point(self):
        print("inside test_end_point")