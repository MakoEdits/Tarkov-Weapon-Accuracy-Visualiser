# Tarkov Weapon Accuracy Visualiser

Visualise Tarkov weapon accuracy based on in game MOA values

Made with Processing.Py

## Information

Tarkov MOA is represented as radius rather than the traditional diamater format

This means that the formula is: ```Tarkov MOA x 2``` for inches, then multiplied by 2.54 for centimeters

## Usage

**Enter** an MOA value based off of weapons in game. Add subsequent distance values, separated by a comma


![ASh-12 Example](/examples/ASh-12Example.png)


**Save** renders by selecting the output destination


![Save Example](/examples/SaveExample.png)


**Import** datasets using a simple json format which will render automatically


```python
[
	1, # MOA value, default distances
	[1, 200] # MOA value, single distance
	[1, 200, 300, 400] # MOA value, multiple distances
]
```


![Import Example](/examples/ImportExample.png)


**Zoom** in and out. Zoom will be retained when saving image, including imports


![Zoom Example](/examples/ZoomExample.png)


## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Primary TODOS

**Major:**

- Allow zoom level to be specified in import

- Spreading circles relative to diameter rather than uniformly

- Moving circle group/moving frame

**Minor:**

- Toggle various text areas

- Accommodating large MOA values

- Displaying text if circle draws larger than frame

## Credits

[Processing.Py 3](https://py.processing.org/)

[controlP5](http://www.sojamo.de/libraries/controlP5/)

[SW Tower](https://www.youtube.com/channel/UCwYEdvfGj9kesA2kiIefNJg) for the idea, template and hard math

## License

[MIT](https://choosealicense.com/licenses/mit/)

## #Ash-12 Best Gun