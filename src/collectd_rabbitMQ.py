#!/usr/bin/env python

try:
    import collectd
except:
    pass
import urllib2
import simplejson as json
import traceback
import base64
import re
import optparse

DEBUG=True

LIVE=True
PLUGIN_NAME='RMQ'
CONFIGS = []
METRICS_RESULTS = []

METRIC={
    'backing_queue_status' : True,
    'consumers' : True,
    'memory' : True,
    'messages' : True,
    'messages_details' : True,
    'messages_ready' : True,
    'messages_ready_details' : True,
    'messages_unacknowledged' : True,
    'messages_unacknowledged_details' : True,
    'deliver_details' : True,
    'message_stats' : True,
    }
SUB_METRIC={
    'backing_queue_status' : True,
    'messages_details' : True,
    'messages_ready_details' : True,
    'messages_unacknowledged_details' : True
}
"""Sample json ouput from RESTFul API http://localhost:55672/api/queues/vhost/"""

MESSAGES_STATS = {
    'ack' : True,
    'ack_details' : True,
    'deliver' : True,
    'deliver_details' : True,
    'deliver_get' : True,
    'deliver_get_details' : True,
    'publish' : True,
    'publish_details' : True
}

METRIC_KEY_TRUNCATE={
    'message_stats-ack_details-rate'                : 'msgst-ack_details-rate',
    'message_stats-ack_details-interval'            : 'msgst-ack_details-interval',
    'message_stats-ack_details-last_event'          : 'msgst-ack_details-last_event',
    'message_stats-deliver_details-rate'            : 'msgst-deliver_details-rate',
    'message_stats-deliver_details-interval'        : 'msgst-deliver_details-interval',
    'message_stats-deliver_details-last_event'      : 'msgst-deliver_details-last_event',
    'message_stats-deliver_get_details-rate'        : 'msgst-deliver_get_details-rate',
    'message_stats-deliver_get_details-interval'    : 'msgst-deliver_get_details-interval',
    'message_stats-deliver_get_details-last_event'  : 'msgst-deliver_get_details-last_event',
    'message_stats-publish_details-rate'            : 'msgst-publish_details-rate',
    'message_stats-publish_details-interval'        : 'msgst-publish_details-interval',
    'message_stats-publish_details-last_event'      : 'msgst-publish_details-last_event',
    'message_stats-redeliver_details-rate'          : 'msgst-redeliver_details-rate',
    'message_stats-redeliver_details-interval'      : 'msgst-redeliver_details-interval',
    'message_stats-redeliver_details-last_event'    : 'msgst-redeliver_details-last_event',
    'messages_unacknowledged_details-interval'      : 'msgs_unack_det-interval',
    'messages_unacknowledged_details-last_event'    : 'msgs_unack_det-last_event',
    'messages_unacknowledged_details-rate'          : 'msgs_unack_det-rate',
    'backing_queue_status-avg_ack_egress_rate'      : 'back_q_st-avg_ack_egress_rate',
    'backing_queue_status-avg_ack_ingress_rate'     : 'back_q_st-avg_ack_ingress_rate',
    'backing_queue_status-avg_egress_rate'          : 'back_q_st-avg_egress_rate',
    'backing_queue_status-avg_ingress_rate'         : 'back_q_st-avg_ingress_rate',
    'backing_queue_status-len'                      : 'back_q_st-len',
    'backing_queue_status-mirror_seen'              : 'back_q_st-mirror_seen',
    'backing_queue_status-mirror_senders'           : 'back_q_st-mirror_senders',
    'backing_queue_status-next_seq_id'              : 'back_q_st-next_seq_id',
    'backing_queue_status-persistent_count'         : 'back_q_st-persistent_count',
    'backing_queue_status-q1'                       : 'back_q_st-q1',
    'backing_queue_status-q2'                       : 'back_q_st-q2',
    'backing_queue_status-q3'                       : 'back_q_st-q3',
    'backing_queue_status-q4'                       : 'back_q_st-q4',
    'backing_queue_status-ram_ack_count'            : 'back_q_st-ram_ack_count',
    'backing_queue_status-ram_msg_count'            : 'back_q_st-ram_msg_count'
}
sample_result = """
[
    {
        "arguments": {
            "x-dead-letter-exchange": "",
            "x-dead-letter-routing-key": "dlq_ruleevent_p6",
            "x-ha-policy": "all"
        },
        "auto_delete": false,
        "backing_queue_status": {
            "avg_ack_egress_rate": 9.490264211890793,
            "avg_ack_ingress_rate": 9.490264211890793,
            "avg_egress_rate": 9.490264211890793,
            "avg_ingress_rate": 9.490264211890793,
            "delta": [
                "delta",
                "undefined",
                0,
                "undefined"
            ],
            "len": 0,
            "mirror_seen": 0,
            "mirror_senders": 55,
            "next_seq_id": 101415599,
            "pending_acks": 0,
            "persistent_count": 0,
            "q1": 0,
            "q2": 0,
            "q3": 0,
            "q4": 0,
            "ram_ack_count": 0,
            "ram_msg_count": 625082,
            "target_ram_count": "infinity"
        },
        "consumers": 8,
        "durable": true,
        "exclusive_consumer_tag": "",
        "memory": 16024016,
        "message_stats": {
            "ack": 193335,
            "ack_details": {
                "interval": 6865961,
                "last_event": 1448898526514,
                "rate": 8.234598202652839
            },
            "deliver": 193335,
            "deliver_details": {
                "interval": 6865961,
                "last_event": 1448898526514,
                "rate": 8.234598202652839
            },
            "deliver_get": 193335,
            "deliver_get_details": {
                "interval": 6865961,
                "last_event": 1448898526514,
                "rate": 8.234598202652839
            },
            "publish": 955,
            "publish_details": {
                "interval": 225472995,
                "last_event": 1448898529620,
                "rate": 8.974702667095691
            }
        },
        "messages": 0,
        "messages_details": {
            "interval": 5099992,
            "last_event": 1448898528828,
            "rate": 0.0
        },
        "messages_ready": 0,
        "messages_ready_details": {
            "interval": 5099992,
            "last_event": 1448898528828,
            "rate": 0.0
        },
        "messages_unacknowledged": 0,
        "messages_unacknowledged_details": {
            "interval": 5099992,
            "last_event": 1448898528828,
            "rate": 0.0
        },
        "name": "ruleevent_p6",
        "node": "rabbit@lyra-rabbitmq3",
        "slave_nodes": [
            "rabbit@lyra-rabbitmq1",
            "rabbit@lyra-rabbitmq2"
        ],
        "synchronised_slave_nodes": [
            "rabbit@lyra-rabbitmq2",
            "rabbit@lyra-rabbitmq1"
        ],
        "vhost": "leto"
    }
]  
"""

class RabbitMQ(object):

    def __init__(self):

        self.admin_port = None
        self.host = None
        self.plugin_name = None
        self.vhost = None
        self.username = None
        self.password = None

        #self.plugin_name = PLUGIN_NAME
        #self.host = "localhost"
        #self.admin_port = 55672
        #self.vhost = "leto"
        #self.username = 'leto'
        #self.password = 'ten20304051'

        self.debug_info = DEBUG
        self.live = LIVE
        self.metric_table = []

    def collectd_info(self, msg):
        if self.debug_info:
            print(msg)
        else:
            collectd.info(msg)
    def collectd_warning(self, msg):
        if self.debug_info:
            print(msg)
        else:
            collectd.warning(msg)

    def config(self, obj):
        for node in obj.children:
            if node.key == 'Port':
                self.admin_port = int(node.values[0])
            elif node.key == 'Host':
                self.host = node.values[0]
            elif node.key == 'Name':
                self.plugin_name = node.values[0]
            elif node.key == 'Vhost':
                self.vhost = node.values[0]
            elif node.key == 'Username':
                self.username = node.values[0]
            elif node.key == 'Password':
                self.password = node.values[0]
            else:
                collectd.warning("%s: Unknown configuration key %s" % (PLUGIN_NAME, node.key))

    def multi_config(self, obj):
        admin_port = None
        host = None
        plugin_name = None
        vhost = None
        username = None
        password = None

        for node in obj.children:
            if node.key == 'Port':
                admin_port = int(node.values[0])
            elif node.key == 'Host':
                host = node.values[0]
            elif node.key == 'Name':
                plugin_name = node.values[0]
            elif node.key == 'Vhost':
                vhost = node.values[0]
            elif node.key == 'Username':
                username = node.values[0]
            elif node.key == 'Password':
                password = node.values[0]
            else:
                collectd.warning("%s: Unknown configuration key %s" % (PLUGIN_NAME, node.key))

        CONFIGS.append( { 'admin_port': admin_port , 'host': host, 'plugin_name' : plugin_name , 'vhost' : vhost , 'username' : username, 'password' : password} )

    def submit(self, metric, type, metric_key, value):

        self.collectd_info('------ submit {0} metrics------'.format(PLUGIN_NAME))
        self.collectd_info('{0}.{1}-{2}.{3}: {4}'.format( self.plugin_name, type, metric, metric_key, str(value)))
        plugin_instance = '%s-%s' % (self.host, self.admin_port)

        v = collectd.Values(plugin=PLUGIN_NAME)
        v.type = type
        v.type_instance = "{0}.{1}".format(metric,metric_key)
        v.plugin = self.plugin_name
        v.plugin_instance = plugin_instance
        v.values = [value,]
        v.dispatch()

    def parse_metric_object(self, metrics):

        queue_name = ''
        queue_metrics = {}
        final_queue_metrics = {}
        main_value = 0
        try:
            for main_key in metrics:

                #if METRIC.has_key(main_key) and METRIC.get(main_key):

                if METRIC.has_key(main_key) and METRIC.get(main_key):

                    if SUB_METRIC.has_key(main_key):
                        try:
                            main_value = metrics[main_key]

                            for sub_key1 in main_value:
                                sub_value1 = main_value[sub_key1]
                                if isinstance(sub_value1, int) or isinstance(sub_value1, float):
                                    graph_metric_key = '{0}-{1}'.format(main_key, sub_key1)
                                    graph_metric_value = sub_value1
                                    queue_metrics[graph_metric_key] = graph_metric_value
                        except:
                            error_msg = traceback.print_exc()
                            self.collectd_warning("{0}: Exception error encountered {1}".format(main_key), error_msg)
                    elif main_key == 'message_stats':
                        main_value = metrics[main_key]
                        for sub_key in main_value:
                            sub_value = 0
                            graph_metric_value = 0
                            if MESSAGES_STATS.has_key(sub_key):
                                if re.search('_details$',sub_key ):
                                    sub_value = main_value[sub_key]['rate']
                                    graph_metric_key = '{0}-{1}-rate'.format(main_key, sub_key)
                                    graph_metric_value = sub_value
                                    queue_metrics[graph_metric_key] = graph_metric_value
                                else:
                                    sub_value = main_value[sub_key]
                                    graph_metric_key = '{0}-{1}'.format(main_key, sub_key)
                                    graph_metric_value = sub_value
                                    queue_metrics[graph_metric_key] = graph_metric_value
                    else:
                        main_value = metrics[main_key]
                        if isinstance(main_value, int) or isinstance(main_value, float):
                            graph_metric_key = main_key
                            graph_metric_value = main_value
                            queue_metrics[graph_metric_key] = graph_metric_value

                if main_key == 'name':
                    queue_name = metrics[main_key]

            
            for k in queue_metrics:                
                final_metric_key = "{0}-{1}-{2}".format(self.vhost, queue_name, self.truncate_key(k) )
                final_metric_value = queue_metrics[k]
                final_queue_metrics[final_metric_key] = final_metric_value
        except:
            error_msg = traceback.print_exc()
            self.collectd_warning( '{0} plugin: {1}'.format(PLUGIN_NAME, error_msg) )                    
        finally:
            return final_queue_metrics

    def check_metrics_rabbitmq_rest_api_json(self):

        try:

            rest_api_url='http://{0}:{1}/api/queues/{2}/'.format(self.host, str(self.admin_port), str(self.vhost))
            self.collectd_info(rest_api_url)
            request = urllib2.Request(rest_api_url)

            base64string = base64.encodestring('%s:%s' % (self.username, self.password)).replace('\n', '')
            request.add_header("Authorization", "Basic %s" % base64string)   

            result = urllib2.urlopen(request)
            content = result.read()

            metric_objects = ()
            if self.live:
                metric_objects = json.loads(content)
            else:
                json_object_result = json.loads(sample_result)

            all_metrics = {}
            for metric in metric_objects:
                parsed_metric_results = self.parse_metric_object(metric)

                for parsed_metric_key in parsed_metric_results:
                    parsed_metric_value = parsed_metric_results[parsed_metric_key]
                    final_key = '{0}-{1}'.format(self.plugin_name, parsed_metric_key)
                    final_value = parsed_metric_value
                    all_metrics[final_key] = final_value

            if self.debug_info:
                str_json = json.dumps(all_metrics)
                print str_json
            else:
                #collect and submit all metrics
                for metric_key in all_metrics:
                    self.submit('RMQ', 'gauge', metric_key, all_metrics[metric_key] )

        except:
            error_msg = traceback.print_exc()
            self.collectd_warning( '{0} plugin: {1}'.format(PLUGIN_NAME, error_msg) )                    

    def truncate_key(self, metric_key):
        try:
            if METRIC_KEY_TRUNCATE.has_key(metric_key):
                return METRIC_KEY_TRUNCATE.get(metric_key)
            else:
                return metric_key
        except:
            pass
            return metric_key

    def check_metrics_by_config(self, config):

        self.admin_port = config['admin_port']
        self.host = config['host']
        self.plugin_name = config['plugin_name']
        self.vhost = config['vhost']
        self.username = config['username']
        self.password = config['password']

        try:

            rest_api_url='http://{0}:{1}/api/queues/{2}/'.format(self.host, str(self.admin_port), str(self.vhost))
            request = urllib2.Request(rest_api_url)

            base64string = base64.encodestring('%s:%s' % (self.username, self.password)).replace('\n', '')
            request.add_header("Authorization", "Basic %s" % base64string)   

            result = urllib2.urlopen(request)
            content = result.read()

            metric_objects = ()
            if self.live:
                metric_objects = json.loads(content)
            else:
                json_object_result = json.loads(sample_result)

            all_metrics = {}
            for metric in metric_objects:
                parsed_metric_results = self.parse_metric_object(metric)

                for parsed_metric_key in parsed_metric_results:
                    parsed_metric_value = parsed_metric_results[parsed_metric_key]
                    final_key =  parsed_metric_key 
                    final_value = parsed_metric_value
                    all_metrics[final_key] = final_value

            if self.debug_info:
                METRICS_RESULTS.append(all_metrics)
            else:
                #collect and submit all metrics
                for metric_key in all_metrics:
                    self.submit('RMQ', 'gauge', metric_key, all_metrics[metric_key] )

        except:
            error_msg = traceback.print_exc()
            self.collectd_warning( '{0} plugin: {1}'.format(PLUGIN_NAME, error_msg) ) 

    def check_run_multi_config(self):
        try:
            for config in CONFIGS:
                self.check_metrics_by_config(config)
        except:
            error_msg = traceback.print_exc()
            self.collectd_warning( error_msg )


    def write(self, vl, data=None):
        for i in vl.values:
            print "%s (%s): %f" % (vl.plugin, vl.type, i)

def main():

    global CONFIGS

    epilog = "collectd_rabbitMQ ."
    usage = """
        %prog
    """
    parser = optparse.OptionParser(usage=usage, epilog=epilog)
    parser.add_option("","--plugin-name", default="RabbitMQ")
    parser.add_option("-H", "--host", default="localhost",
        help="RabbitMQ hostname. Default localhost")
    parser.add_option("-P", "--port", default=55672,
        help="RabbitMQ Admin port. Default 55672.")
    parser.add_option("", "--username", default="guest",
        help="Username credential. Default guest.")
    parser.add_option("", "--password", default="guest",
        help="Password credential. Default guest.")
    parser.add_option("", "--vhost", default="/",
        help="Virtual host. Default /")

    opts, arg_files = parser.parse_args()

    CONFIGS = ([{'plugin_name' : opts.plugin_name, 'host' : opts.host, 'admin_port' : opts.port, 'vhost' : opts.vhost, 'username' : opts.username, 'password' : opts.password }])
    co = RabbitMQ()
    co.check_run_multi_config()
    if co.debug_info:
        str_json = json.dumps(METRICS_RESULTS)
        print str_json


if not DEBUG:
    collectd_rabbitMQ = RabbitMQ()
    collectd.register_config(collectd_rabbitMQ.multi_config)
    collectd.register_read(collectd_rabbitMQ.check_run_multi_config)
    collectd.register_write(collectd_rabbitMQ.write)

if __name__ == '__main__':
    main()
