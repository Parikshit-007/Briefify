from django.shortcuts import render
import openpyxl
from django.http import HttpResponse
from webapp.models import ExcelFile
import pandas as pd
def upload(request):
    if request.method == 'POST' and request.FILES['file']:
        # Get the uploaded file from the request
        file = request.FILES['file']
        
        # Save the file to the database
        excel_file = ExcelFile()
        excel_file.file = file
        excel_file.save()

        # Open the uploaded Excel file with openpyxl
        wb = openpyxl.load_workbook(excel_file.file)
        
        # Create an HttpResponse object with the Excel file content
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename={}'.format(excel_file.file.name)

        # Write the Excel file content to the response
        wb.save(response)

        return response

    return render(request, 'uploadd.html')

def display(request, file_id):
    # Get the ExcelFile object by its ID
    excel_file = ExcelFile.objects.get(id=file_id)
    
    # Read the Excel file and convert it into a Pandas DataFrame
    df = pd.read_excel(excel_file.file.path)
    
    # Pass the DataFrame to the template
    context = {'df': df}
    return render(request, 'displayy.html', context)
