import requests

def generate_bode_plot(numerator, denominator):
    url = 'http://192.168.1.4:80/generate_bode_plot'
    data = {'numerator': numerator, 'denominator': denominator}
    response = requests.post(url, json=data)
    if response.status_code == 200:
        with open('bode_plot.png', 'wb') as f:
            f.write(response.content)
        print("Bode plot image saved successfully.")
    else:
        print("Failed to generate Bode plot image.")