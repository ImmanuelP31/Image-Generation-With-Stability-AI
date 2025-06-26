import customtkinter as ctk
import tkinter
from PIL import Image, ImageTk
import requests
import base64
import io

api_key = "sk-0ebB5UvtovdSWhOWd8KPMmHdqTPUj4aSMyspCO2iZvp653AU"
engine_id = "stable-diffusion-v1-6"

def generate():
    user_prompt = prompt_entry.get("0.0", tkinter.END).strip()
    if not user_prompt:
        print("Prompt is empty.")
        return
    style = style_dropdown.get().strip()
    if style:
        user_prompt = f"{user_prompt}, in {style.lower()} style"

    print(f"Generating image for: {user_prompt}")
    url = f"https://api.stability.ai/v1/generation/{engine_id}/text-to-image"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "text_prompts": [{"text": user_prompt}],
        "cfg_scale": 7,
        "height": 512,
        "width": 512,
        "samples": 1,
        "steps": 30
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        image_b64 = data["artifacts"][0]["base64"]
        image_data = base64.b64decode(image_b64)
        image = Image.open(io.BytesIO(image_data)).resize((512, 512), Image.LANCZOS)
        photo_img = ImageTk.PhotoImage(image)
        canvas.delete("all")
        canvas.image = photo_img
        canvas.create_image(0, 0, anchor="nw", image=photo_img)

    except requests.exceptions.RequestException as e:
        print("HTTP error:", e)
    except Exception as e:
        print("Image processing error:", e)


root = ctk.CTk()
root.title("Image Generator")
ctk.set_appearance_mode("dark")
input_frame = ctk.CTkFrame(root)
input_frame.pack(side="left", expand=True, padx=20, pady=20)
prompt_label = ctk.CTkLabel(input_frame, text="Prompt")
prompt_label.grid(row=0, column=0, padx=10, pady=10)
prompt_entry = ctk.CTkTextbox(input_frame, height=100, width=300)
prompt_entry.grid(row=0, column=1, padx=10, pady=10)
style_label = ctk.CTkLabel(input_frame, text="Style")
style_label.grid(row=1, column=0, padx=10, pady=10)
style_dropdown = ctk.CTkComboBox(input_frame, values=["Realistic", "Cartoon", "3D Illustration", "Flat Art"])
style_dropdown.grid(row=1, column=1, padx=10, pady=10)
style_dropdown.set("Realistic")
generate_button = ctk.CTkButton(input_frame, text="Generate", command=generate)
generate_button.grid(row=2, column=0, columnspan=2, padx=10, pady=20)
canvas = tkinter.Canvas(root, width=512, height=512, bg="black")
canvas.pack(side="left", padx=10)

root.mainloop()
