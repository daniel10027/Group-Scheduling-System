# Room Assignment and Group Scheduling System - Django Project

## Project Overview

This Django project is designed to optimize the assignment of classrooms (salles) to student groups (groupes) based on available room capacities and the number of students enrolled in each program (filière). The application ensures efficient scheduling by dividing large groups into smaller ones when necessary and allocating rooms for specific time slots, ensuring no overlap between groups.

The system supports two main schedules for each room:
- **Morning Session:** 08:00 to 12:00
- **Afternoon Session:** 13:00 to 17:00

Each room can host up to two groups per day—one in the morning and one in the afternoon—maximizing room utilization across multiple campuses.

## Key Features

- **Room Capacity Management**: Assign groups to rooms based on room capacities while maintaining group sizes of at least 30 students when splitting larger groups.
- **Time Slot Scheduling**: Assign each group to a morning or afternoon time slot, ensuring no overlap within the same room.
- **Excel File Upload**: Easily upload room and filière data via Excel files, making it simple to update the system with new entries.
- **Group Generation**: Automatically generate student groups based on the number of enrollees and room capacity constraints.
- **Results Display**: View the room assignments and generated groups through a results page.
- **Reset Functionality**: Clear all current room and filière data, providing an easy way to start fresh for a new term or session.

## Project Structure

### Models

1. **Filiere**: 
   - Represents the academic program (filière), including details such as the level of study (niveau), cycle, and the number of students enrolled (nombre d'inscrits).
   - Example: *Informatique Licence 3 with 120 students*

2. **Salle**:
   - Represents the classroom or room, including its name, campus, and capacity.
   - Example: *Room 101 on Campus A with a capacity of 50 students*

3. **Group**:
   - Represents a group of students assigned to a specific room, including the room, program, group number, time slot (morning or afternoon), and the number of students in the group.

### Views

1. **Home View**:
   - Displays the list of rooms and filières.
   
2. **Upload View for Salles**:
   - Allows the user to upload room details via an Excel file.

3. **Upload View for Filieres**:
   - Allows the user to upload filière details via an Excel file.

4. **Generate Groups**:
   - Generates student groups based on the number of students and available rooms, splitting them into smaller groups if necessary.

5. **Results View**:
   - Displays the final room assignments, showing the groups that have been allocated to rooms and their respective time slots.

6. **Reset View**:
   - Deletes all room and filière data, providing a fresh start for a new scheduling process.

### URL Patterns

- `/upload_salles/`: Upload room (salle) data.
- `/upload_filieres/`: Upload filière data.
- `/results/`: View the results of room assignments.
- `/generate_groups/`: Trigger the generation of groups based on uploaded room and filière data.
- `/reset/`: Clear the database for a fresh start.
- `/`: Home page displaying all rooms and filières.

### Templates

- **index.html**: Displays the list of rooms and filières.
- **upload_salles.html**: Form to upload Excel file for room data.
- **upload_filieres.html**: Form to upload Excel file for filière data.
- **results.html**: Displays the assigned groups with room and time slot information.

## How It Works

1. **Upload Data**: First, you upload the room (salle) and filière details using Excel files. Each file should have the correct format, with column names matching the expected fields.
   
2. **Generate Groups**: Once the data is uploaded, the system processes the filière enrollment numbers and room capacities to create optimized group assignments. It automatically divides large groups when necessary and assigns them to available rooms with time slots.

3. **View Results**: After the group generation process, you can view the final room assignments on the results page, ensuring that each group is scheduled efficiently across the available rooms and time slots.

4. **Reset Data**: If you need to start over, the reset function allows you to clear all existing room and filière data and upload new datasets.

## Technology Stack

- **Django**: Backend web framework used to handle views, models, and business logic.
- **Pandas**: For processing Excel files and handling data manipulation efficiently.
- **Bootstrap**: Used for front-end styling, making the interface clean and responsive.

## How to Run the Project

1. **Clone the repository**:
   ```bash
   git clone <repository_url>
   cd <project_directory>
   ```

2. **Install dependencies**:
   Make sure you have Python installed. Then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

4. **Start the server**:
   ```bash
   python manage.py runserver
   ```

5. **Access the application**:
   Open a browser and go to `http://127.0.0.1:8000/`.

## Conclusion

This Django project provides an efficient solution for managing room assignments and group scheduling, especially useful for educational institutions with multiple campuses and large student enrollments. By leveraging the power of Django, Pandas, and Bootstrap, it offers a flexible and user-friendly system for handling complex scheduling tasks.