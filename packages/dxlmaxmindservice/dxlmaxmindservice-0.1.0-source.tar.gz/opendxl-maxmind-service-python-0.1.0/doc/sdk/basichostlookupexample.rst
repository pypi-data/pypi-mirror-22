Basic Host Lookup Example
=========================

This sample invokes and displays the results of a MaxMind "host lookup" via DXL.

For more information see:
    http://dev.maxmind.com/geoip/geoip2/geolite2/

Prerequisites
*************
* The samples configuration step has been completed (see :doc:`sampleconfig`)
* The MaxMind DXL service is running (see :doc:`running`)

Running
*******

To run this sample execute the ``sample/basic/basic_host_lookup_example.py`` script as follows:

    .. parsed-literal::

        python sample/basic/basic_host_lookup_example.py

The output should appear similar to the following:

    .. code-block:: python

        {
            "city": {
                "geoname_id": 5375480,
                "names": {
                    "de": "Mountain View",
                    "en": "Mountain View",
                    "fr": "Mountain View",
                    "ja": "\u30de\u30a6\u30f3\u30c6\u30f3\u30d3\u30e5\u30fc",
                    "ru": "\u041c\u0430\u0443\u043d\u0442\u0438\u043d-\u0412\u044c\u044e",
                    "zh-CN": "\u8292\u5ef7\u7ef4\u5c24"
                }
            },
            "continent": {
                "code": "NA",
                "geoname_id": 6255149,
                "names": {
                    "de": "Nordamerika",
                    "en": "North America",
                    "es": "Norteam\u00e9rica",
                    "fr": "Am\u00e9rique du Nord",
                    "ja": "\u5317\u30a2\u30e1\u30ea\u30ab",
                    "pt-BR": "Am\u00e9rica do Norte",
                    "ru": "\u0421\u0435\u0432\u0435\u0440\u043d\u0430\u044f \u0410\u043c\u0435\u0440\u0438\u043a\u0430",
                    "zh-CN": "\u5317\u7f8e\u6d32"
                }
            },
            "country": {
                "geoname_id": 6252001,
                "iso_code": "US",
                "names": {
                    "de": "USA",
                    "en": "United States",
                    "es": "Estados Unidos",
                    "fr": "\u00c9tats-Unis",
                    "ja": "\u30a2\u30e1\u30ea\u30ab\u5408\u8846\u56fd",
                    "pt-BR": "Estados Unidos",
                    "ru": "\u0421\u0428\u0410",
                    "zh-CN": "\u7f8e\u56fd"
                }
            },
            "location": {
                "accuracy_radius": 1000,
                "latitude": 37.386,
                "longitude": -122.0838,
                "metro_code": 807,
                "time_zone": "America/Los_Angeles"
            },
            "postal": {
                "code": "94035"
            },
            "registered_country": {
                "geoname_id": 6252001,
                "iso_code": "US",
                "names": {
                    "de": "USA",
                    "en": "United States",
                    "es": "Estados Unidos",
                    "fr": "\u00c9tats-Unis",
                    "ja": "\u30a2\u30e1\u30ea\u30ab\u5408\u8846\u56fd",
                    "pt-BR": "Estados Unidos",
                    "ru": "\u0421\u0428\u0410",
                    "zh-CN": "\u7f8e\u56fd"
                }
            },
            "subdivisions": [
                {
                    "geoname_id": 5332921,
                    "iso_code": "CA",
                    "names": {
                        "de": "Kalifornien",
                        "en": "California",
                        "es": "California",
                        "fr": "Californie",
                        "ja": "\u30ab\u30ea\u30d5\u30a9\u30eb\u30cb\u30a2\u5dde",
                        "pt-BR": "Calif\u00f3rnia",
                        "ru": "\u041a\u0430\u043b\u0438\u0444\u043e\u0440\u043d\u0438\u044f",
                        "zh-CN": "\u52a0\u5229\u798f\u5c3c\u4e9a\u5dde"
                    }
                }
            ]
        }


The geolocation information for the host with localized names is in the response.

Details
*******

The majority of the sample code is shown below:

    .. code-block:: python

        # Create the client
        with DxlClient(config) as client:

            # Connect to the fabric
            client.connect()

            logger.info("Connected to DXL fabric.")

            # Create and send request
            request_topic = "/opendxl-maxmind/service/geolocation/host_lookup"
            req = Request(request_topic)
            MessageUtils.dict_to_json_payload(req, {"ip":"8.8.8.8"})
            res = client.sync_request(req, timeout=30)

            if res.message_type != Message.MESSAGE_TYPE_ERROR:
                # Display results
                res_dict = MessageUtils.json_payload_to_dict(res)
                print MessageUtils.dict_to_json(res_dict, pretty_print=True)
            else:
                print "Error invoking service with topic '{0}': {1} ({2})".format(
                    request_topic, res.error_message, res.error_code)


After connecting to the DXL fabric, a `request message` is created with a topic that targets the "host lookup" method
of the MaxMind DXL service.

The next step is to set the `payload` of the request message. The contents of the payload include the `IP address`
to look up (in this case, 8.8.8.8, a google DNS IP).

The final step is to perform a `synchronous request` via the DXL fabric. If the `response message` is not an error
its contents are displayed.