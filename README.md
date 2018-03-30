# LulzBlap
This project is a real-world playable arcade made using a LulzBot and controlled with a Pebble Time. It was awarded Best Integration With a 3rd Party API in the [Pebble Rocks Boulder](https://www.hackster.io/hackathons/pebble-rocks-boulder/a-pebble-hackathon/projects) hackathon.

From your LulzBot 3D printer you can print a landscape and a model ship (or flying toaster) then use your Pebble Time smartwatch to navigate the ship through the terrain. More information about the genesis of this project can be found at the [hackster.io project](https://www.hackster.io/team-aboriginal-nonentity-congressmen/lulzblap). A demonstration of this project can be seen on YouTube:

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/iOtIGAwGAAE/0.jpg)](https://www.youtube.com/embed/iOtIGAwGAAE?rel=0)

This project is split into two components: the [Pebble app](pebble/README.md) used for navigation and a [Python app](flightpath/README.md) that runs on your desktop and listens to messages from the Pebble while controling the LulzBot 3D printer. It does not utilize a phone app to facilitate this communication. Specific information regarding installing and running each component can be found in the README's of the corresponding directories.

