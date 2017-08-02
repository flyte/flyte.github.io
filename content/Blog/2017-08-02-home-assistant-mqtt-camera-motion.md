Title: MQTT Camera Based Motion Tracking for Home Assistant
Tags: home-assistant, mqtt, motion, camera, cctv, docker, home-automation

This blog post will demonstrate the process I use to add motion tracking to any IP camera (and also perhaps directly connected ones) using the free and open source software [Motion](https://github.com/Motion-Project/motion), and publish the motion detection over the [MQTT message bus](http://mqtt.org/) for use by [Home Assistant](https://home-assistant.io/), or indeed anything else that may want to use it.

Since I run my services with [Docker](https://www.docker.com/), it utilises a [Docker Image of my creation](https://hub.docker.com/r/flyte/motion-mqtt/), but the configuration details still apply, regardless of how you run Motion.

Background
----------

I have a handful of IP cameras connected to the network in my home. They are relatively cheap, low powered, sparsely featured devices which just about handle the capture and streaming of video using Motion JPEG.

Home Assistant has no problem viewing the video feed from the devices, but in order to use the video in my automations, I needed a way of detecting motion. Thankfully, there's a great, lightweight, free and open source project called [Motion](https://github.com/Motion-Project/motion) which handles the detection of motion in video streams.

The majority of the 'smart' devices in my home communicate over the MQTT message bus. This is very convenient and integrates very well with Home Assistant. I wanted to find a way to use Motion to detect motion on my IP cameras and publish the events on an MQTT topic.

Most of the services running on my home server are within Docker containers. I wanted Motion to be no different so I [created a Docker Image for it](https://hub.docker.com/r/flyte/motion-mqtt/), specifically including an MQTT publish client.

Camera Configuration
--------------------

All of the cameras I use serve Motion JPEG streams over HTTP. This method is not limited to this configuration, and will support any camera which is supported by Motion. This includes [network cameras](https://htmlpreview.github.io/?https://github.com/Motion-Project/motion/blob/master/motion_guide.html#netcam_url) and also [directly connected ones](https://htmlpreview.github.io/?https://github.com/Motion-Project/motion/blob/master/motion_guide.html#videodevice), although you'll need to [pass the device through](https://docs.docker.com/engine/reference/commandline/run/#add-host-device-to-container-device) to the docker container.

In order to receive a Motion JPEG stream from my cameras, I use the following URL:

    http://10.0.0.10/videostream.cgi?loginuse=admin&loginpas=mypassword

You may be able to get the URL for your camera by viewing its web interface in your browser (Chrome in this case), right clicking on the video feed and choosing 'Copy image address'.

Note that in my case, simply browsing to the above URL doesn't seem to work. The same URL does work within Home Assistant and Motion, however.

Motion Configuration
--------------------

Motion requires the use of a configuration file, so in order to get this, use the following Docker command:

    :::bash
    docker run -ti --rm flyte/motion-mqtt config > motion.conf

If you're not using Docker, then you should be able to find this file in `/etc/motion` or `/usr/local/etc/motion`. It may be called `motion.conf` or `motion-dist.conf`.

### Camera Setup

To set up Motion to connect to your IP camera, edit the `motion.conf` file and perform the following actions:

- Comment out the `videodevice /dev/video0` line
- Uncomment the `netcam_url` line and set it to the URL of your video camera. For example:

```
netcam_url http://10.0.0.10/videostream.cgi?loginuse=admin&loginpas=mypassword
```

Note, for my cameras I use the `mjpeg://` 'protocol', [as described in the Motion guide](https://htmlpreview.github.io/?https://github.com/Motion-Project/motion/blob/master/motion_guide.html#netcam_url):

    netcam_url mjpeg://10.0.0.10/videostream.cgi?loginuse=admin&loginpas=mypassword

### Disable Picture and Video Capture

Since we're only using Motion to detect motion and not to record the events, change the following two config values from 'on' to 'off':

    output_pictures off
    ffmpeg_output_movies off

### Event Length

By default each event lasts for 60 seconds after the motion is no longer detected. This is too long for my liking, so adjust the amount of seconds with the `event_gap` configuration value:

    event_gap 5

MQTT Configuration
------------------

Finally, in order to actually publish the events to an MQTT topic, you must set the `on_event_start` and `on_event_end` configuration values. For example:

    on_event_start mosquitto_pub -h test.mosquitto.org -u yourusername -P yourpassword -t "cam/office/motion" -m "on"
    on_event_end mosquitto_pub -h test.mosquitto.org -u yourusername -P yourpassword -t "cam/office/motion" -m "off"

If you're not using my Docker image, then you should be able to get the `mosquitto_pub` tool from the `mosquitto-clients` package. `apt-get install mosquitto-clients` if you're using Ubuntu/Debian/Raspbian.

Have a look at `mosquitto_pub --help` for more usage information.

Run the Service
---------------

For my Docker containers, I tend to create a `docker` directory, then organise the files for each of the containers within subdirectories. For example, my three cameras are organised as such:

    motion-mqtt
    ├── office
    │   ├── config
    │   │   └── motion.conf
    │   └── run.sh
    ├── server_room
    │   ├── config
    │   │   └── motion.conf
    │   └── run.sh
    └── workshop
        ├── config
        │   └── motion.conf
        └── run.sh

Each of the `run.sh` files contains the command I use to run each container:

    :::bash
    docker run -d \
        --name motion-mqtt-office \
        -v /home/flyte/docker/motion-mqtt/office/config:/motion:ro \
        flyte/motion-mqtt

Note that the Motion configuration file is within a `config` directory which is shared within the Docker container as a volume at `/motion`. By default, the container will look for a configuration file at `/motion/motion.conf`.

Once you've created a directory structure and created a `run.sh` script, make the script runnable with `chmod +x run.sh` and then execute it with `./run.sh`. This should now have created a new Docker container. You can check the logs with `docker logs -f motion-mqtt-office`.

If everything's gone well, you should now be able to wave at the camera and receive log entries along the line of the following:

    [1:ml1] [NTC] [ALL] motion_init: Started motion-stream server on port 8081 (auth Disabled)
    [1:ml1] [NTC] [EVT] event_new_video: Source FPS 2
    [1:ml1] [NTC] [ALL] motion_detected: Motion detected - starting event 1
    [1:ml1] [NTC] [ALL] mlp_actions: End of event 1
    [1:ml1] [NTC] [EVT] event_new_video: Source FPS 2
    [1:ml1] [NTC] [ALL] motion_detected: Motion detected - starting event 2
    [1:ml1] [NTC] [ALL] mlp_actions: End of event 2
    [1:ml1] [NTC] [EVT] event_new_video: Source FPS 2
    [1:ml1] [NTC] [ALL] motion_detected: Motion detected - starting event 3
    [1:ml1] [NTC] [ALL] mlp_actions: End of event 3

Use your favourite MQTT subscription tool (MQTT Lens or mosquitto_sub in my case) to check that you're publishing events to MQTT properly.

Home Assistant Configuration
----------------------------

To add the new motion sensor to Home Assistant, create a new Binary Sensor:

    :::yaml
    binary_sensor:
      - name: Office Motion
        platform: mqtt
        state_topic: home/office/motion
        payload_on: "on"
        payload_off: "off"

You may also want to set its `device_class` as `motion` so that the UI makes more sense:

    :::yaml
    homeassistant:
      customize:
        binary_sensor.office_motion:
          device_class: motion

This should now be enough to view the motion sensor state in Home Assistant. You may now want to set up automations using the input of the motion sensor, in which case I recommend you start with [Automating Home Assistant](https://home-assistant.io/docs/automation/).
