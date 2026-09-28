from flask import Flask, request, render_template
import os
import PyPDF2
import docx2txt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()
os.environ["HF_TOKEN"]=os.getenv("HF_TOKEN")

model=SentenceTransformer("all-MiniLM-L6-v2")





app=Flask(__name__)
app.config['UPLOAD_FOLDER']='uploads/'


def extract_txt_pdf(file_path):

    text=""
    with open(file_path,'rb') as file:
        reader=PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()

    return text

def extract_txt_doc(file_path):
    return docx2txt.process(file_path)

def extract_txt_txt(file_path):
    with open(file_path,'r',encoding="utf-8") as file:
            return file.read()


def extract_txt(file_path):
    if file_path.endswith(".pdf"):
        return extract_txt_pdf(file_path)
    elif file_path.endswith(".docx"):
        return extract_txt_doc(file_path)
    elif file_path.endswith(".txt"):
        return extract_txt_txt(file_path)
    else :
        return ""
    
    
@app.route("/")
def matchResume():
    return render_template("matchresume.html")

@app.route("/matcher",methods=['GET','POST'])
def matcher():
    if request.method=='POST':
        jd=request.form.get('job_description')
        resume_files=request.files.getlist('resumes')

        resumes=[]

        for resume_file in resume_files:
            filename=os.path.join(app.config["UPLOAD_FOLDER"],resume_file.filename)
            resume_file.save(filename)
            resumes.append(extract_txt(filename))

        if not resumes or not jd:
            return render_template('matchresume.html',message="Please upload resumes and enter job description")


        
        jd_vector=model.encode([jd])
        resumes_vectors=model.encode(resumes)
        similarities=cosine_similarity(jd_vector,resumes_vectors)[0]

        top_indices=similarities.argsort()[-5:][::-1]
        top_resumes=[resume_files[i].filename for i in top_indices]
        score=[round(similarities[i],2) for i in top_indices ]


        return render_template('matchresume.html',message="Top matching resumes:",top_resumes=top_resumes, similarity_scores=score)
    
    return render_template('matchresume.html')

# @app.route("/matcher",methods=['GET','POST'])
# def matcher():
#     if request.method=='POST':
#         jd=request.form.get('job_description')
#         resume_files=request.files.getlist('resumes')

#         resumes=[]

#         for resume_file in resume_files:
#             filename=os.path.join(app.config["UPLOAD_FOLDER"],resume_file.filename)
#             resume_file.save(filename)
#             resumes.append(extract_txt(filename))

#         if not resumes or not jd:
#             return render_template('matchresume.html',message="Please upload resumes and enter job description")


#         vectorizer=TfidfVectorizer().fit_transform([jd] + resumes)
#         vectors=vectorizer.toarray()
#         jd_vector=vectors[0]
#         resumes_vectors=vectors[1:]
#         similarities=cosine_similarity([jd_vector],resumes_vectors)[0]

#         top_indices=similarities.argsort()[-5:][::-1]
#         top_resumes=[resume_files[i].filename for i in top_indices]
#         score=[round(similarities[i],2) for i in top_indices ]


#         return render_template('matchresume.html',message="Top matching resumes:",top_resumes=top_resumes, similarity_scores=score)
    
#     return render_template('matchresume.html')

# @app.route("/matcher", methods=["POST"])
# def matcher1():

    # Get job description
    jd = request.form.get("job_description")

    # Get multiple resumes
    resume_files = request.files.getlist("resumes")

    if not jd:
        return jsonify({
            "error": "Job description is required"
        }), 400

    if not resume_files:
        return jsonify({
            "error": "At least one resume is required"
        }), 400

    resumes = []
    resume_names = []

    for resume_file in resume_files:

        if resume_file.filename == "":
            continue

        text = extract_txt(resume_file)

        if text.strip():
            resumes.append(text)
            resume_names.append(resume_file.filename)

    if not resumes:
        return jsonify({
            "error": "Could not extract text from any resume"
        }), 400

   
    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform([jd] + resumes)

    jd_vector = vectors[0]
    resume_vectors = vectors[1:]

    
    similarities = cosine_similarity(
        jd_vector,
        resume_vectors
    )[0]

    
    top_indices = similarities.argsort()[-3:][::-1]

    top_resumes = []

    for index in top_indices:

        top_resumes.append({
            "filename": resume_names[index],
            "similarity_score": round(float(similarities[index]), 2)
        })

    return jsonify({
        "message": "Top 3 matching resumes",
        "results": top_resumes
    })

if __name__ == "__main__":
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
