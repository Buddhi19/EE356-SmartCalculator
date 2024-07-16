import requests
import os
from server_address import server_address

parent_dir = os.path.dirname(os.path.abspath(__file__))

## not used
def generate_bode_plot(numerator, denominator):
    url = server_address+'/generate_bode_plot'
    data = {'numerator': numerator, 'denominator': denominator}
    response = requests.post(url, json=data)
    if response.status_code == 200:
        with open('bode_plot.png', 'wb') as f:
            f.write(response.content)
        print("Bode plot image saved successfully.")
    else:
        print("Failed to generate Bode plot image.")