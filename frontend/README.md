# Mathtastic Frontend

Welcome to the **Mathtastic Frontend**, a Vue.js-based web application designed to make math learning fun and engaging! Mathtastic features interactive activities like the Balance Scale Game, where students balance scales using weights to master addition and problem-solving skills. This frontend integrates with a FastAPI backend and Firebase for authentication and data management.

![Mathtastic Frontend Demo](https://res.cloudinary.com/dz3aj0ti8/image/upload/v1745082026/Screenshot_2025-04-19_at_10.30.01_PM_pykv6l.png)  

![Mathtastic Gameplay](https://res.cloudinary.com/dz3aj0ti8/image/upload/v1745078757/Screen_Recording_2025-04-14_at_4.18.26_PM_pcwl6m.gif)

## Table of Contents
- [About](#about)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Environment Setup](#environment-setup)
- [Running the Application](#running-the-application)
- [Project Structure](#project-structure)
- [Development](#development)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## About
Mathtastic is an educational platform aimed at transforming math learning through personalized, playful experiences. The frontend, built with Vue.js, provides an intuitive interface for students and educators, integrating with a FastAPI backend for game logic and Firebase for user authentication and progress tracking. This project aligns with Comini Learning’s vision of microschools and online platforms like Zippie, offering tools for customizable learning activities.

## Features
- **Interactive Games**: Play the Balance Scale Game to learn addition with visual feedback.
- **Firebase Authentication**: Secure login and user management with email/password and social providers.
- **Tailwind CSS**: Responsive and customizable styling for a modern UI.
- **Activity Builder**: Allows educators to create and configure games with adjustable difficulty levels.
- **Progress Tracking**: Stores user progress and achievements via Firebase Firestore.
- **Cross-Device Support**: Optimized for desktops, tablets, and mobile devices.

## Prerequisites
- Node.js 16.x or higher
- npm or yarn
- Vue CLI (for initial setup, optional with Vite)
- Firebase account (for authentication and Firestore)
- Git

## Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur).

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

Firebase variables

`VITE_apiKey`

`VITE_authDomain`

`VITE_projectId`

`VITE_storageBucket`

`VITE_messagingSenderId`

`VITE_appId`

`VITE_measurementId`

Backend Host URL

`VITE_BACKEND_HOST`

## Run Locally

Clone the project

```bash
  git clone https://github.com/Csb-218/MathTastic.git
```

Go to the project directory

```bash
  cd frontend
```
Run in dev mode 

```
npm run dev
```

Build the project

```
npm run build
```

Run in production

```
npm run preview
```

## Running Tests

To run tests, run the following command

```bash
  cd frontend
```
```bash
  npm run test
```
