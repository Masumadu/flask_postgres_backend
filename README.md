<div align="center">
  <h1><b>FLASK POSTGRES BACKEND APPLICATION</b></h1>
  <h4>A Design Template For Building Enterprise Level Backend Applications Using Flask And Postgres</h4>
</div>

## 📗 Table of Contents

- [📖 About the Project](#about-project)
  - This is a flask backend application architecture to help developers kickstart their
  - development without worrying about how to structure, design or architect their projects.
  - Developers a free to clone the project and modify it to suit their needs.
    - [👀 Overview](#overview)
      - Design template for enterprise level backend application using flask.
    - [🛠 Built With](#built-with)
      - Python
      - Poetry
      - Docker
      - Docker Compose
      - [🔥 Tech Stack](#tech-stack)
        - Flask
        - Postgres
        - Redis
      - [🔑 Key Features](#key-features)
        - Factory Design Pattern
        - Decorator Pattern
        - Clean Code Approach
        - Model View Controller (MVC) Design Pattern
- [💪 Motivation](#motivation)
  - When I started as a python backend developer, I always struggled when it comes to designing,
  - structuring or architecting my application to suit the growing needs of my clients.
  - I read a lot of books about software architecture and design principles. These helped
  - me to come up with this design to help serve as a template for new developers. This can
  - serve as a guide for new python developers to build upon.
- [💻 Getting Started](#getting-started)
  - [📜 Prerequisites](#prerequisites)
    - python3
    - python3-venv
    - poetry
    - postgres
    - redis
    - docker
    - docker-compose
    - git
  - [⚓ Install](#setup)
    - install the various tools listed under prerequisite on your local machine
    - for instructions on how to install and set up these tools, please check their websites for directions
  - [⚙️ Setup](#install)
    - from your terminal, navigate to your preferred directory location on your machine
    - clone the repository into a directory of your choice
    - navigate into this directory
  - [▶️ Run Application](#run-application)
    - without docker:
      - create a virtual environment and activate it by executing below commands
        - for linux, run
          1. `python3 -m venv venv`
          2. `source venv/bin/activate`
        - for windows, run
          1. `python3 -m venv venv`
          2. `venv\Scripts\activate`
      - with the virtual environment activated, run blow commands to install dependencies
          1. `poetry install`
      - after installing dependencies, run below command to start application
          1. `flask run -p 5000`
    - with docker:
      - run below command:
        - `docker-compose up`
  - [🕹️ Usage](#usage)
    - access application on http://localhost:5000
    - test endpoint from swagger documentation
  - [💯 Run tests](#run-tests)
    - To run the unit tests cases, run below command
      - `pytest -v`
  - [🚀 Deployment](#triangular_flag_on_post-deployment)
    - deployed to docker hub registry using github actions.
- [👥 Author](#author)
  - Michael Asumadu
    - email ✉️ : michaelasumadu10@gmail.com
    - country 🌍 : Ghana 🇬🇭
    - contact 📞 : +233 247 049 596
- [⭐️ Show your support](#support)
  - If you like this project, please leave a star 😁
- [🙏 Acknowledgements](#acknowledgements)
  - Thanks to everyone who helped
- [❓ FAQ (OPTIONAL)](#faq)
  - **Can I reuse this code?**
    - Yes, feel free to fork it
  - **Can we improve it?**
    - Yes, feel free to send a pull request
