import tkinter as tk
import numpy as np
import tensorflow as tf
import webbrowser

# Cargar el modelo entrenado
model = tf.keras.models.load_model('modelo')

class DigitRecognizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Digit Recognizer")

        self.canvas = tk.Canvas(root, width=280, height=280, bg="white")
        self.canvas.pack()

        self.button_clear = tk.Button(root, text="Borrar", command=self.clear_canvas)
        self.button_clear.pack()

        self.button_recognize = tk.Button(root, text="Reconocer", command=self.recognize_digit)
        self.button_recognize.pack()

        self.label_result = tk.Label(root, text="")
        self.label_result.pack()

        self.link_portfolio = tk.Label(root, text="My portfolio (Web)", fg="blue", cursor="hand2")
        self.link_portfolio.pack()
        self.link_portfolio.bind("<Button-1>", self.open_portfolio)

        self.link_portfolio = tk.Label(root, text="Hire me! (Linkedin)", fg="blue", cursor="hand2")
        self.link_portfolio.pack()
        self.link_portfolio.bind("<Button-1>", self.open_linkedin)

        self.drawing = False
        self.last_x = 0
        self.last_y = 0

        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)

        self.image_data = np.zeros((28, 28), dtype=np.uint8)

    def start_drawing(self, event):
        self.drawing = True
        self.last_x = event.x
        self.last_y = event.y

    def draw(self, event):
        if self.drawing:
            x = event.x
            y = event.y
            self.canvas.create_line(self.last_x, self.last_y, x, y, fill="black", width=10, capstyle=tk.ROUND, smooth=tk.TRUE)
            self.last_x = x
            self.last_y = y
            self.update_image_data(x, y)

    def stop_drawing(self, event):
        self.drawing = False

    def update_image_data(self, x, y):
        scaled_x = int(x / 10)
        scaled_y = int(y / 10)
        self.image_data[scaled_y, scaled_x] = 255

    def clear_canvas(self):
        self.canvas.delete("all")
        self.image_data = np.zeros((28, 28), dtype=np.uint8)

    def recognize_digit(self):
        scaled_image = np.array(self.image_data, dtype=np.float32) / 255.0
        scaled_image = np.expand_dims(scaled_image, axis=0)
        prediction = model.predict(scaled_image)
        predicted_digit = np.argmax(prediction)
        print("Predicted digit:", predicted_digit)

    def open_portfolio(self, event):
        webbrowser.open("http://limlauer.github.io")
        
    def open_linkedin(self, event):
        webbrowser.open("https://www.linkedin.com/in/luis-imlauer/")

root = tk.Tk()
app = DigitRecognizerApp(root)
root.mainloop()