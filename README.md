
# Color Catcher Game

An interactive Python game that combines **computer vision**, **real-time object tracking**, and **game development**. Players control a paddle using a **blue-colored object** in front of a webcam to catch falling items.

---

## Table of Contents

- [Overview](#overview)  
- [Features](#features)  
- [Technologies Used](#technologies-used)  
- [Installation](#installation)  
- [Usage](#usage)  
- [How it Works](#how-it-works)  
- [Learning Outcomes](#learning-outcomes)  
- [License](#license)  

---

## Overview

The **Color Catcher Game** allows the player to interact with the game using a real-world object. A colored object (blue in this version) is tracked using **OpenCV** and **HSV color detection**, and its movement is used to control a paddle in real-time. The goal is to catch falling items to score points while avoiding misses.

---

## Features

- Real-time object tracking using OpenCV  
- Adjustable HSV sliders for accurate color detection  
- Smooth paddle movement with object tracking  
- Dynamic falling items with collision detection  
- Live camera preview for feedback  
- Progressive difficulty as the score increases  
- Fun and interactive gameplay  

---

## Technologies Used

- Python  
- OpenCV (Computer Vision)  
- NumPy (Array handling, calculations)  
- Pygame (Game interface and animations)  

---

## Installation

1. Clone this repository:

```bash
git clone https://github.com/yourusername/color-catcher-game.git
cd color-catcher-game

Install dependencies:

pip install opencv-python numpy pygame


Usage

Run the HSV calibration tool (optional, recommended for best results):
python calibrate_hsv.py

Run the main game:
python color_catcher_blue.py


