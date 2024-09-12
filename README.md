# FitConnect

Welcome to **FitConnect**, a fitness web application designed to help you track your workouts, view your workout history, and stay motivated by connecting with others. Whether you're a seasoned gym-goer or someone just starting out (like the creator, who’s never set foot in a gym!), FitConnect is here to support your fitness journey.

## Table of Contents

- [Project Overview](#project-overview)
- [How FitConnect Came to Be](#how-fitconnect-came-to-be)
- [Key Features](#key-features)
- [How to Launch on Your PC](#how-to-launch-on-your-pc)
- [Technologies Used](#technologies-used)
- [Contact Information](#contact-information)

---

## Project Overview

FitConnect helps users:
- **Track workouts**: Log your daily exercises, including time, type, and intensity.
- **View workout history**: Review your past workouts and see your progress over time.
- **Connect socially**: Although the social feature is a future update, this aims to allow users to interact and motivate each other in their fitness endeavors.

## How FitConnect Came to Be

FitConnect was born out of my personal fitness struggles. As someone who hasn't been to the gym yet (yes, you read that right!), I was looking for a way to stay active and hold myself accountable, all while connecting with others on a similar journey. The result? FitConnect, a place where you can track progress, stay motivated, and eventually, flex your social muscles (pun intended).

Also, if you've ever found yourself wondering whether walking from the fridge to the couch counts as cardio – you’re in the right place.

## Key Features

- **Workout Tracking**: Log exercises and track your fitness journey over time.
- **Workout History**: Access a detailed history of your past workouts.
- **Simple and Clean Design**: A responsive and visually appealing interface themed in shades of green, blue, and white.

## How to Launch on Your PC

Follow the steps below to set up **FitConnect** on your local machine.

### Prerequisites
- Python (version 3.8 or higher)
- Virtualenv (optional but recommended)
- SQLite (no installation required, it's included with Python)

### Step 1: Clone the Repository

bash
git clone https://github.com/PreciousEzeigbo/Portfolio_project.git
```bash
cd Portfolio_project
```
### Step 2: Set Up a Virtual Environment (Optional but Recommended)
```bash

python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```
### Step 3: Install Dependencies

```bash

pip install -r requirements.txt
```
### Step 4: Initialize the SQLite Database

```bash

flask db upgrade

# This will set up the database for FitConnect. We're using SQLite, so you don't need any additional setup.
```
### Step 5: Run the App

```bash

flask run

# The app will be available at http://127.0.0.1:5000. Now you can start tracking your workouts!
```
### Step 6: Troubleshooting

If you encounter any issues, make sure:

    You’ve activated your virtual environment.
    All dependencies have been installed (pip install -r requirements.txt).
    The database migration ran without errors.

### Technologies Used

    Python: For the backend models(PS, that's what I'm more familiar with at the moment). 
    Flask: For building the web app and routing.
    Flask-Migrate: For database migrations.
    SQLite: For the database (simple and lightweight).
    HTML/CSS: For the frontend interface.
    JavaScript: For interactivity.

## Contact Information

Developed by Precious Ezeigbo, a tech enthusiast who turned personal fitness challenges into a powerful solution. Let's build a healthier future together!
- **GitHub**: PreciousEzeigbo
- **LinkedIn**: Precious Ezeigbo
- **X**: preciousezeigbo

Feel free to reach out if you have questions, suggestions, or just want to chat about fitness (or lack thereof)!

### Fun Facts & Jokes
```bash
    Why did the gym close down? It just didn’t work out! 💪
    I built this app so I could work on my fitness without actually working on my fitness. 😅
    The only lifting I’ve been doing lately is lifting this project to GitHub.
````
## css


Feel free to tweak it further, but this version includes all the details for setting up the app, its backstory, and some jokes to keep things lighthearted!
