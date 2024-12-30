from flask import Flask, render_template, request
from fpdf import FPDF
import google.generativeai as genai

app = Flask(__name__)

genai.configure(api_key="")
model = genai.GenerativeModel("gemini-1.5-flash")

def generate_resume_content(name, email, phone, skills, experience,address,education):
    prompt = f"""
    Generate a professional resume based on the following details:

    Name: {name}
    Email: {email}
    Phone: {phone}
    Skills: {skills}
    Experience: {experience}
    Address:{address}
    Education:{education}

    Format the response with sections for Summary, Skills, Experience, and Education.
    """
    
    response = model.generate_content(prompt)
    return response.text.strip()

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/generate', methods=['POST'])
def generate():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    skills = request.form['skills']
    experience = request.form['experience']
    address =request.form['address']
    education=request.form['education']

    resume_content = generate_resume_content(name, email, phone, skills, experience,address,education)

    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('DejaVu', '', 'static/fonts/DejaVuSans.ttf', uni=True)
    pdf.set_font('DejaVu', '', 12)
    pdf.multi_cell(0, 10, resume_content)
    
    output_file = "static/resume.pdf"
    pdf.output(output_file)

    return render_template('result.html', pdf_path=output_file)

if __name__ == '__main__':
    app.run(debug=True)
