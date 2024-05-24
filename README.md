# VentureM starts his work on this TFT
# Thats an excellent start point for me !! - My rant starts

So I have had this machine for about 6 months, am one of the early adopters. However I was stuck with the same issue, the TFT can only be used in Windows and with the warnings I was  getting in Windows, I was not planning to keep running windows.
The original purpose of this machine was to work as a home server so that I could run my LLM experiments on this, while utilising cloud instances and other powerfull local machines for actual computing needs.
Once I installed Bodhilinux, I found myself stuck with clock display and nothing else. Probing the USB devices led to below :

![image](https://github.com/venturem/AceMagic-S1-LED-TFT-Linux/assets/13586393/4e2fd070-137e-4bf1-9127-10ffdefecc10)

Now the challenge was to understand what was going on here - but due to work commitments I could not spend too much time on this.
As a result even today (31 March 2024), the TFT still shows time only :)

## And we have the next issue.
It seems that the default firmware is coded to show time, but the developer did not bother with intricacies like Daylight Time Savings - so today when UK rolls back time, the clock is one hour behind with no other option but to work on this issue.
Many thanks to the OP for starting this thread; and time and effort spent in capturing the data packets.


## 07-04-2024 LED control is implemented !!! 

The LED control has been implemented in python using PySerial - did need a few reboots into Windoz to get the CRC right, but I belive it is now fixed and working as expected.
Please raise an issue if you find a bug, I'll endeavour to replicate and fix the issue.

## XX-05-2024 Next is to implement the TFT screen handler 

I have been able to implement a Screen handler with some effort. As said by @tjaworski, the framebuffer of LCD is extremely slow. Slow to the extent that it takes 2.8 to 3.3 seconds if you try to update the whole screen.
So naturally, we have to create and maintain a offline buffer and update LCD framebuffer only if and when required. This introduces some hassle and complexity.
Also in my case (as maybe with many other folks), the minipc is in vertical orientation, while the framebuffer is in horizontal orientation, this needs x,y axis translation and rotation, plus bounding on the axes to get correct result.

Screenshots of what has been acheived. I'll be updating the code once I have better handling for both; vertical and horizontal orientations.

![IMG_20240427_191132](https://github.com/venturem/AceMagic-S1-LED-TFT-Linux/assets/13586393/b1606762-64ce-4f34-b956-586746d8afb8)


![IMG_20240505_110547](https://github.com/venturem/AceMagic-S1-LED-TFT-Linux/assets/13586393/c2efc188-270a-4d11-9ee0-94f9cee338e0)

![wallpaper](https://github.com/venturem/AceMagic-S1-LED-TFT-Linux/assets/13586393/6562b003-3fce-44db-81bd-5ea2b0f8ea04)



## XX-XX-2024 Create a FAST API to control this from endpoint

## XX-XX-2024 Later to dockerise the whole thing



# Original Text from [[https://github.com/tjaworski](https://github.com/tjaworski/AceMagic-S1-LED-TFT-Linux)](https://github.com/tjaworski/AceMagic-S1-LED-TFT-Linux)



# AceMagic-S1-LED-TFT-Linux
ACEMAGIC S1 Mini TFT/LCD Control for Linux


