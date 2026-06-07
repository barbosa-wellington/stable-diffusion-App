
# Ensure that all libraries are installed before testing the code
# trimm, matplotlib, and numpy
import cv2
import torch
import matplotlib.pyplot as plt

# reference source for deep study
# indepth vision using MiDaS
# https://www.youtube.com/watch?v=c_WbKfyt8pY


#download of MiDaS models - Image for the test
midas= torch.hub.load('intel-isl/MiDaS', 'MiDaS_small')
filename = 'data/00001-1918428395.png'


# modifying the model to check for avaiable GPU otherwise use cpu
device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
midas.to(device)
midas.eval()


# input transformational pipeline
transforms = torch.hub.load('intel-isl/MiDaS', 'transforms')
transform = transforms.small_transform

# ploting image of depth map
def processing_image_depth(filename):
    # using an image for this test
    img = cv2.imread(filename)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    input_batch = transform(img).to(device)

    # predict and resize the original image
    with torch.no_grad():
        prediction = midas(input_batch)

        prediction = torch.nn.functional.interpolate(
            prediction.unsqueeze(1),
            size = img.shape[:2],
            mode='bicubic',
            align_corners=False,

        ).squeeze()

    # Obtaining the numpy array of the image
    output = prediction.cpu().numpy()
    # add the image to a plot and using hte cmap function to distiguish the depths
    plt.imshow(output, cmap='magma')
    plt.show()


# processing_image_depth(filename)


def processing_video_depth():

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

processing_video_depth()
