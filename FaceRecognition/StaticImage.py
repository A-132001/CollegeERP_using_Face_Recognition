import cv2
import face_recognition
import numpy as np
import psycopg2
# Connect to the database
conn = psycopg2.connect(
    host="localhost",
    database="CollegeManagementSystem",
    user="postgres",
    password="123456",
)
# get date & and course Id
date = '2023-04-01'
course_id = "CS425"
# Create a cursor object
cur = conn.cursor()

# load test image
image = cv2.imread("images/test/test3.jpeg")

# detect faces 
face_locations = face_recognition.face_locations(image)

known_faces = []
known_names = ["CSA01", "CSA02", "CSA03","CSA04","CSA05"]

for name in known_names:
    filename = f"images/MyData/{name.lower().replace(' ', '_')}.jpeg"
    face_image = face_recognition.load_image_file(filename)
    face_encoding = face_recognition.face_encodings(face_image)[0]
    known_faces.append(face_encoding)

#create list to store names in photo
people_name = []

#start compare
for face_location in face_locations:
    face_encoding = face_recognition.face_encodings(image, [face_location])[0]
    matches = face_recognition.compare_faces(known_faces, face_encoding)
    name = "Unknown"
    
    if True in matches:
        match_index = matches.index(True)
        name = known_names[match_index]
        if name in known_names:
            # Update the 'ceil' column in the 'your_table' table
            cur.execute("UPDATE public.info_attendance SET status = true WHERE date = %s AND student_id = %s AND course_id = %s ;",(date,name,course_id,))
            # Commit the changes
            conn.commit()
            
        people_name.append(name)
        

    # Draw a box around the face and label it with the name
    top, right, bottom, left = face_location
    cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 2)
    cv2.putText(image, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (127,255,0), 2)

# For absent students 
for name in known_names:
    if name not in people_name:
         # Update the 'ceil' column in the 'your_table' table
        cur.execute("UPDATE public.info_attendance SET status = false WHERE date = %s AND student_id = %s AND course_id = %s ;",(date,name,course_id,))
        # Commit the changes
        conn.commit()

# Close the cursor and connection
cur.close()
conn.close()

print(people_name)
cv2.imshow("Image", image)
cv2.waitKey(0)