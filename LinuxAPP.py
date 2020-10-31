#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk
import os
import threading 
import subprocess
def aboutme():
	winx = tk.Toplevel()
	winx.geometry("300x150")
	winx.title("About the developer")
	t=tk.Text(winx)
	t.pack()
	t.configure(state='normal')
	t.insert("1.0","Developed by Suhaib Bin Younis\nFollow @suhaibbinyounis\ntiny.cc/sby")
	t.configure(state='disabled')
	winx.mainloop()
def sensors():
	global sensorText
	sensorText.configure(state='normal')
	sensorText.delete("1.0","end")
	test = subprocess.Popen(["sensors"], stdout=subprocess.PIPE)
	x = test.communicate()[0]
	sensorText.insert('1.0',x)
	sensorText.configure(state='disabled')
def freeMemory():
	global freeMemText
	freeMemText.configure(state='normal')
	freeMemText.delete("1.0","end")
	test = subprocess.Popen(["free","-m"], stdout=subprocess.PIPE)
	x = test.communicate()[0]
	freeMemText.insert('1.0',x)
	freeMemText.configure(state='disabled')
def hddtemp():
	global hddtempText
	hddtempText.configure(state='normal')
	hddtempText.delete("1.0","end")
	test = subprocess.Popen(["sudo","hddtemp","/dev/sda1"], stdout=subprocess.PIPE)
	x = test.communicate()[0]
	hddtempText.insert('1.0',x)
	hddtempText.configure(state='disabled')
def ping():
	global pingText
	test = subprocess.Popen(["ping","8.8.8.8"], stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	while True:
		stdout = []
		line = test.stdout.readline()
		stdout.append(line)
		if(len(line) > 0 ):
			pingText.insert("1.0", line)
			pingText.update_idletasks()    
		if line == '' and test.poll() != None:
			break
def runCommand():
	global outputText
	global commandEntry
	outputText.configure(state='normal')
	outputText.delete("1.0","end")
	cmdstr = commandEntry.get('1.0',"end-1c")
	inp = list(cmdstr.split(' '))
	test = subprocess.Popen(inp, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	while True:
		stdout = []
		line = test.stdout.readline()
		stdout.append(line)
		if(len(line) > 0 ):
			outputText.configure(state='normal')
			outputText.insert(tk.END, line)
			outputText.configure(state='disabled')
			outputText.update_idletasks()    
		if line == '' and test.poll() != None:
			break
	outputText.configure(state='disabled')
try:
	win = tk.Tk()
	win.title("Linux Utility Tools")
	win.geometry("900x900")

	main_frame = tk.Frame(win)
	main_frame.pack(fill=tk.BOTH,expand=1)

	my_canvas = tk.Canvas(main_frame)
	my_canvas.pack(side=tk.LEFT,fill=tk.BOTH,expand=1)

	my_scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL,command=my_canvas.yview)
	my_scrollbar.pack(side=tk.RIGHT,fill=tk.Y)

	my_canvas.configure(yscrollcommand=my_scrollbar.set)
	my_canvas.bind('<Configure>',lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

	second_frame = tk.Frame(my_canvas)
	my_canvas.create_window((0,0),window=second_frame)

	scrollbar = tk.Scrollbar(win)
	scrollbar.pack( side = tk.RIGHT, fill=tk.Y )

	#about
	aboutBtn = tk.Button(second_frame,text="About",command=aboutme)
	aboutBtn.pack()
	#Ping 8.8.8.8
	pingFrame = tk.Frame(second_frame)
	pingFrame.pack()
	pingLabel = tk.Label(pingFrame,text="\nPinging \n8.8.8.8")
	pingLabel.pack(side=tk.LEFT)
	pingText = tk.Text(pingFrame,height=16,width=65)
	pingText.pack(side=tk.LEFT)
	threading.Thread(target=ping).start()
	
	#Sensors
	sensorFrame = tk.Frame(second_frame)
	sensorFrame.pack()
	sensorLabel = tk.Label(sensorFrame,text="\nSensors")
	sensorLabel.pack(side=tk.LEFT)
	sensorText = tk.Text(sensorFrame,height=16,width=65)
	sensorText.pack(side=tk.LEFT)
	threading.Thread(target=sensors).start()

	#HDDTemp
	hddtempFrame = tk.Frame(second_frame)
	hddtempFrame.pack()
	hddtempLabel = tk.Label(hddtempFrame,text="\nHardDisk\nTemperatue")
	hddtempLabel.pack(side=tk.LEFT)
	hddtempText = tk.Text(hddtempFrame,height=2,width=65)
	hddtempText.pack(side=tk.LEFT)
	threading.Thread(target=hddtemp).start()

	#freeMemory
	freeMemoryFrame = tk.Frame(second_frame)
	freeMemoryFrame.pack()
	freeMemLabel = tk.Label(freeMemoryFrame,text="\nFree Memory(m)")
	freeMemLabel.pack(side=tk.LEFT)
	freeMemText = tk.Text(freeMemoryFrame,height=5,width=80)
	freeMemText.pack(side=tk.LEFT)
	threading.Thread(target=freeMemory).start()


	win.mainloop()
except:
	exit(1)
