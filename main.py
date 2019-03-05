
from picamera import PiCamera
from time import sleep
import requests
import json
import os
from PIL import Image

import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
camera = PiCamera()
while True:
  if GPIO.input(10) == GPIO.HIGH:
    start = "Welcome"
    os.system('espeak -s120 -g2 -ven+m7  \"'+ start + '\" 2>/dev/null')
    
    camera.start_preview()
    sleep(3)
    camera.capture('image.jpg')
    camera.stop_preview()
    picture =  Image.open('image.jpg')
    picture.rotate(270).save('image.jpg')
    
    image_value = "Image Captured"
    os.system('espeak -s120 -g2 -ven+m7  \"'+ image_value + '\" 2>/dev/null')
    


    def open_image(path):
      newImage = Image.open(path)
      return newImage

    # Save Image
    def save_image(image, path):
      image.save(path, 'png')


    # Create a new image with the given size
    def create_image(i, j):
      image = Image.new("RGB", (i, j), "white")
      return image


    # Get the pixel from the given image
    def get_pixel(image, i, j):
      # Inside image bounds?
      width, height = image.size
      if i > width or j > height:
        return None

      # Get Pixel
      pixel = image.getpixel((i, j))
      return pixel

    # Create a Grayscale version of the image
    def convert_grayscale(image):
      # Get size
      width, height = image.size

      # Create new Image and a Pixel Map
      new = create_image(width, height)
      pixels = new.load()

      # Transform to grayscale
      for i in range(width):
        for j in range(height):
          # Get Pixel
          pixel = get_pixel(image, i, j)

          # Get R, G, B values (This are int from 0 to 255)
          red =   pixel[0]
          green = pixel[1]
          blue =  pixel[2]

          # Transform to grayscale
          gray = (red * 0.30) + (green * 0.59) + (blue * 0.11)

          # Set Pixel in new image
          pixels[i, j] = (int(gray), int(gray), int(gray))

      # Return new image
      return new

    value = "Gray scale conversion is under Proccess for Better output. It might take 5 to 10 seconds"
    os.system('espeak -s120 -g2 -ven+m7  \"'+ value + '\" 2>/dev/null')
    
    if __name__ == "__main__":
      # Load Image (JPEG/JPG needs libjpeg to load)
      original = open_image('image.jpg')
      

      # Convert to Grayscale and save
      new = convert_grayscale(original)
      save_image(new, 'image.jpg')

    def ocr_space_file(filename, overlay=False, api_key='01d51b30af88957', language='eng'):
        

        payload = {'isOverlayRequired': overlay,
                   'apikey': api_key,
                   'language': language,
                   }
        with open(filename, 'rb') as f:
            r = requests.post('https://api.ocr.space/parse/image',
                              files={filename: f},
                              data=payload,
                              )
        return r.content.decode()

    print()
    # Use examples:
    
    test_file = ocr_space_file(filename='image.jpg', language='eng')
    #print(test_file)
    
    j= json.loads(test_file)
    print(j["ParsedResults"][0]["ParsedText"])

    print(j)
    ans =  j["ParsedResults"][0]["ParsedText"]
    print(ans)
    ans1 = ans.replace('\r\n' , "")
    print(ans1)
    #tts = gTTS(text = ans, lang='en')
    #tts.save("good1.mp3")
    os.system('espeak -s120 -g2 -ven+m7  \"'+ ans1 + '\" 2>/dev/null')

    #print image_to_string(Image.open('/home/pi/Desktop/image2.jpg'))
    #print image_to_string(Image.open('image2-english.jpg'),lang='eng')
    
