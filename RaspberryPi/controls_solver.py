import requests
from server_address import server_address

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