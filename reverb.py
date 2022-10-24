import numpy as np
import scipy.io.wavfile
import time

import tkinter as tk
from tkinter.filedialog import askopenfilename
import os

def zero_pad(x, k):
  return np.append(x, np.zeros(k))

# partition impulse response and precompute frequency response for each block
def precompute_frequency_responses(h, L, k, num_blocks):
  H = np.zeros((num_blocks, L+k)).astype('complex128')
  for j in range(num_blocks):
    H[j] += np.fft.fft(zero_pad(h[j*k: (j+1)*k], L))
  return H

# break sig into chunks (size L)
# break ir into chunks (size k)
# use overlap add fft based conv to convolve
def uniform_partitioned_conv(sound_src, source_kernel):
  source_kernel_len = len(source_kernel)
  signal_block_size = 2**8 #signal block size
  ir_block_size = signal_block_size #ir block size

  sound_src = sound_src[0: -1 * (sound_src.shape[0] % signal_block_size)]
  N = sound_src.shape[0]
  num_ir_blocks = int(source_kernel_len/ir_block_size)
  num_sig_blocks = int(sound_src.shape[0] / signal_block_size)
  H = precompute_frequency_responses(source_kernel, signal_block_size, ir_block_size, num_ir_blocks)
  output = np.zeros(source_kernel_len-1 + num_sig_blocks*signal_block_size)
  start_time = time.time()
  for i in range(num_sig_blocks):
    input_buffer = zero_pad(sound_src[i*signal_block_size: (i+1)*signal_block_size], ir_block_size)
    spectrum = np.fft.fft(input_buffer)
    for j in range(num_ir_blocks):
      output[i*signal_block_size+j*ir_block_size: (i+1)*signal_block_size+(j+1)*ir_block_size-1] += np.fft.ifft(spectrum * H[j]).real[:2*ir_block_size-1]
  x_zp = zero_pad(sound_src, source_kernel_len-1)
  output = amount_verb * output + x_zp
  return output, time.time() - start_time


class MyFile:
  def __init__(self, name = None):
    self.name = name


root = tk.Tk()
amount_verb = .015

def open_file(file):
  file.name = askopenfilename(parent=root, title="Select a file", initialdir='.',filetypes=[("WAV file", "*.wav")])


def processData():
  print(file1.name)
  print(file2.name)
  ### All convolution Algorithmns for One Channel Real Signals
  sample_rate1, guitar = scipy.io.wavfile.read(file1.name)
  sample_rate2, reverb = scipy.io.wavfile.read(file2.name)
  reverb = (reverb.astype('float64') / np.max(reverb))[:,0] #one channel only

  signal3, timer1 = uniform_partitioned_conv(guitar, reverb)
  scipy.io.wavfile.write('output.wav', sample_rate1, signal3.astype('int16'))
  print('Uniform Partitioned Conv Reverb: ' + str(timer1) + ' seconds')
  os.startfile('output.wav')
  

frame1 = tk.Frame()
frame2 = tk.Frame()

text_source = tk.Label(root, text="File original", font="Raleway")
text_source.grid(column=0, row=1)

text_filter = tk.Label(root, text="Reverb IR", font="Raleway")
text_filter.grid(column=2, row=1)

#browse button
browse_text = tk.StringVar()
browse_text.set("Browse")

process_text = tk.StringVar()
process_text.set("Convolve")

file1 = MyFile()
browse_btn1 = tk.Button(root, textvariable=browse_text, command=lambda:open_file(file1), font="Raleway", bg="#20bebe", fg="white", height=2, width=15)
browse_btn1.grid(column=0, row=2)

file2 = MyFile()
browse_btn2 = tk.Button(root, textvariable=browse_text, command=lambda:open_file(file2), font="Raleway", bg="#20bebe", fg="white", height=2, width=15)
browse_btn2.grid(column=2, row=2)

process_btn = tk.Button(root, textvariable=process_text, command=lambda:processData(), font="Raleway", bg="#20bebe", fg="white", height=2, width=15)
process_btn.grid(column=1, row=3, pady=50)

canvas = tk.Canvas(root, width=600, height=100)
canvas.grid(columnspan=3)

root.mainloop()

  
  