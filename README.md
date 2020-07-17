# Tarkov Weapon Accuracy Visualiser

Visualise Tarkov weapon accuracy based on in game MOA values

Made with Processing.Py

## Usage

Find the relevant build in the builds directory

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


## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Primary Todo

- Spreading circles relative to diameter rather than uniformly

- Accommodating large MOA values

## Credits

[Processing.Py 3](https://py.processing.org/)

[controlP5](http://www.sojamo.de/libraries/controlP5/)

[SW_Tower](https://www.reddit.com/user/tower299) for the template and scaling math

## License

[MIT](https://choosealicense.com/licenses/mit/)

## #Ash-12 Best Gun