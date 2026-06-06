
# Ensure that all libraries are installed before testing the code
# trimm, matplotlib, and numpy
import cv2
import torch
import matplotlib.pyplot as plt

# reference source for deep study
# indepth vision using MiDaS
# https://www.youtube.com/watch?v=c_WbKfyt8pY


#download of MiDaS models
midas= torch.hub.load('intel-isl/MiDaS', 'MiDaS_small')
midas.to('cpu')
midas.eval()


# input transformational pipeline
transforms = torch.hub.load('intel-isl/MiDaS', 'transforms')
transform = transforms.small_transform


# Hook into OpenCV
cap = cv2.VideoCapture(0)
while cap.isOpened():
    ret, frame = cap.read()

    # transform import from Midas
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    imgbatch = transform(img).to('cpu')

    # making a prediction
    with torch.no_grad():
        prediction = midas(imgbatch)
        prediction = torch.nn.functional.interpolate(
            prediction.unsqueeze(1),
            size= img.shape[:2],
            mode='bicubic',
            align_corners=False
        ).squeeze()

        output = prediction.cpu().numpy()
        
        # print(prediction)
        # print(output)
        
    plt.imshow(output)
    cv2.imshow('CV2Frame',frame)
    plt.pause(0.00001)

    if cv2.waitKey(10) & 0xFF ==ord('q'):
        cap.release()
        cv2.destroyAllWindows()
plt.show()

