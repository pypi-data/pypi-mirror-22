json2swagger
========================================

.. image:: https://travis-ci.org/podhmo/json2swagger.svg?branch=master
    :target: https://travis-ci.org/podhmo/json2swagger



.. code-block:: bash

  $ json2swagger --help
  
  usage: json2swagger [-h] [--name NAME] [--annotations ANNOTATIONS]
                      [--show-minimap]
                      [--logging {CRITICAL,NOTSET,DEBUG,WARN,INFO,ERROR,WARNING}]
                      [--emit {schema,info}] [--dst DST]
                      src
  
  positional arguments:
    src
  
  optional arguments:
    -h, --help            show this help message and exit
    --name NAME
    --annotations ANNOTATIONS
    --show-minimap
    --logging {CRITICAL,NOTSET,DEBUG,WARN,INFO,ERROR,WARNING}
    --emit {schema,info}
    --dst DST
  

example
----------------------------------------

data.yaml

.. code-block:: yaml

  # from: https://github.com/nfarina/homebridge/blob/master/config-sample.json
  bridge:
    name: Homebridge
    username: CC:22:3D:E3:CE:30
    port: 51826
    pin: 031-45-154
  description: This is an example configuration file with one fake accessory and one
    fake platform. You can use this as a template for creating your own configuration
    file containing devices you actually own.
  accessories:
  - accessory: WeMo
    name: Coffee Maker
  platforms:
  - platform: PhilipsHue
    name: Hue


.. code-block:: bash

  $ json2swagger examples/readme/data.yaml > examples/readme/swagger.yaml
  

swagger.yaml

.. code-block:: yaml

  definitions:
    bridge:
      type: object
      properties:
        name:
          type: string
          example: Homebridge
        username:
          type: string
          example: CC:22:3D:E3:CE:30
        port:
          type: integer
          example: 51826
        pin:
          type: string
          example: 031-45-154
      required:
      - name
      - username
      - port
      - pin
    accessoriesItem:
      type: object
      properties:
        accessory:
          type: string
          example: WeMo
        name:
          type: string
          example: Coffee Maker
      required:
      - accessory
      - name
    accessories:
      type: array
      items:
        $ref: '#/definitions/accessoriesItem'
    platformsItem:
      type: object
      properties:
        platform:
          type: string
          example: PhilipsHue
        name:
          type: string
          example: Hue
      required:
      - platform
      - name
    platforms:
      type: array
      items:
        $ref: '#/definitions/platformsItem'
    top:
      type: object
      properties:
        bridge:
          $ref: '#/definitions/bridge'
        description:
          type: string
          example: This is an example configuration file with one fake accessory and
            one fake platform. You can use this as a template for creating your own
            configuration file containing devices you actually own.
        accessories:
          $ref: '#/definitions/accessories'
        platforms:
          $ref: '#/definitions/platforms'
      required:
      - bridge
      - description
      - accessories
      - platforms

