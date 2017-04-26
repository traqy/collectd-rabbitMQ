# Usage
## Setup and deploy as collectd plugin
* Configuration /etc/collectd.d/rabbitMQ.conf

  ```
<LoadPlugin python>
        Globals true
</LoadPlugin>
<Plugin python>
        ModulePath "/usr/local/collectd/plugins/"
        Import "collectd_rabbitMQ"
        LogTraces true
        Interactive false

        <Module collectd_rabbitMQ>
                Name RMQMain
                Host 'localhost'
                Port 55672
                Username guest
                Password guest
                Vhost "/"
        </Module>  
        
        <Module collectd_rabbitMQ>
                Name rabbitMQFoo
                Host 'localhost'
                Port 55672
                Username foo_user
                Password foo_secret
                Vhost foo
        </Module>
</Plugin>
```
* Copy src/collect_rabbitMQ.py to your desired path. But in the above configuration, copy the python collectd_rabbitMQ.py to /usr/local/collectd/plugins/

  ```
  cp src/collectd_rabbitMQ.py /usr/local/collectd/plugins/
```

## Debugging
* Modify python scripts src/collectd_rabbitMQ.py and change DEBUG=False to DEBUG=True
```
DEBUG=True
```

* Testing of the python script without deploying it as collectd python plugin
```
python src/collectd_rabbitMQ.py -h
Usage:
        collectd_rabbitMQ.py
Options:
  -h, --help            show this help message and exit
  --plugin-name=PLUGIN_NAME
  -H HOST, --host=HOST  RabbitMQ hostname. Default localhost
  -P PORT, --port=PORT  RabbitMQ Admin port. Default 55672.
  --username=USERNAME   Username credential. Default guest.
  --password=PASSWORD   Password credential. Default guest.
  --vhost=VHOST         Virtual host. Default /
```

* Example command line executions

```
python src/collectd_rabbitMQ.py | python -mjson.tool
[
{
    "/-myqueue-back_q_st-avg_ack_egress_rate": 8.906804541361915,
    "/-myqueue-back_q_st-avg_ack_ingress_rate": 9.005769036265935,
    "/-myqueue-back_q_st-avg_egress_rate": 9.005769036265935,
    "/-myqueue-back_q_st-avg_ingress_rate": 9.005769036265935,
    "/-myqueue-back_q_st-len": 0,
    "/-myqueue-back_q_st-mirror_seen": 0,
    "/-myqueue-back_q_st-mirror_senders": 36,
    "/-myqueue-back_q_st-next_seq_id": 158784222,
    "/-myqueue-back_q_st-persistent_count": 12,
    "/-myqueue-back_q_st-q1": 0,
    "/-myqueue-back_q_st-q2": 0,
    "/-myqueue-back_q_st-q3": 0,
    "/-myqueue-back_q_st-q4": 0,
    "/-myqueue-back_q_st-ram_ack_count": 0,
    "/-myqueue-back_q_st-ram_msg_count": 0,
    "/-myqueue-backing_queue_status-pending_acks": 12,
    "/-myqueue-consumers": 39,
    "/-myqueue-memory": 30436064,
    "/-myqueue-message_stats-ack": 4652,
    "/-myqueue-message_stats-deliver": 4701,
    "/-myqueue-message_stats-deliver_get": 4701,
    "/-myqueue-message_stats-publish": 116,
    "/-myqueue-messages": 12,
    "/-myqueue-messages_details-interval": 5071492,
    "/-myqueue-messages_details-last_event": 1449224319537,
    "/-myqueue-messages_details-rate": 0.19718063244504772,
    "/-myqueue-messages_ready": 0,
    "/-myqueue-messages_ready_details-interval": 5071492,
    "/-myqueue-messages_ready_details-last_event": 1449224319537,
    "/-myqueue-messages_ready_details-rate": 0.0,
    "/-myqueue-messages_unacknowledged": 12,
    "/-myqueue-msgs_unack_det-interval": 5071492,
    "/-myqueue-msgs_unack_det-last_event": 1449224319537,
    "/-myqueue-msgs_unack_det-rate": 0.19718063244504772,
    "/-myqueue-msgst-ack_details-rate": 7.780895855543384,
    "/-myqueue-msgst-deliver_details-rate": 7.780895855543384,
    "/-myqueue-msgst-deliver_get_details-rate": 7.780895855543384,
    "/-myqueue-msgst-publish_details-rate": 0.21849490875529817
}
]
```
 * With parameters

  ```
python collectd_rabbitMQ.py --vhost=foo --username=foo_user --password=foo_secret | python -mjson.tool  
[
    {
        "foo-myfirstqueue-back_q_st-avg_ack_egress_rate": 2.7303689035555205,
        "foo-myfirstqueue-back_q_st-avg_ack_ingress_rate": 2.7303689035555205,
        "foo-myfirstqueue-back_q_st-avg_egress_rate": 2.7303689035555205,
        "foo-myfirstqueue-back_q_st-avg_ingress_rate": 2.7303689035555205,
        "foo-myfirstqueue-back_q_st-len": 0,
        "foo-myfirstqueue-back_q_st-mirror_seen": 0,
        "foo-myfirstqueue-back_q_st-mirror_senders": 8,
        "foo-myfirstqueue-back_q_st-next_seq_id": 49540350,
        "foo-myfirstqueue-back_q_st-persistent_count": 0,
        "foo-myfirstqueue-back_q_st-q1": 0,
        "foo-myfirstqueue-back_q_st-q2": 0,
        "foo-myfirstqueue-back_q_st-q3": 0,
        "foo-myfirstqueue-back_q_st-q4": 0,
        "foo-myfirstqueue-back_q_st-ram_ack_count": 0,
        "foo-myfirstqueue-back_q_st-ram_msg_count": 2150,
        "foo-myfirstqueue-backing_queue_status-pending_acks": 0,
        "foo-myfirstqueue-consumers": 12,
        "foo-myfirstqueue-memory": 12350344,
        "foo-myfirstqueue-message_stats-ack": 11850,
        "foo-myfirstqueue-message_stats-deliver": 15720,
        "foo-myfirstqueue-message_stats-deliver_get": 15720,
        "foo-myfirstqueue-message_stats-publish": 1168,
        "foo-myfirstqueue-messages": 0,
        "foo-myfirstqueue-messages_details-interval": 6344012,
        "foo-myfirstqueue-messages_details-last_event": 1449224614281,
        "foo-myfirstqueue-messages_details-rate": 0.0,
        "foo-myfirstqueue-messages_ready": 0,
        "foo-myfirstqueue-messages_ready_details-interval": 6344012,
        "foo-myfirstqueue-messages_ready_details-last_event": 1449224614281,
        "foo-myfirstqueue-messages_ready_details-rate": 0.0,
        "foo-myfirstqueue-messages_unacknowledged": 0,
        "foo-myfirstqueue-msgs_unack_det-interval": 6344012,
        "foo-myfirstqueue-msgs_unack_det-last_event": 1449224614281,
        "foo-myfirstqueue-msgs_unack_det-rate": 0.0,
        "foo-myfirstqueue-msgst-ack_details-rate": 1.177677878300655,
        "foo-myfirstqueue-msgst-deliver_details-rate": 1.177677878300655,
        "foo-myfirstqueue-msgst-deliver_get_details-rate": 1.177677878300655,
        "foo-myfirstqueue-msgst-publish_details-rate": 1.9902195481166027,
        "foo-mysecondqueue-back_q_st-avg_ack_egress_rate": 0.0,
        "foo-mysecondqueue-back_q_st-avg_ack_ingress_rate": 0.0,
        "foo-mysecondqueue-back_q_st-avg_egress_rate": 0.0,
        "foo-mysecondqueue-back_q_st-avg_ingress_rate": 0.0,
        "foo-mysecondqueue-back_q_st-len": 0,
        "foo-mysecondqueue-back_q_st-mirror_seen": 0,
        "foo-mysecondqueue-back_q_st-mirror_senders": 13,
        "foo-mysecondqueue-back_q_st-next_seq_id": 1905517,
        "foo-mysecondqueue-back_q_st-persistent_count": 0,
        "foo-mysecondqueue-back_q_st-q1": 0,
        "foo-mysecondqueue-back_q_st-q2": 0,
        "foo-mysecondqueue-back_q_st-q3": 0,
        "foo-mysecondqueue-back_q_st-q4": 0,
        "foo-mysecondqueue-back_q_st-ram_ack_count": 0,
        "foo-mysecondqueue-back_q_st-ram_msg_count": 1489,
        "foo-mysecondqueue-backing_queue_status-pending_acks": 0,
        "foo-mysecondqueue-consumers": 12,
        "foo-mysecondqueue-memory": 35040,
        "foo-mysecondqueue-message_stats-ack": 65,
        "foo-mysecondqueue-message_stats-deliver": 65,
        "foo-mysecondqueue-message_stats-deliver_get": 65,
        "foo-mysecondqueue-message_stats-publish": 31628,
        "foo-mysecondqueue-messages": 0,
        "foo-mysecondqueue-messages_details-interval": 5375863,
        "foo-mysecondqueue-messages_details-last_event": 1449224589106,
        "foo-mysecondqueue-messages_details-rate": 0,
        "foo-mysecondqueue-messages_ready": 0,
        "foo-mysecondqueue-messages_ready_details-interval": 5375863,
        "foo-mysecondqueue-messages_ready_details-last_event": 1449224589106,
        "foo-mysecondqueue-messages_ready_details-rate": 0,
        "foo-mysecondqueue-messages_unacknowledged": 0,
        "foo-mysecondqueue-msgs_unack_det-interval": 5375863,
        "foo-mysecondqueue-msgs_unack_det-last_event": 1449224589106,
        "foo-mysecondqueue-msgs_unack_det-rate": 0,
        "foo-mysecondqueue-msgst-ack_details-rate": 0,
        "foo-mysecondqueue-msgst-deliver_details-rate": 0,
        "foo-mysecondqueue-msgst-deliver_get_details-rate": 0,
        "foo-mysecondqueue-msgst-publish_details-rate": 0
    }
] 
```
