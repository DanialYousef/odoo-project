import math

from odoo import http
from odoo.http import request
import json
from urllib.parse import parse_qs

def valid_response(data ,pagination_info , status):
    response = {
        "data" : data
    }
    if pagination_info:
        response["pagination_info"] = pagination_info
    return request.make_json_response(response , status=status)

class PropertyApi(http.Controller):
    def validation_name(self, vals, name="name"):
        if not vals.get(name):
            return True
        else: return False

    # @http.route("/v1/property/http" , methods=["POST"] , type="http" , auth="none" , csrf=False )
    # def property_create_endpoint(self):
    #     args = request.httprequest.data.decode()
    #     vals = json.loads(args)
    #     if self.validation_name(vals):
    #         return request.make_json_response({
    #             "message": "column name is required",
    #         }, status=400)
    #     try:
    #         res =  request.env['property'].sudo().create(vals)
    #         if res:
    #             return request.make_json_response({
    #                 "message" : "success",
    #                 "id" : res.id,
    #                 "name" : res.name
    #             },status =201)
    #         return None
    #     except Exception as error:
    #         return request.make_json_response({
    #             "message": error
    #
    #         }, status=400)
    @http.route("/v1/property/http" , methods=["POST"] , type="http" , auth="none" , csrf=False )
    def property_create_endpoint(self):
        args = request.httprequest.data.decode()
        vals = json.loads(args)
        if self.validation_name(vals):
            return request.make_json_response({
                "message": "column name is required",
            }, status=400)
        try:
            cr = request.env.cr
            columns =', '.join(vals.keys())
            values =', '.join(['%s'] * len(vals))
            query = f"""INSERT INTO property ({columns}) VALUES ({values}) RETURNING id ,name , postcode"""
            cr.execute(query , tuple(vals.values()))
            res = cr.fetchone()
            print(res)
            if res:
                return request.make_json_response({
                    "message" : "success",
                    "id" : res[0],
                    "name" : res[1],
                    "postcode" :res[2]
                },status =201)
            return None
        except Exception as error:
            return request.make_json_response({
                "message": error

            }, status=400)

    @http.route("/v1/property/json", methods=["POST"], type="json", auth="none", csrf=False)
    def property_json_end_point(self):
        args = request.httprequest.data.decode()
        vals = json.loads(args)
        res = request.env['property'].sudo().create(vals)
        if res:
            return [{
                "message" : "success",
            }]
        return None

    @http.route("/v1/property/update/<int:property_id>" , methods=["put"], type="json", auth="none", csrf=False)
    def property_update_endpoint(self , property_id):
        property_ids = request.env['property'].sudo().search([('id' , '=' , property_id)])
        print(property_ids)
        args = request.httprequest.data.decode()
        vals = json.loads(args)
        print(vals)
        property_ids.write(vals)
        print(property_ids.name)
        return {
            "message": "property has been updated successfully",
            "id": property_ids.id,
            "name": property_ids.name,
        },

    @http.route("/v1/property/get/<int:property_id>" , methods=["GET"], type="http", auth= "none", csrf=False)
    def property_get_endpoint(self , property_id):
        try:
            property_ids = request.env['property'].sudo().search([('id', '=', property_id)])
            if not property_ids:
                return request.make_json_response({
                    "message": "property not found",
                }, status=400)
            return valid_response({
                "id": property_ids.id,
                "name": property_ids.name,
                "active" : property_ids.active,
                "description" : property_ids.description,
                "data_availability" : property_ids.data_availability,
                "data_selling_expected" : property_ids.data_selling_expected,
                "expected_price" : property_ids.expected_price,
                "selling_price": property_ids.selling_price,
                "bedrooms" : property_ids.bedrooms,
                "state" : property_ids.state,
            } , status=200)

        except Exception as error:
            return request.make_json_response({
                "message": error
            } , status=400)

    @http.route("/v1/property/delete/<int:property_id>" , methods=["DELETE"] ,type="http", auth="none" , csrf=False)
    def property_delete_endpoint(self , property_id):
         try:
             property_ids = request.env['property'].sudo().search([('id', '=', property_id)])
             if not property_ids:
                 return request.make_json_response({
                     "message": "property not found",
                 }, status=400)
             property_ids.unlink()
             return request.make_json_response({
                 "message": "property has been deleted successfully",
                 "property_id" : property_ids.id
             })
         except Exception as error:
             return request.make_json_response({
                 "error": error
            } , status=400)

    @http.route("/v1/property/list" , methods=["GET"], type="http", auth= "none", csrf=False)
    def property_get_list_endpoint(self):
        try:
            params = parse_qs(request.httprequest.query_string.decode("utf-8"))
            print(params)
            property_domain = []
            page = offset = None
            limit = 5
            if params:
                if params.get('page'):
                    page = int(params['page'][0])
                    print(page)
                if params.get('limit'):
                    limit = int(params['limit'][0])
                    print(limit)
                offset = (page * limit) - limit
            if params.get("state"):
                property_domain += [("state", "=", params["state"][0])]
            property_ids = request.env['property'].sudo().search(property_domain , offset = offset , limit = limit)
            print(property_ids)
            property_count = request.env['property'].sudo().search_count(property_domain)
            print(property_count)
            if not property_ids:
                return request.make_json_response({
                    "message": "there are no records",
                }, status=400)
            return valid_response([{
                "id": property_id.id,
                "name": property_id.name,
                "active" : property_id.active,
                "description" : property_id.description,
                "data_availability" : property_id.data_availability,
                "data_selling_expected" : property_id.data_selling_expected,
                "expected_price" : property_id.expected_price,
                "selling_price": property_id.selling_price,
                "bedrooms" : property_id.bedrooms,
                "state" : property_id.state,
            } for property_id in property_ids  ], pagination_info={
                "page": page if page else 1 ,
                "limit" : limit,
                "pages" : math.ceil(property_count / limit) if limit else 1,
                "count" : property_count
             } , status=200)
        except Exception as error:
            return request.make_json_response({
                "message": error
            } , status=400)








