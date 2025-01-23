# National Parks Application

This Flask application manages national parks data, user accounts, bookings, and more. It includes functionalities for 
both normal users and admin users, allowing users to register, log in, view parks, create and manage bookings, and view 
wildlife and trail information. Admin users can also manage park registrations and updates.

## Features

- **User Authentication**
    - User Registration
    - User Login/Logout
    - Password Hashing for Security
    - User Roles (Admin and Regular User)

- **Park Information**
    - View Parks
    - Create and Update Parks (Admin Only)
    - View Wildlife and Trails for Specific Parks
    - View and Manage Announcements for Parks
    - Feedback from other users' experiences

- **Bookings**
    - Create, Update, and Delete Bookings
    - View All Bookings (User-Specific)

- **Weather Information**
    - Fetch Weather Data for a Park on a Specific Date

- **Feedback**
  - Submit feedbacks based on personal park visits

## Installation

### Prerequisites

Make sure you have the following installed:
- Python 3.7+
- Flask
- Flask-Login
- SQLAlchemy
- SQLite (for the database)
- Werkzeug
- secrets

### Steps to Install

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/nourheneltaief/npa


### Steps to Run

- pip install -r requirements.txt
- cd app && python app.py
