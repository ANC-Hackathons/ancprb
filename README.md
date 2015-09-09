# LulzBlap
Python app: [![Build Status](https://travis-ci.org/thompsnm/ancprb.svg?branch=master)](https://travis-ci.org/thompsnm/ancprb)

This project is a real-world playable arcade made using a LulzBot and controlled with a Pebble Time.

From your LulzBot 3D printer you can print a landscape and a model ship (or flying toaster) then use your Pebble Time smartwatch to navigate the ship through the terrain. More information about the genesis of this project can be found at the [hackster.io project](https://www.hackster.io/team-aboriginal-nonentity-congressmen/lulzblap).

This project is split into two components: the [Pebble app](pebble/README.md) used for navigation and a [Python app](flightpath/README.md) that runs on your desktop and listens to messages from the Pebble while controling the LulzBot 3D printer. It does not utilize a phone app to facilitate this communication. Specific information regarding installing and running each component can be found in the README's of the corresponding directories.

