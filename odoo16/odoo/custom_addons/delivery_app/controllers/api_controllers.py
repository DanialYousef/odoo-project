from odoo import http
from odoo.http import request
import json
import uuid
from datetime import datetime, timedelta


class CustomerApi(http.Controller):
    def _validate_token(self):
        token = request.httprequest.headers.get('Authorization')
        if not token:
            return {
                'error' : 'No API key provided'
            }
        api_session = request.env['api.session'].sudo().search([('token', '=', token)])
        if not  api_session:
            return {
                'error' : 'Invalid or expired token.'
            }

        return  api_session.customer_id

    @http.route('/api/v1/order/create/<int:delivery_person_id>' , methods=['POST'] ,type='json', auth="none", csrf=False)
    def order_create(self ,delivery_person_id , **kwargs):
        delivery_person = request.env['res.users'].search([('id' ,'=', delivery_person_id)])
        if not delivery_person:
            return {
                "message":"This delivery person is not registered."
            }
        customer = self._validate_token()
        if not customer:
            return {
                'error' : 'No API key provided'
            }
        print(customer)
        delivery_gay = request.env['res.users'].search([('is_delivery_person','=',False)])
        print(delivery_gay)
        try:
            args = request.httprequest.data.decode()
            vals = json.loads(args)
            if not vals.get('name'):
                return  {
                    'error' : 'Name order is required'
                }
            res = request.env['delivery.order'].create({
                "name" : vals.get('name'),
                "customer_id" : customer.id,
                "delivery_person_id" :delivery_person_id,
                "order_lines": vals.get('order_lines' , [])
            })
            if res:
                return {
                    "message" : "Order created successfully",
                    "order_id": res.id,
                    "delivery_person_id": delivery_person_id,
                    "customer_id": customer,
                }
            else:
                return {
                    "message" : "Something went wrong",
                }
        except Exception as e:
            return {
                'error' : e
            }

    @http.route("/api/v1/get_users" , methods=['GET'] , type='json' , auth="none" , csrf=False)
    def get_users(self):
        persons = request.env['res.users'].search([])
        if not persons:
            return {
                "message" : "No users registered"
            }
        return [
            {
                "person_id" : person.id,
                "person_name" : person.name,
                "is_delivery_person" : person.is_delivery_person,
                "is_available" : person.is_available,
            }for person in persons]

    @http.route("/api/v1/get_order/<int:order_id>" , methods=['GET'] , type='json' , auth='none' , csrf=False)
    def get_order(self, order_id , **kwargs):
        customer = request.env['delivery.customer'].sudo().search([('id', '=', order_id)])
        if not customer:
            return {
                "error" : "Customer not found"
            }

        order_ids = request.env['delivery.order'].search([('customer_id.id', '=', order_id)])
        print(order_ids)
        return [{
            "message" : "Get order successfully",
            "order_name" : order_id.name,
            "order_id": order_id.id,
            "customer_name" : order_id.customer_id.name,
            "state" : order_id.state,

        }for order_id in order_ids]

    @http.route("/api/v1/get_order" , methods=['GET'] , type='json' , auth='none' , csrf=False)
    def get_orders(self, **kwargs):
        try:
            order_ids = request.env['delivery.order'].search([])
            if not order_ids:
                return {
                    "error" : "No orders found"
                }
            return {
                "message" : "Get orders successfully",
                "order_details" :[{
                    "order_name" : order_id.name,
                    "order_date" : order_id.order_date,
                    "order_id" : order_id.id,
                    "customer_id" : order_id.customer_id.id,
                    "state" :  order_id.state
                }for order_id in order_ids],
            }
        except Exception as e:
            return {
                "error" : e
            }

    @http.route('/api/v1/update_order/<int:order_id>' , method=['PUT'] , type='json' , auth='none' , csrf=False)
    def update_order(self, order_id , **kwargs):
        args = request.httprequest.data.decode()
        vals = json.loads(args)
        if not vals.get('state'):
            return {
                'error' : 'No state provided'
            }
        order_ids = request.env['delivery.order'].search([('id' , '=' , order_id)])
        old_state = order_ids.state
        if not order_ids:
            return {
                "error" : "No orders found"
            }
        order_ids.write(vals)
        return {
            "message" : "Update order successfully",
            "old_state" : old_state,
            "new_state" : order_ids.state,
        }
    @http.route('/api/v1/customer/create' , methods=['POST'] , type='json' , auth='none' , csrf=False)
    def create_customer(self, **kwargs):
        try:
            args = request.httprequest.data.decode()
            vals = json.loads(args)
            if not vals.get('name') or not vals.get('email') or not vals.get('password'):
                return {
                    "error" : 'Name , email , password are required'
                }

            customer = request.env['delivery.customer'].sudo().create(vals)
            new_token = str(uuid.uuid4())
            request.env['api.session'].sudo().create({
                'token': new_token,
                "customer_id": customer.id,
                'expiration_time': datetime.now() + timedelta(hours=1)
            })
            return {
                "Success" : True,
                "Customer_id" : customer.id,
                "name" : customer.name,
                "email" : customer.email,
                'message' : "Customer Created Successfully"
            }
        except Exception as error:
            return {
                "error" : str(error),
            }

    @http.route('/api/v1/customer/login' , methods=['POST'] , auth='none' , type='http' , csrf=False)
    def customer_login(self, **kwargs):
        args = request.httprequest.data.decode()
        vals = json.loads(args)
        if not vals.get('email') or not vals.get('password'):
            return request.make_json_response({
                "error": 'email , password are required'
            } , status=400)
        try:
            domain = [
                ('email' , '=' , vals.get('email') ),
                ('password' , '=' , vals.get('password') )
            ]
            customer = request.env['delivery.customer'].sudo().search(domain)
            if not customer:
                return request.make_json_response({
                    "error": "Customer Not Found"
                }, status=400)
            request.env['api.session'].sudo().search([('customer_id', '=', customer.id)]).unlink()

            new_token = str(uuid.uuid4())
            result = request.env['api.session'].sudo().create({
                'token': new_token,
                'customer_id': customer.id,
                "expiration_time": datetime.now() + timedelta(hours=24)
            })
            if result:
                return request.make_json_response({
                    "message": "Customer Login Successfully",
                    "customer_id": customer.id,
                    "new_token": new_token,
                }, status=200)
            else:
                return request.make_json_response({
                    "message": "Something went wrong",
                })
        except Exception as error:
            return request.make_json_response({
                "error" : str(error),
            })

    @http.route("/api/auth/logout", methods=["POST"], type="json", auth="none", csrf=False)
    def logout(self, **kwargs):
        customer = self._validate_token()
        if 'error' in customer:
            return {
                'error' : "customer error"
            }

        request.env['api.session'].sudo().search([('customer_id', '=', customer.id)]).unlink()
        return {'success': True, 'message': 'Logged out successfully.'}

    @http.route("/api/auth/profile", methods=["GET"], type="json", auth="none", csrf=False)
    def get_profile(self, **kwargs):
        customer = self._validate_token()
        if 'error' in customer:
            return customer

        return {'customer_id': customer.id, 'name': customer.name, 'email': customer.email}

