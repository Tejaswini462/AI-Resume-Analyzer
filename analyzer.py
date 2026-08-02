import spacy
import PyPDF2
import difflib

nlp = spacy.load("en_core_web_sm")

skills_database = {

"data scientist":[
"python","machine learning","pandas","numpy",
"sql","data analysis","statistics","matplotlib"
],

"ml engineer":[
"python","machine learning","tensorflow",
"pytorch","numpy","pandas","deep learning"
],

"ai engineer":[
"python","machine learning","deep learning",
"tensorflow","pytorch","nlp","computer vision"
],

"backend developer":[
"java","spring","sql","rest api","microservices"
],

"software developer":[
"java","python","sql","data structures",
"algorithms","git"
],

"frontend developer":[
"html","css","javascript","react","bootstrap","ui"
]

}


def extract_text(file):

    reader = PyPDF2.PdfReader(file)

    text=""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text

    return text.lower()



def extract_skills(text):

    found_skills=[]

    for role in skills_database.values():
        for skill in role:
            if skill in text and skill not in found_skills:
                found_skills.append(skill)

    return found_skills



def find_closest_role(role):

    roles=list(skills_database.keys())

    match=difflib.get_close_matches(role,roles,n=1)

    if match:
        return match[0]

    return None



def predict_role(found_skills):

    best_role=None
    best_score=0

    for role,skills in skills_database.items():

        match_count=0

        for skill in skills:
            if skill in found_skills:
                match_count+=1

        if match_count>best_score:
            best_score=match_count
            best_role=role

    return best_role



def analyze_resume(text,role):

    role=role.lower().strip()

    found_skills=extract_skills(text)

    if role=="":
        role=predict_role(found_skills)

    if role not in skills_database:
        closest=find_closest_role(role)
        if closest:
            role=closest

    required_skills=skills_database.get(role,[])

    matched=[]
    missing=[]

    for skill in required_skills:

        if skill in found_skills:
            matched.append(skill)

        else:
            missing.append(skill)

    if len(required_skills)==0:
        score=0
    else:
        score=int((len(matched)/len(required_skills))*100)

    return matched,missing,score,role