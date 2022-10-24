import numpy as np
import scipy.io.wavfile
import time

import tkinter as tk
from tkinter.filedialog import askopenfilename
import os

def zero_pad(x, k):
  return np.append(x, np.zeros(k))

def fft_conv(x, h):
  L, P = len(x), len(h)
  h_zp = zero_pad(h, L-1)
  x_zp = zero_pad(x, P-1)
  X = np.fft.fft(x_zp)
  start_time = time.time()
  output = np.fft.ifft(X * np.fft.fft(h_zp)).real
  output = amount_verb * output + x_zp
  end_time = time.time()
  return output, end_time - start_time


class MyFile:
  def __init__(self, name = None):
    self.name = name


root = tk.Tk()
amount_verb = .015

def open_file(file):
  file.name = askopenfilename(parent=root, title="Select a file", initialdir='.',filetypes=[("WAV file", "*.wav")])


def processData():
  global amount_verb
  amount_verb = amt.get() * 0.085 / 100 + 0.015
  print(amount_verb)
    
  print(file1.name)
  print(file2.name)
  ### All convolution Algorithmns for One Channel Real Signals
  sample_rate1, guitar = scipy.io.wavfile.read(file1.name)
  sample_rate2, reverb = scipy.io.wavfile.read(file2.name)
  reverb = (reverb.astype('float64') / np.max(reverb))[:,0] #one channel only

  signal3, timer1 = fft_conv(guitar, reverb)
  scipy.io.wavfile.write('output.wav', sample_rate1, signal3.astype('int16'))
  print('Uniform Partitioned Conv Reverb: ' + str(timer1) + ' seconds')
  os.startfile('output.wav')
  

frame1 = tk.Frame()
frame2 = tk.Frame()

text_amount = tk.Label(root, text="Intensity", font=("Comic Sans MS", 16, "bold"))
text_amount.grid(column=1, row=2)
amt = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL)
amt.grid(column=1, row=3)

text_source = tk.Label(root, text="File original", font=("Comic Sans MS", 16, "bold"))
text_source.grid(column=0, row=4)

text_filter = tk.Label(root, text="Reverb IR", font=("Comic Sans MS", 16, "bold"))
text_filter.grid(column=2, row=4)

#browse button
browse_text = tk.StringVar()
browse_text.set("Browse")

process_text = tk.StringVar()
process_text.set("Convolve")

file1 = MyFile()
browse_btn1 = tk.Button(root, textvariable=browse_text, command=lambda:open_file(file1), font=("Comic Sans MS", 16, "bold"), bg="#20bebe", fg="white", height=2, width=15)
browse_btn1.grid(column=0, row=5)

file2 = MyFile()
browse_btn2 = tk.Button(root, textvariable=browse_text, command=lambda:open_file(file2), font=("Comic Sans MS", 16, "bold"), bg="#20bebe", fg="white", height=2, width=15)
browse_btn2.grid(column=2, row=5)

process_btn = tk.Button(root, textvariable=process_text, command=lambda:processData(), font=("Comic Sans MS", 16, "bold"), bg="#20bebe", fg="white", height=2, width=15)
process_btn.grid(column=1, row=6, pady=50)

canvas = tk.Canvas(root, width=600, height=0)
canvas.grid(columnspan=3)

root.mainloop()

  
  