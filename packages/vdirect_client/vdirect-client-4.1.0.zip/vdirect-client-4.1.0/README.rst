.. image:: http://www.radappliances.com/images/Software/vDirect/vdirect.jpg

============================================================
A REST-based client for vDirect
============================================================
An auto-generated, unofficial (but seems to work..) REST-based client for `Radware vDirect <https://www.radware.com/products/vdirect/>`_


*******************
Client features:
*******************
- Support Async operation. The default behaviour of the client is to wait until async operation is complete. This behaviour can be overidden.
- Support vDirect HA. If the client is configured with a secondary vDirect address it will try to switch to the secondary vDirect if the primary vDirect fails.
- API call result is a tuple with four entries:
    1. HTTP response code. Example: 404. (int)
    2. HTTP response reason. Example: Not found. (string)
    3. The response as a string.
    4. The response as a dict (most of the time).

To understand which payloads to send and their expected response, developers should consult the vDirect REST API docs (https://<vdirect_ip>:2189/docs/api-docs/).


*******************
Basic client usage:
*******************
.. code-block:: python

    import vdirect_client
    from vdirect_client import RestClient as Client

    def show(result):
        print result[vdirect_client.RESP_STATUS]
        print result[vdirect_client.RESP_REASON]
        print result[vdirect_client.RESP_STR]
        print result[vdirect_client.RESP_DATA]

    ip = <vdirect_ip>
    user = <vdirect_user>
    password = <vdirect_password>
    client = Client(ip, user, password)
    data = {"tenants":[],"parameters":{"vipAddress":"1.1.1.1","ServerIps":["1.2.3.4","1.2.3.5"]},
                                        "devices":{"adc":{"deviceId":{"name":"Site1.vx2"}}}}
    show(client.workflowTemplate.create_workflow(data,'caching_enh','inst1'))
    show(client.ha.get_ha_config())
    show(client.ha.get_ha_status())
    show(client.template.list())
    show(client.template.run_template({},"A"))
    show(client.defensePro.list())

