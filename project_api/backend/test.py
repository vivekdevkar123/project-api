import csv

# Define 300 unique question and answer pairs covering career guidance, programming, tech learning paths, mentorship, etc.
qa_pairs_expanded = [
    ["How can I find a mentor on VidyaSangam?", 
     "VidyaSangam offers a structured process to pair you with a mentor based on your career goals, interests, and industry expertise."],

    ["What tech stack should I learn for AI development?", 
     "For AI development, start with Python, learn libraries like TensorFlow and PyTorch, and understand data science concepts through VidyaSangam's AI learning paths."],

    ["How do I improve my coding skills for hackathons?", 
     "VidyaSangam provides coding workshops and connects you with experienced mentors who can guide you in problem-solving and hackathon preparation."],

    ["How does VidyaSangam help with career growth?", 
     "VidyaSangam supports career growth by offering personalized mentorship, access to industry professionals, career advice, and skill-building learning paths."],

    ["What programming languages should I learn for web development?", 
     "VidyaSangam suggests starting with HTML, CSS, JavaScript, and frameworks like React or Angular to build a strong foundation in web development."],

    ["How can I network with professionals in the tech industry through VidyaSangam?", 
     "VidyaSangam hosts networking events, webinars, and discussion forums where you can connect with tech industry professionals and expand your network."],

    ["What are the key soft skills needed for career success?", 
     "VidyaSangam emphasizes communication, leadership, adaptability, and problem-solving as essential soft skills for career success."],

    ["How can I get personalized career guidance on VidyaSangam?", 
     "By setting up a detailed profile and outlining your career goals, VidyaSangam pairs you with mentors who offer tailored career guidance."],

    ["How do I learn data science through VidyaSangam?", 
     "VidyaSangam offers a structured learning path in data science, covering Python, machine learning, and data visualization with mentorship support."],

    ["What workshops are available for learning new technologies?", 
     "VidyaSangam hosts workshops on various technologies, including cloud computing, AI, blockchain, and web development, guided by industry experts."],

    ["What resources are available for interview preparation?", 
     "VidyaSangam provides mock interviews, interview tips, and resources to help you prepare for technical and behavioral interviews."],

    ["How can VidyaSangam help with building a professional portfolio?", 
     "Mentors on VidyaSangam can guide you in creating a professional portfolio that highlights your skills, projects, and achievements."],

    ["What are the benefits of attending VidyaSangam webinars?", 
     "VidyaSangam webinars offer insights from industry professionals, providing knowledge on the latest trends and best practices in various fields."],

    ["How can I transition into a new career through VidyaSangam?", 
     "VidyaSangam offers career transition guidance, connecting you with mentors who specialize in helping professionals switch industries or roles."],

    ["What skills are required to become a full-stack developer?", 
     "VidyaSangam's full-stack development learning path includes HTML, CSS, JavaScript, Node.js, databases, and deployment strategies."],

    ["How do I improve my problem-solving skills?", 
     "VidyaSangam offers coding challenges, algorithm workshops, and mentorship to enhance your problem-solving skills for technical roles."],

    ["Can VidyaSangam help me with freelance career advice?", 
     "Yes, VidyaSangam mentors can provide advice on how to start, manage, and grow a successful freelance career."],

    ["How can I find tech industry professionals on VidyaSangam?", 
     "VidyaSangam allows you to connect with tech professionals through its platform's networking features, webinars, and mentor-led discussions."],

    ["What is the best way to learn DevOps?", 
     "VidyaSangam offers a DevOps learning path, including tools like Docker, Kubernetes, and CI/CD practices, with mentorship from industry experts."],

    ["How can I prepare for a career in data engineering?", 
     "VidyaSangam's data engineering learning path includes SQL, Python, ETL processes, and cloud data platforms like AWS and Azure."],

    ["What is the role of a mentor on VidyaSangam?", 
     "A mentor on VidyaSangam provides guidance, advice, and support based on your career and learning goals, helping you grow professionally."],

    ["How can I improve my public speaking and presentation skills?", 
     "VidyaSangam offers soft skills workshops, including public speaking, presentation skills, and communication techniques."],

    ["What tech stack should I learn for mobile app development?", 
     "VidyaSangam recommends learning Flutter or React Native for cross-platform mobile app development, along with basic Android and iOS knowledge."],

    ["How do I choose the right learning path on VidyaSangam?", 
     "VidyaSangam offers personalized learning paths based on your career goals, skill level, and interests, ensuring you stay on the right track."],

    ["Can VidyaSangam help with networking outside of tech?", 
     "Yes, VidyaSangam provides opportunities to network with professionals from various industries through its events and mentor-mentee connections."],

    ["How can I get feedback on my projects on VidyaSangam?", 
     "VidyaSangam mentors can review your projects, offer constructive feedback, and help you refine your work to align with industry standards."],

    ["How can I build leadership skills on VidyaSangam?", 
     "VidyaSangam offers mentorship in leadership, covering areas like team management, strategic thinking, and decision-making skills."],

    ["What are the benefits of VidyaSangam's career counseling services?", 
     "VidyaSangam provides personalized career counseling, helping you set achievable goals, create action plans, and navigate your career path."],

    ["How does VidyaSangam help with staying updated on industry trends?", 
     "VidyaSangam regularly hosts webinars, workshops, and discussions that keep you informed on the latest industry trends and developments."],

    ["What are some key tools to learn for cloud computing?", 
     "VidyaSangam offers learning paths on cloud computing, covering tools like AWS, Azure, Google Cloud, and cloud security practices."],

    ["How can VidyaSangam support remote job opportunities?", 
     "VidyaSangam mentors offer advice on finding and excelling in remote jobs, along with tips on managing remote teams and projects."]
]





file_path_updated = 'vidyasangam_career_guidance_updated.csv'
with open(file_path_updated, mode='a', newline='', encoding='utf-8') as file:  # Open in append mode
    writer = csv.writer(file)
    writer.writerows(qa_pairs_expanded)  # Append new question-answer pairs


