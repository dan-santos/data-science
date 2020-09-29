import face_recognition
import cv2
import numpy as np

# python libraries
import os
import glob

faces_encodings = list()
faces_names = list()

# pics of faces
path = 'faces/'

# tacking all jpeg files in folder
list_of_files = [f for f in glob.glob(path + '*.jpeg')]

number_files = len(list_of_files)

# file names
names = list_of_files.copy()


def get_person_name(file_name):
    # removing the file path
    file_name = file_name.replace(path, '')

    # removing the file extension
    file_name = file_name.split('.')[0]

    # if file name contains '-', replace it to a blank space
    if '-' in file_name:
        file_name = file_name.replace('-', ' ')
    return file_name


for i in range(number_files):
    globals()['image_{}'.format(i)] = face_recognition.load_image_file(list_of_files[i])
    globals()['image_encoding_{}'.format(i)] = face_recognition.face_encodings(globals()['image_{}'.format(i)])[0]

    # creating array of know names
    faces_encodings.append(globals()['image_encoding_{}'.format(i)])
    faces_names.append(get_person_name(names[i]))

face_locations = list()
face_encodings = list()
face_names = list()

# auxiliar variable
process_this_frame = True

video_capture = cv2.VideoCapture(0)

while True:
    ret, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]

    if process_this_frame:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        face_names = list()

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(faces_encodings, face_encoding)
            name = 'Unknown'
            face_distances = face_recognition.face_distance(faces_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                name = faces_names[best_match_index]
                face_names.append(name)
                process_this_frame = not process_this_frame  # display the results

    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # draw a rectangle around the face
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Input text label with a name below the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX

        # Display the resulting image
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
