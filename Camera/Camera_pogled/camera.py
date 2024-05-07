
# import sys
# sys.path.append("../..")
from MovenetDepthai import MovenetDepthai, KEYPOINT_DICT
from MovenetRenderer import MovenetRenderer
import argparse

import pandas as pd
import time 
import os

# InfluxDB
from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# You can generate an API token from the "API Tokens Tab" in the UI
token = "vZQcvi2JcrPvrDBzIVoIZSbjUyF-Jt1DcgpKmozlk23MwuWiUSQbp0JSyc5xkJTKDfmTc0lor4xiQbXj8kL6LQ=="
org = "test"




parser = argparse.ArgumentParser()
parser.add_argument("-m", "--model", type=str, choices=['lightning', 'thunder'], default='thunder',
                        help="Model to use (default=%(default)s")
parser.add_argument('-i', '--input', type=str, default='rgb',
                    help="'rgb' or 'rgb_laconic' or path to video/image file to use as input (default: %(default)s)")  
parser.add_argument("-o","--output",
                    help="Path to output video file")
args = parser.parse_args()            
df = pd.DataFrame(columns=['timestamp',
    'nose','left_eye','right_eye','left_ear',
    'right_ear','left_shoulder','right_shoulder','left_elbow',
    'right_elbow','left_wrist','right_wrist',
    'left_hip','right_hip','left_knee',
    'right_knee','left_ankle','right_ankle'
])
pose = MovenetDepthai(input_src=args.input, model=args.model)
renderer = MovenetRenderer(pose, output=args.output)
print("BEFORE")
# bucket = os.environ['BUCKET']
# print("THIS IS TO CHECK IF THE VARIBLE IS INPUTTED", bucket)
data = []
# bucket = bucket[9:]

start_time = time.time()
i = 0
while True:
    # Run blazepose on next frame
    frame, body = pose.next_frame()
    if frame is None: 
        break
    timestamp = time.time()
    row = {'timestamp': timestamp, 
        'nose': body.keypoints_norm[0], 
        'left_eye': body.keypoints_norm[1], 
        'right_eye': body.keypoints_norm[2], 
        'left_ear': body.keypoints_norm[3], 
        'right_ear': body.keypoints_norm[4], 
        'left_shoulder': body.keypoints_norm[5], 
        'right_shoulder': body.keypoints_norm[6], 
        'left_elbow': body.keypoints_norm[7], 
        'right_elbow': body.keypoints_norm[8], 
        'left_wrist': body.keypoints_norm[9], 
        'right_wrist': body.keypoints_norm[10], 
        'left_hip': body.keypoints_norm[11], 
        'right_hip': body.keypoints_norm[12], 
        'left_knee': body.keypoints_norm[13], 
        'right_knee': body.keypoints_norm[14], 
        'left_ankle': body.keypoints_norm[15], 
        'right_ankle': body.keypoints_norm[16]}
    data.append(row)
    
    # Draw 2d skeleton
    frame = renderer.draw(frame, body)
    key = renderer.waitKey(delay=1)

    left_eye = data[i]['left_eye']
    right_eye = data[i]['right_eye']
    # print(left_eye[0], right_eye[0])
    # sleft_eye = left_eye[0]
    # sright_eye = right_eye[0]
    # print(sleft_eye) 
    # # Write to InfluxDB

    # # Create a Point object with a timestamp and field value
    # point = Point("camera").tag("host", "host1").field("cam_left_eye", sleft_eye)
    # point2 = Point("camera").tag("host", "host1").field("cam_right_eye", sright_eye)

   
    # with InfluxDBClient(url="http://localhost:8086", token=token, org=org) as client:
    #     write_api = client.write_api(write_options=SYNCHRONOUS)



    #     write_api.write(bucket=bucket, record=point)
    #     write_api.write(bucket=bucket, record=point2)
    #     bucket2 = '222222'
    #     write_api.write(bucket=bucket2, record=point)

    #     client.close()
    


    i += 1
    # print(df2)
    if key == 27 or key == ord('q'):
        break

# renderer.exit()
pose.exit()

# Convert data to DataFrame
df = pd.DataFrame(data)
print(df)
# Write data to Excel file
# with pd.ExcelWriter(r'C:\Users\jeans\Downloads\depthai_movenet-main (1)\depthai_movenet-main\examples\skeleton_detection\medias\testing.xlsx') as writer: 
#     df.to_excel(writer, sheet_name='df_1') 






  