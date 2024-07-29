from flask import Blueprint, request, jsonify
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
import time



load_dotenv()

gemini = Blueprint('gemini', __name__)

@gemini.route('/generate', methods=['POST'])
def generate():
    
    request_data = request.get_json()
    print(request_data)
    company = request_data['company']
    role = request_data['role']
    technicalSkill = request_data['technicalSkill']
    location = request_data['location']
    experience = request_data['experience']
    jobType = request_data['jobType']
    position = request_data['position']
    min_salary = request_data['min_salary']
    max_salary = request_data['max_salary']
    
    
    # Load the model
    model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

    # Prepare messages for the model
    prompt = f"""Prepare a Small Job Description according to the requirement mentioned below: 
            Company Name: {company}
            Role: {role}
            Experience: {experience}
            Location: {location}
            Job Type: {jobType}
            Number of Openings: {position}
            Primary Skill Required for: {technicalSkill}
            Secondary Skill Required for: Skills that are not mandatory but will be an added advantage as pe the Primary Skill Mentioned Above.
            Salary range: {min_salary} - {max_salary}
            please provide the Job Description for the above requirement and no need to mention apply process.
            no need to mention about the company as well but just mention the company name.
            """
    messages = [
                 SystemMessage(content="You are a helpful AI assistant who suggests the Job Description according to the user's input."),
                 HumanMessage(content=prompt),
            ]

    # Generate responses
    response = model.invoke(messages)
    return jsonify({"response": response.content})


