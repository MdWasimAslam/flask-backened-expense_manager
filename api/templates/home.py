import streamlit as st
import speech_recognition as sr
import pyaudio
import wave
import requests
# Initialize the recognizer
recognizer = sr.Recognizer()

print("Welcome to the speech recognition")
st.title("Speech Recognition")
st.write("Press the button and speak")

st.markdown('<div>', unsafe_allow_html=True)

if st.button("Start Recording"):
    # PyAudio parameters
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "output.wav"

    audio = pyaudio.PyAudio()

    # Start recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    st.write("Recording...")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    st.write("Finished recording.")

    # Stop recording
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save the recorded data as a WAV file
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    # Use the recognizer to convert the audio to text
    with sr.AudioFile(WAVE_OUTPUT_FILENAME) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            st.write("You said: " + text)
        except sr.UnknownValueError:
            st.write("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            st.write("Could not request results from Google Speech Recognition service; {0}".format(e))

st.markdown('</div>', unsafe_allow_html=True)




# Custom CSS styling for the page
st.markdown(
    """
    <style>
    .stButton > button {
        background-color: #FF5733;
        color: white;
        font-size: 16px;
        border-radius: 8px;
        padding: 10px 20px;
    }
    .stButton > button:hover {
        background-color: #FF4500;
        color: white;
        opacity: 0.9;
    }
    .stButton > button:active {
        background-color: #FF6347;
        color: white;
        opacity: 0.7;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Job Description Generator")
st.write("Fill in the details below to generate a job description.")

# Form container with improved styling
with st.form(key="my_form"):
    
    # Text input fields
    company = st.text_input(label="Enter the company name:")
    role = st.text_input(label="Enter the role:")
    technicalSkill = st.text_input(label="Enter the technical skill that you are hiring for:")
    location = st.text_input(label="Enter the location:")
    experience = st.text_input(label="Enter the years of experience:")
    
    # Job type selection
    jobType = st.selectbox("Select the job type:", ["Full-time", "Part-time", "Contract", "Internship"])
    
    # Number of openings
    position = st.number_input(label="Enter the number of Openings:", value=0)
    
    # Salary inputs in two columns
    col1, col2 = st.columns(2)
    with col1:
        min_salary = st.number_input(label="Min Salary", value=0)
    with col2:
        max_salary = st.number_input(label="Max Salary", value=0)
    
    # Submit button
    submit_button = st.form_submit_button(label="Generate Job Description")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Processing and displaying the result
if submit_button:
    # Validate form fields
    if not company or not role or not technicalSkill or not location or not experience or not jobType or position <= 0 or min_salary <= 0 or max_salary <= 0:
        st.error("Please fill in all the fields correctly.")
    else:
        with st.spinner("Processing..."):
            # Prepare the payload for the API request
            payload = {
                "company": company,
                "role": role,
                "technicalSkill": technicalSkill,
                "location": location,
                "experience": experience,
                "jobType": jobType,
                "position": position,
                "min_salary": min_salary,
                "max_salary": max_salary,
            }
            
            # Send the POST request to the API
            try:
                response = requests.post("http://127.0.0.1:5000/gemini/generate", json=payload)
                response.raise_for_status()  # Raise an exception for HTTP errors
                
                if response.status_code == 200:
                    try:
                        response_json = response.json()
                        job_description = response_json.get("response", "No description found.")
                        st.success("Job description generated successfully!")
                        
                        # Decode the job description if it's in bytes
                        if isinstance(job_description, bytes):
                            job_description = job_description.decode('utf-8')
                        
                        # Display the job description directly
                        st.markdown("### Job Description")
                        st.markdown(job_description)
                    except ValueError as e:
                        st.error(f"Error parsing JSON: {e}")
                else:
                    st.error(f"Failed to generate job description. Status code: {response.status_code}")
            except requests.exceptions.RequestException as e:
                st.error(f"An error occurred: {e}")