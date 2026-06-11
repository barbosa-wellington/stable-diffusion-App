
# Ensure that all libraries are installed before testing the code
# trimm, matplotlib, and numpy
import cv2
import torch
import matplotlib.pyplot as plt
import numpy as np

# reference source for deep study
# indepth vision using MiDaS
# https://www.youtube.com/watch?v=c_WbKfyt8pY


#download of MiDaS models - Image for the test
midas= torch.hub.load('isl-org/MiDaS', 'MiDaS_small')
filename = 'data/00001-1918428395.png'
fn = 'data/ocean-coast.jpg'


# modifying the model to check for avaiable GPU otherwise use cpu
device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
midas.to(device)
midas.eval()


# input transformational pipeline
transforms = torch.hub.load('isl-org/MiDaS', 'transforms')
transform = transforms.small_transform

# ploting image of depth map
def processing_image_depth(image):
    # using an image for this test
    img = cv2.imread(image)
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
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))

    axes[0].imshow(img)
    axes[0].set_title("SD image")
    axes[0].axis('off')

    im_depth = axes[1].imshow(output, cmap='magma')
    axes[1].set_title("Depth Map")
    axes[1].axis('off')

    fig.colorbar(im_depth, ax=axes[1], shrink=0.7)
    
    plt.tight_layout()
    plt.show()

# create a simple depth asset of given image
def proc_comp_img(image):
    # using an image for this test
    img = cv2.imread(image)
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

    # save_depth(output)

    plt.imshow(output, cmap='magma')
    plt.show()

def save_depth(image):
    """ This function allow the creation of a new depth image applying normalization using numpy.
        This results on a image based on the original only focus on the depth without the scale projection
        check the folder Processing for the next step.
    """

    # Applying normalization using opencv
    normalized_img = cv2.normalize(image, None, alpha=0,
                                   beta=255, norm_type=cv2.NORM_MINMAX)

    # visualizing the new matrix numpy
    # print(normalized_img)

    # convertion of float to numeric of the matrix using numpy
    int_img = normalized_img.astype(np.uint8)
    # print(int_img)

    # invert so far = dark, near
    int_img = cv2.bitwise_not(int_img)
    # plt.savefig("image", dpi=300, bbox_inches="tight")
    cv2.imwrite("data/ocean-image.png", int_img)

# Calling the fuction
# proc_comp_img(fn)

# save_depth(fn)
processing_image_depth(fn)

# processing video depth function
def processing_video_depth():

    # Hook into OpenCV
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()

        # transform import from Midas
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        imgbatch = transform(img).to(device)

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

# processing_video_depth()
