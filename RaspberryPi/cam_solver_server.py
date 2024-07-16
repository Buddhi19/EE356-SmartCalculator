import requests
from server_address import server_address

#post image to server
def post_image(image_path):
    url = server_address+'/image'
    files = {'file': open(image_path, 'rb')}
    response = requests.post(url, files=files)

    if response.status_code == 200:
        print("Image sent successfully")
    else:
        print("Error sending image")
        print(response.text)
    return response.json().get("result")


def get_plot_image_cam(exp: str):
    url = server_address + '/plot_graph'
    data = {'expression': exp}
    response = requests.post(url, json=data)
    if response.status_code == 200:
        with open('camera/plot.png', 'wb') as f:
            f.write(response.content)
        print("Plot image saved successfully.")
        return 1
    else:
        print("Failed to generate plot image.")
        return 0