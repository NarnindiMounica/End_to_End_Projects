import requests
import json
import gradio

url = "http://localhost:11434/api/generate"

headers = {"Content-Type":"application/json"}

history = []
def generate_response(prompt):
    history.append(prompt)
    final_prompt = "\n".join(history)

    data = {
        "model":"monimario",
        "prompt": final_prompt,
        "stream": False
    }

    response = requests.post(url, headers=headers, data=json.dump(data))

    if response.status_code==200:
        response=response.text
        final_response=json.load(response)
        final_response=final_response['response']
        return final_response
    else:
        print(f"Error:", response.text)


app = gradio.Interface(
    fn=generate_response,
    inputs="text",
    outputs="text"
)

app.launch()