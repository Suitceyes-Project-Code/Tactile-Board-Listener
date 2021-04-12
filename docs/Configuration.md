---
layout: default
title: Configuration
nav_order: 2
---
# Configuration
The following describes the parameters that can be set in the `config.json` file located in the root directory.

| Parameter | Value | Description |
| - |-| -|
| ServerUri | Example: mqtt.ably.io / 127.0.0.1  | The hostname or IP address of the broker. |
| Port | Example: 8883 |   The network port of the server host to connect to, |
| CleanSession | `true` / `false` | A boolean that determines the client type. If `true`, the broker will remove all information about this client when it disconnects. If `false`, the client is a durable client and subscription information and queued messages will be retained when the client disconnects. |
| Username | Example: "MyUsername" | The client id string used when connecting to the broker. |
| Password | "mypassword123" | Optional password for broker authentication.|
| Topics | ["TopicA", "TopicB"] | An array of topics the client should subscribe to.|
| OverridePinLayout | `true`/ `false` | Determines whether the default vibration motor layout should be overriden. The default layout starts at pin index 0 and continues counting upwards by 1. When set to `true` a custom pin mapping can be set. See `Layout` to see how this is done. |
| Layout | Example : ```{ "0": 4, "1" : "6", "2" : "8" }``` | A list of key-value pairs where the key is the original pin index and the value is the pin it is mapped to.|