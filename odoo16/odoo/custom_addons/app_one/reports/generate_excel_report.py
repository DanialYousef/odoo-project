from docutils.nodes import literal

from odoo import http
from odoo.http import request
import io
import xlsxwriter
from ast import literal_eval



class GenerateExcelReport(http.Controller):

    @http.route('/property/excel/report/<string:property_ids>' , type='http', auth='user')
    def property_excel_report(self ,property_ids):

        property_ids= request.env['property'].browse(literal_eval(property_ids))
        print(property_ids)
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output , {'in_memory': True})
        worksheet = workbook.add_worksheet('properties')

        header_format = workbook.add_format({'bold' : True , 'bg_color' : '#D3D3D3' , 'border' : 1 , 'align':'center'})
        string_format = workbook.add_format({'num_format' : '$##,###00.00' , 'border' : 1 , 'align':'center'})

        headers = ['Name' , 'Postcode' , 'Selling Price' , 'Gardens']
        for col_number,header in enumerate(headers):
            worksheet.write(0, col_number, header, header_format)
        row_number = 1
        for property in property_ids:
            worksheet.write(row_number , 0 , property.name ,string_format)
            worksheet.write(row_number, 1, property.postcode ,string_format)
            worksheet.write(row_number, 2, property.selling_price,string_format)
            worksheet.write(row_number, 3, 'Yes' if property.garden else 'No' ,string_format)
            row_number += 1


        workbook.close()
        output.seek(0)

        file_name = 'Property Report.xlsx'
        return request.make_response(
            output.getvalue(),
            headers=[
                ('Content-type' , 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                ('Content-Disposition' , f'attachment ; filename={file_name}'),
            ]
        )