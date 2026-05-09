from flask import Flask, render_template, request, make_response
from rules import CountryRules

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        user_data = request.form.to_dict()
        
        # Calculate result based on the country
        if user_data.get('country') == 'UK':
            result = CountryRules.calculate_uk(user_data)
        
        if result:
            result['employee_name'] = user_data.get('employee_name', 'Employee')
        
        # Handle Document Generation Actions
        action = request.form.get('action')
        
        if action in ['internal', 'employee']:
            template = 'doc_internal.html' if action == 'internal' else 'doc_employee.html'
            return render_template(template, result=result, data=user_data)
        
        elif action == 'audit':
            # Create a CSV row for technical audit
            line = (f"{result['employee_name']},{user_data['end_date']},"
                    f"{user_data['annual_salary']},{result['statutory_pay']},"
                    f"{result['bonus_pay']},{result['total_package']}\n")
            
            response = make_response(line)
            filename = f"audit_{result['employee_name'].replace(' ', '_')}.csv"
            response.headers["Content-Disposition"] = f"attachment; filename={filename}"
            response.headers["Content-type"] = "text/csv"
            return response

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)