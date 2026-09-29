from flask import Flask, request, render_template
import os
import PyPDF2
import docx2txt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import re

SKILLS_DB = [

    'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'c',
    'ruby', 'go', 'golang', 'rust', 'swift', 'kotlin', 'php', 'r',
    'scala', 'perl', 'matlab', 'dart', 'lua', 'objective-c',
    'groovy', 'shell scripting', 'powershell', 'bash','html', 'html5', 'css', 'css3', 'sass', 'scss', 'less',
    'bootstrap', 'tailwind css', 'tailwind','javascript', 'typescript','react', 'react.js', 'reactjs','angular', 'angular.js', 
    'vue', 'vue.js', 'vuejs',
    'next.js', 'nextjs', 'nuxt', 'nuxt.js',
    'jquery', 'redux', 'redux toolkit',
    'material ui', 'mui',
    'chakra ui', 'webpack', 'vite',
    'babel', 'web components',
    'responsive design',

    'node.js', 'nodejs', 'express', 'express.js',
    'django', 'flask', 'fastapi',
    'spring', 'spring boot', 'spring mvc',
    'spring security', 'spring cloud',
    'spring data jpa', 'hibernate',
    'laravel', 'rails', 'ruby on rails',
    '.net', 'asp.net', 'asp.net core',
    'entity framework',
    'nestjs', 'nest.js',
    'gin', 'fiber',

    'rest', 'rest api', 'restful api',
    'graphql', 'grpc',
    'websocket', 'websockets',
    'soap', 'api development',
    'microservices', 'monolithic architecture',
    'event-driven architecture',
    'serverless',
    'api gateway',
    'load balancing',
    'scalability',

    'artificial intelligence', 'ai',
    'machine learning', 'ml',
    'deep learning',
    'supervised learning',
    'unsupervised learning',
    'reinforcement learning',
    'transfer learning',
    'feature engineering',
    'model training',
    'model evaluation',
    'hyperparameter tuning',
    'classification',
    'regression',
    'clustering',
    'time series',
    'recommendation systems',

    'nlp', 'natural language processing',
    'text classification',
    'sentiment analysis',
    'text preprocessing',
    'tokenization',
    'stemming',
    'lemmatization',
    'named entity recognition',
    'ner',
    'pos tagging',
    'word embeddings',
    'word2vec',
    'glove',
    'tf-idf',
    'text mining',

    'computer vision',
    'image processing',
    'image classification',
    'object detection',
    'image segmentation',
    'face recognition',
    'ocr',
    'optical character recognition',
    'opencv',
    'yolo',
    'yolov5',
    'yolov8',
    'yolov9',
    'yolov10',
    'yolov11',
    'ssd',
    'faster r-cnn',
    'mask r-cnn',
    'mediapipe',
    'pillow',

    'tensorflow',
    'pytorch',
    'keras',
    'scikit-learn',
    'xgboost',
    'lightgbm',
    'catboost',
    'numpy',
    'pandas',
    'scipy',
    'matplotlib',
    'seaborn',
    'plotly',
    'statsmodels',

    'generative ai',
    'genai',
    'generative ai models',
    'large language models',
    'llm',
    'llms',
    'prompt engineering',
    'prompt design',
    'fine-tuning',
    'llm fine-tuning',
    'rag',
    'retrieval augmented generation',
    'vector database',
    'embeddings',
    'text generation',
    'chatbots',
    'ai agents',
    'agentic ai',
    'multimodal ai',

    'langchain',
    'langgraph',
    'llamaindex',
    'llama index',
    'hugging face',
    'huggingface',
    'transformers',
    'openai',
    'openai api',
    'ollama',
    'groq',
    'anthropic',
    'gemini',
    'google gemini',
    'mistral',
    'llama',
    'pydantic',

    'sql',
    'mysql',
    'postgresql',
    'postgres',
    'sqlite',
    'oracle',
    'mariadb',
    'sql server',
    'microsoft sql server',
    'pl/sql',
    't-sql',

    'mongodb',
    'redis',
    'firebase',
    'firestore',
    'dynamodb',
    'cassandra',
    'couchdb',
    'neo4j',
    'elasticsearch',
    'opensearch',

    'data engineering',
    'data pipeline',
    'etl',
    'elt',
    'data warehouse',
    'data lake',
    'apache spark',
    'spark',
    'pyspark',
    'hadoop',
    'hive',
    'kafka',
    'apache kafka',
    'airflow',
    'apache airflow',
    'databricks',
    'snowflake',
    'dbt',

    'aws',
    'amazon web services',
    'ec2',
    's3',
    'lambda',
    'rds',
    'ecs',
    'eks',
    'cloudformation',
    'azure',
    'microsoft azure',
    'azure functions',
    'azure devops',
    'gcp',
    'google cloud',
    'google cloud platform',
    'compute engine',
    'cloud storage',
    'bigquery',

    'docker',
    'docker compose',
    'kubernetes',
    'k8s',
    'terraform',
    'ansible',
    'jenkins',
    'github actions',
    'gitlab ci',
    'ci/cd',
    'continuous integration',
    'continuous deployment',
    'helm',
    'prometheus',
    'grafana',
    'nginx',
    'apache',
    'linux',
    'ubuntu',
    'bash',
    'shell scripting',

    'git',
    'github',
    'gitlab',
    'bitbucket',
    'svn',
    'version control',
    'git branching',
    'pull requests',

    'unit testing',
    'integration testing',
    'system testing',
    'functional testing',
    'test automation',
    'pytest',
    'unittest',
    'junit',
    'mockito',
    'selenium',
    'cypress',
    'playwright',
    'postman',
    'jmeter',

    'core java',
    'java 8',
    'java 11',
    'java 17',
    'java 21',
    'oops',
    'object oriented programming',
    'jdbc',
    'servlets',
    'jsp',
    'maven',
    'gradle',
    'spring boot',
    'spring framework',
    'spring mvc',
    'spring security',
    'spring data',
    'spring cloud',
    'hibernate',
    'jpa',

    'data structures',
    'data structures and algorithms',
    'dsa',
    'algorithms',
    'object oriented programming',
    'oops',
    'design patterns',
    'system design',
    'low level design',
    'high level design',
    'software development',
    'software engineering',
    'debugging',
    'problem solving',
    'code review',

    'data analysis',
    'data analytics',
    'data science',
    'excel',
    'advanced excel',
    'power bi',
    'tableau',
    'looker',
    'qlik',
    'business intelligence',
    'data visualization',
    'statistics',
    'statistical analysis',

    'android',
    'android development',
    'android studio',
    'ios',
    'ios development',
    'flutter',
    'react native',
    'swiftui',
    'jetpack compose',

    'cybersecurity',
    'information security',
    'network security',
    'application security',
    'ethical hacking',
    'penetration testing',
    'owasp',
    'owasp top 10',
    'authentication',
    'authorization',
    'jwt',
    'oauth',
    'oauth2',
    'ssl',
    'tls',
    'encryption',

    'computer networks',
    'tcp/ip',
    'http',
    'https',
    'dns',
    'dhcp',
    'vpn',
    'firewall',
    'networking',
    'socket programming',

    'postman',
    'swagger',
    'openapi',
    'jira',
    'confluence',
    'notion',
    'vs code',
    'visual studio',
    'intellij idea',
    'eclipse',
    'jupyter notebook',
    'anaconda',

    'agile',
    'scrum',
    'kanban',
    'devops',
    'tdd',
    'bdd',
    'waterfall',

    'communication',
    'leadership',
    'teamwork',
    'problem solving',
    'critical thinking',
    'analytical skills',
    'time management',
    'project management',
    'collaboration',
    'technical documentation',

]


# load_dotenv()
# os.environ["HF_TOKEN"]=os.getenv("HF_TOKEN")

# model=SentenceTransformer("all-MiniLM-L6-v2")





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

# ─────────────────────────────────────────────
# 🔧 Extraction Functions
# ─────────────────────────────────────────────

# ── Email ──────────────────────────────────────
def extract_email(text):
    """Extract first email address found in the text."""
    pattern = r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}'
    match = re.search(pattern, text)
    return match.group() if match else None


# ── Phone ──────────────────────────────────────
def extract_phone(text):
    """Extract first phone number (handles +91, dashes, dots, spaces)."""
    pattern = r'(\+?\d[\d\s\-().]{7,15}\d)'
    matches = re.findall(pattern, text)
    for m in matches:
        digits_only = re.sub(r'\D', '', m)
        if 7 <= len(digits_only) <= 15:
            return m.strip()
    return None


# ── Name ───────────────────────────────────────
# Strategy: the name is usually on one of the first non-empty lines,
# before any label like 'email:', 'phone:', etc.
def extract_name(text):
    """Heuristic: first short non-label line that looks like a proper name."""
    lines = text.strip().split('\n')
    SKIP_LABELS = re.compile(
        r'^(email|phone|mobile|address|linkedin|github|website|summary|objective|name\s*:)',
        re.IGNORECASE
    )
    NAME_PATTERN = re.compile(r'^[A-Z][a-z]+(\s[A-Z][a-z]+){1,3}$')
    for line in lines[:10]:           # check first 10 lines only
        stripped = line.strip()
        if not stripped:
            continue
        if SKIP_LABELS.match(stripped):
            # Try extracting the value after the colon
            if ':' in stripped:
                val = stripped.split(':', 1)[1].strip()
                if NAME_PATTERN.match(val):
                    return val
            continue
        if NAME_PATTERN.match(stripped):
            return stripped
    return None

def extract_skills(text):
    """Match known skills from text (case-insensitive)."""
    text_lower = text.lower()
    found = [
        skill for skill in SKILLS_DB
        if re.search(r'(?<![a-z])' + re.escape(skill) + r'(?![a-z])', text_lower)
    ]
    return list(dict.fromkeys(found))  

EDUCATION_KEYWORDS = [
    'b.tech', 'b.e', 'b.sc', 'b.com', 'b.a', 'bca', 'bba',
    'm.tech', 'm.e', 'm.sc', 'm.com', 'm.a', 'mca', 'mba',
    'phd', 'ph.d', 'bachelor', 'master', 'doctorate',
    'high school', 'secondary', 'diploma', '12th', '10th',
    'university', 'college', 'institute',
]

SECTION_STOP = re.compile(
       r'^(experience|skills|projects|certifications|achievements|languages|publications)',
       re.IGNORECASE
)

def extract_education(text):
    """Grab lines under the Education section or containing education keywords."""
    lines = text.split('\n')
    results, in_section = [], False

    for line in lines:
        s = line.strip()
        if not s:
            continue
        if re.search(r'\b(education|academic|qualification)\b', s, re.IGNORECASE):
            in_section = True
            continue
        if in_section and SECTION_STOP.match(s):
            break
        if in_section and len(s) > 4:
            results.append(s)
        elif any(kw in s.lower() for kw in EDUCATION_KEYWORDS) and s not in results:
            results.append(s)

    return results if results else None


# ── Experience ─────────────────────────────────
EXPERIENCE_STOP = re.compile(
    r'^(education|skills|projects|certifications|achievements|languages|publications)',
    re.IGNORECASE
)

def extract_experience(text):
    """Grab lines under the Experience / Work History section."""
    lines = text.split('\n')
    results, in_section = [], False

    for line in lines:
        s = line.strip()
        if not s:
            continue
        if re.search(r'\b(experience|work history|employment|professional experience)\b', s, re.IGNORECASE):
            in_section = True
            continue
        if in_section and EXPERIENCE_STOP.match(s):
            break
        if in_section and len(s) > 4:
            results.append(s)

    return results if results else None


# ── Master function ─────────────────────────────
def extract_all(text):
    """Run all extractors and return a structured dictionary."""
    return f"""
        Name : {extract_name(text)},
        Email : {extract_email(text)},
        Phone : {extract_phone(text)},
        Skills : {extract_skills(text)},
        Education : {extract_education(text)},
        Experience : {extract_experience(text)},
        """
        

print('✅ All extraction functions defined!')
    
    
@app.route("/")
def matchResume():
    return render_template("matchresume.html")

# @app.route("/matcher",methods=['GET','POST'])
# def matcher():
#     if request.method=='POST':
#         jd=request.form.get('job_description')
#         resume_files=request.files.getlist('resumes')

#         resumes=[]

#         for resume_file in resume_files:
#             filename=os.path.join(app.config["UPLOAD_FOLDER"],resume_file.filename)
#             resume_file.save(filename)
#             resumes.append(extract_all(extract_txt(filename)))

#         if not resumes or not jd:
#             return render_template('matchresume.html',message="Please upload resumes and enter job description")


#         job_desc=extract_all(jd)
        
#         jd_vector=model.encode([job_desc])
#         resumes_vectors=model.encode(resumes)
#         similarities=cosine_similarity(jd_vector,resumes_vectors)[0]

#         top_indices=similarities.argsort()[-5:][::-1]
#         top_resumes=[resume_files[i].filename for i in top_indices]
#         score=[round(similarities[i],2) for i in top_indices ]


#         return render_template('matchresume.html',message="Top matching resumes:",top_resumes=top_resumes, similarity_scores=score)
    
#     return render_template('matchresume.html')

@app.route("/matcher",methods=['GET','POST'])
def matcher():
    if request.method=='POST':
        jd=request.form.get('job_description')
        resume_files=request.files.getlist('resumes')

        resumes=[]

        for resume_file in resume_files:
            filename=os.path.join(app.config["UPLOAD_FOLDER"],resume_file.filename)
            resume_file.save(filename)
            resumes.append(extract_all(extract_txt(filename)))

        if not resumes or not jd:
            return render_template('matchresume.html',message="Please upload resumes and enter job description")
        job_desc=extract_all(jd)

        vectorizer=TfidfVectorizer().fit_transform([job_desc] + resumes)
        vectors=vectorizer.toarray()
        jd_vector=vectors[0]
        resumes_vectors=vectors[1:]
        similarities=cosine_similarity([jd_vector],resumes_vectors)[0]

        top_indices=similarities.argsort()[-5:][::-1]
        top_resumes=[resume_files[i].filename for i in top_indices]
        score=[round(similarities[i],2) for i in top_indices ]


        return render_template('matchresume.html',message="Top matching resumes:",top_resumes=top_resumes, similarity_scores=score)
    
    return render_template('matchresume.html')


#@app.route("/matcher", methods=["POST"])
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
