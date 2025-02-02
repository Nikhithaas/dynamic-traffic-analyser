# Dynamic Traffic Analyser 🎯


## Basic Details
### Team Name: ABC


### Team Members
- Member 1: A S Nikhitha - Mar Athanasius College of Engineering
- Member 2: Nima Wilson  - Mar Athanasius College of Engineering
- Member 3: Riya Roy     - Mar Athanasius College of Engineering

### Hosted Project Link


### Project Description
The Dynamic Traffic Controlling System is an intelligent solution designed to revolutionize urban traffic management. By leveraging real-time traffic data, advanced sensors, and machine learning algorithms, this system dynamically adjusts traffic signal timings to optimize traffic flow, minimize congestion, and enhance road safety. Whether it's rush hour or late at night, the system intelligently adapts to varying traffic conditions, ensuring a smoother and more efficient commute for everyone.

### The Problem statement
Urban areas around the world are facing increasing challenges related to traffic congestion, inefficient traffic management, and road safety. Traditional traffic signal systems often rely on fixed timing intervals or pre-set schedules, which do not adapt to real-time traffic conditions. This results in longer wait times at intersections, inefficient use of roadways, increased fuel consumption, and higher carbon emissions. During peak traffic hours or emergencies, these static systems can further exacerbate congestion, causing delays, frustration for commuters, and potential safety hazards. Furthermore, the current systems do not account for pedestrian safety or prioritize emergency vehicles in a way that ensures swift passage.

### The Solution
The Dynamic Traffic Controlling System is an intelligent solution designed to revolutionize urban traffic management. By leveraging real-time traffic data, advanced sensors, and machine learning algorithms, this system dynamically adjusts traffic signal timings to optimize traffic flow, minimize congestion, and enhance road safety. Whether it's rush hour or late at night, the system intelligently adapts to varying traffic conditions, ensuring a smoother and more efficient commute for everyone.

Key Features:
•	Real-Time Traffic Monitoring: Continuously analyses traffic data from sensors placed at intersections.
•	Adaptive Signal Timing: Adjusts signal patterns based on current traffic density to reduce congestion.
•	Peak Hour Optimization: Identifies peak traffic hours and adapts to handle high traffic volumes more efficiently.

## Technical Details
This code is detecting vehicles in a video stream by:
(BACK END)
1.	Comparing consecutive frames to identify vehicles.
2.	Counting how many vehicles cross a predefined line in the frame.
3.	Calculating traffic density based on vehicles per second.
4.	Calculating time elapsed
5.	Introducing 2 videos for reference that makes a connection between the traffic lights.
6.	When certain number of vehicles passes, the red-light changes to green for a limited time according to the density of vehicles in the incoming road. The outgoing road must stay at red light while the other is on green. Then this process happens vice versa too.
The system also uses some basic techniques like contour detection and centroid tracking to ensure vehicles are counted correctly while avoiding duplicates

(FRONT END)
1)	Created a website in which it inputs traffic flow in front of junction 1 and junction 2 separately.
2)	If we give a time elapse by 30 seconds , in junction 1 green light be ON and simultaneously in junction 2 red light should be ON.
3)	After the 30 secs duration is completed then then yellow light for the both junctions will be in yellow light for the vehicles to wait for the next action.
4)	Then it happens vice versa from step 2.

### Technologies/Components Used
For Software:
- Machine learning
- numpy, cv2, math, time, os, json
- cursor

### Implementation
For Software:
Website created
# Installation
VS code, cursor
# Run
[commands]

### Project Documentation
For Software:DYNAMIC TRAFFIC CONTROLLING SYSTEM

THE PROBLEM TO BE SOLVED

Urban areas around the world are facing increasing challenges related to traffic congestion, inefficient traffic management, and road safety. Traditional traffic signal systems often rely on fixed timing intervals or pre-set schedules, which do not adapt to real-time traffic conditions. This results in longer wait times at intersections, inefficient use of roadways, increased fuel consumption, and higher carbon emissions. During peak traffic hours or emergencies, these static systems can further exacerbate congestion, causing delays, frustration for commuters, and potential safety hazards. Furthermore, the current systems do not account for pedestrian safety or prioritize emergency vehicles in a way that ensures swift passage.

SOLUTION

The Dynamic Traffic Controlling System is an intelligent solution designed to revolutionize urban traffic management. By leveraging real-time traffic data, advanced sensors, and machine learning algorithms, this system dynamically adjusts traffic signal timings to optimize traffic flow, minimize congestion, and enhance road safety. Whether it's rush hour or late at night, the system intelligently adapts to varying traffic conditions, ensuring a smoother and more efficient commute for everyone.

Key Features:
•	Real-Time Traffic Monitoring: Continuously analyses traffic data from sensors placed at intersections.
•	Adaptive Signal Timing: Adjusts signal patterns based on current traffic density to reduce congestion.
•	Peak Hour Optimization: Identifies peak traffic hours and adapts to handle high traffic volumes more efficiently.

WHAT WE ACTUALLY DO

This code is detecting vehicles in a video stream by:
(BACK END)
1.	Comparing consecutive frames to identify vehicles.
2.	Counting how many vehicles cross a predefined line in the frame.
3.	Calculating traffic density based on vehicles per second.
4.	Calculating time elapsed
5.	Introducing 2 videos for reference that makes a connection between the traffic lights.
6.	When certain number of vehicles passes, the red-light changes to green for a limited time according to the density of vehicles in the incoming road. The outgoing road must stay at red light while the other is on green. Then this process happens vice versa too.
The system also uses some basic techniques like contour detection and centroid tracking to ensure vehicles are counted correctly while avoiding duplicates

(FRONT END)
1)	Created a website in which it inputs traffic flow in front of junction 1 and junction 2 separately.
2)	If we give a time elapse by 30 seconds , in junction 1 green light be ON and simultaneously in junction 2 red light should be ON.
3)	After the 30 secs duration is completed then then yellow light for the both junctions will be in yellow light for the vehicles to wait for the next action.
4)	Then it happens vice versa from step 2.


# Screenshots (Add at least 3)

![image](https://github.com/user-attachments/assets/60f804c8-13d6-48b8-aaf7-38f71e8d7853)
the number of vehicles passing in 10 second
![ee9f21eb-033b-455e-a7b9-067b855ce905](https://github.com/user-attachments/assets/a6b542b9-9698-4b6a-b52e-a19635d6728d)
this displays green in junction 1 and red in junction 2 for 30 second
![e3228004-b0c3-41b4-9198-f93ec3b01bf5](https://github.com/user-attachments/assets/2fe2d855-b7f5-4d86-ba39-cb642d44a3b1)
this displays red in junction 1 and green in junction 2 for 30 second
![a6151989-440b-4df6-b2d7-740b107c00b2](https://github.com/user-attachments/assets/f60d3f5c-f94b-47a1-b35d-b0ff08fd02f2)
Displays yellow light in both sides for 5 second

# Diagrams
![Workflow](Add your workflow/architecture diagram here)
*Add caption explaining your workflow*

For Hardware:

# Schematic & Circuit
![Circuit](Add your circuit diagram here)
*Add caption explaining connections*

![Schematic](Add your schematic diagram here)
*Add caption explaining the schematic*

# Build Photos
![Team](Add photo of your team here)


![Components](Add photo of your components here)
*List out all components shown*

![Build](Add photos of build process here)
*Explain the build steps*

![Final](Add photo of final product here)
*Explain the final build*

### Project Demo
# Video
[Add your demo video link here]
*Explain what the video demonstrates*

# Additional Demos
[Add any extra demo materials/links]

## Team Contributions
- [Name 1]: [Specific contributions]
- [Name 2]: [Specific contributions]
- [Name 3]: [Specific contributions]

