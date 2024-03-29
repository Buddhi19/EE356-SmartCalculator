import torch
import numpy as np
import matplotlib.pyplot as plt
from model_load import for_test
from PIL import Image, ImageTk


def imresize(im,sz):
    pil_im = Image.fromarray(im)
    return np.array(pil_im.resize(sz))

def resize( w_box, h_box, pil_image): 
	w, h = pil_image.size 
	f1 = 1.0*w_box/w 
	f2 = 1.0*h_box/h    
	factor = min([f1, f2])   
	width = int(w*factor)    
	height = int(h*factor)    
	return pil_image.resize((width, height), Image.ANTIALIAS)  

img_test = Image.open("./test_images/test2.png").convert("L")

img_test = np.invert(img_test)

plt.imshow(img_test, cmap="gray")
plt.show()

img_proceed = torch.from_numpy(np.array(img_test)).type(torch.FloatTensor)
img_proceed = img_proceed/255.0
img_proceed = img_proceed.unsqueeze(0)
img_proceed = img_proceed.unsqueeze(0)

#display img_proceed
plt.imshow(img_proceed[0][0], cmap="gray")
plt.show()


attention, prediction = for_test(img_proceed)

prediction_text = ""

for i in range(attention.shape[0]):
	if prediction[i] == "<eol>":
		continue
	else:
		prediction_text += prediction[i]

print(prediction_text)