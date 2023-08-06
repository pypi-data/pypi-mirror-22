import unittest

from mock import patch

from tcell_agent.appsensor.meta import AppSensorMeta
from tcell_agent.appsensor.sensors import ResponseSizeSensor


class ResponseSizeSensorTest(unittest.TestCase):
    def create_default_sensor_test(self):
        sensor = ResponseSizeSensor()
        self.assertEqual(sensor.enabled, False)
        self.assertEqual(sensor.limit, 2097152)
        self.assertEqual(sensor.excluded_route_ids, {})

    def create_enabled_sensor_test(self):
        sensor = ResponseSizeSensor({"enabled": True})
        self.assertEqual(sensor.enabled, True)
        self.assertEqual(sensor.limit, 2097152)
        self.assertEqual(sensor.excluded_route_ids, {})

    def create_sensor_with_limit_test(self):
        sensor = ResponseSizeSensor({"limit": 1024})
        self.assertEqual(sensor.enabled, False)
        self.assertEqual(sensor.limit, 1024)
        self.assertEqual(sensor.excluded_route_ids, {})

    def create_sensor_with_exclude_routes_test(self):
        sensor = ResponseSizeSensor({"exclude_routes": ["1", "10", "20"]})
        self.assertEqual(sensor.enabled, False)
        self.assertEqual(sensor.limit, 2097152)
        self.assertEqual(sensor.excluded_route_ids, {"1": True, "10": True, "20": True})

    def with_disabled_sensor_check_test(self):
        sensor = ResponseSizeSensor({"enabled": False})
        appsensor_meta = AppSensorMeta()
        appsensor_meta.request_content_bytes_len = 1024
        sensor.check(appsensor_meta)

    def with_enabled_sensor_and_size_is_too_big_but_route_id_is_excluded_check_test(self):
        sensor = ResponseSizeSensor({"enabled": True, "limit": 1, "exclude_routes": ["23947"]})
        appsensor_meta = AppSensorMeta()
        appsensor_meta.remote_address = "remote_addr"
        appsensor_meta.method = "request_method"
        appsensor_meta.location = "abosolute_uri"
        appsensor_meta.route_id = "23947"
        appsensor_meta.session_id = "session_id"
        appsensor_meta.user_id = "user_id"
        appsensor_meta.response_content_bytes_len = 2048

        with patch('tcell_agent.appsensor.sensors.size_sensor.send_event') as patched_send_event:
            sensor.check(appsensor_meta)
            self.assertFalse(patched_send_event.called)

    def with_enabled_sensor_and_size_is_ok_check_test(self):
        sensor = ResponseSizeSensor({"enabled": True, "limit": 1024})
        appsensor_meta = AppSensorMeta()
        appsensor_meta.remote_address = "remote_addr"
        appsensor_meta.method = "request_method"
        appsensor_meta.location = "abosolute_uri"
        appsensor_meta.route_id = "route_id"
        appsensor_meta.session_id = "session_id"
        appsensor_meta.user_id = "user_id"
        appsensor_meta.response_content_bytes_len = 10

        with patch('tcell_agent.appsensor.sensors.size_sensor.send_event') as patched_send_event:
            sensor.check(appsensor_meta)
            self.assertFalse(patched_send_event.called)

    def with_enabled_sensor_and_size_is_too_big_by_half_a_KiB_check_test(self):
        appsensor_meta = AppSensorMeta()
        appsensor_meta.remote_address = "remote_addr"
        appsensor_meta.method = "request_method"
        appsensor_meta.location = "abosolute_uri"
        appsensor_meta.route_id = "route_id"
        appsensor_meta.session_id = "session_id"
        appsensor_meta.user_id = "user_id"
        appsensor_meta.response_content_bytes_len = 1024 + 512

        sensor = ResponseSizeSensor({"enabled": True, "limit": 1})

        with patch('tcell_agent.appsensor.sensors.size_sensor.send_event') as patched_send_event:
            sensor.check(appsensor_meta)
            patched_send_event.assert_called_once_with(
                appsensor_meta=appsensor_meta,
                detection_point=ResponseSizeSensor.DP_UNUSUAL_RESPONSE_SIZE,
                parameter=None,
                meta={"sz": 1536},
                collect_full_uri=False)

    def with_enabled_sensor_and_size_is_too_big_by_one_check_test(self):
        appsensor_meta = AppSensorMeta()
        appsensor_meta.remote_address = "remote_addr"
        appsensor_meta.method = "request_method"
        appsensor_meta.location = "abosolute_uri"
        appsensor_meta.route_id = "route_id"
        appsensor_meta.session_id = "session_id"
        appsensor_meta.user_id = "user_id"
        appsensor_meta.response_content_bytes_len = 2048

        sensor = ResponseSizeSensor({"enabled": True, "limit": 1})

        with patch('tcell_agent.appsensor.sensors.size_sensor.send_event') as patched_send_event:
            sensor.check(appsensor_meta)
            patched_send_event.assert_called_once_with(
                appsensor_meta=appsensor_meta,
                detection_point=ResponseSizeSensor.DP_UNUSUAL_RESPONSE_SIZE,
                parameter=None,
                meta={"sz": 2048},
                collect_full_uri=False)

    def with_enabled_sensor_and_size_is_one_less_than_limit_check_test(self):
        appsensor_meta = AppSensorMeta()
        appsensor_meta.remote_address = "remote_addr"
        appsensor_meta.method = "request_method"
        appsensor_meta.location = "abosolute_uri"
        appsensor_meta.route_id = "route_id"
        appsensor_meta.session_id = "session_id"
        appsensor_meta.user_id = "user_id"
        appsensor_meta.response_content_bytes_len = 0

        sensor = ResponseSizeSensor({"enabled": True, "limit": 1})

        with patch('tcell_agent.appsensor.sensors.size_sensor.send_event') as patched_send_event:
            sensor.check(appsensor_meta)
            self.assertFalse(patched_send_event.called)

    def with_enabled_sensor_and_size_is_equal_to_limit_check_test(self):
        appsensor_meta = AppSensorMeta()
        appsensor_meta.remote_address = "remote_addr"
        appsensor_meta.method = "request_method"
        appsensor_meta.location = "abosolute_uri"
        appsensor_meta.route_id = "route_id"
        appsensor_meta.session_id = "session_id"
        appsensor_meta.user_id = "user_id"
        appsensor_meta.response_content_bytes_len = 1024

        sensor = ResponseSizeSensor({"enabled": True, "limit": 1})

        with patch('tcell_agent.appsensor.sensors.size_sensor.send_event') as patched_send_event:
            sensor.check(appsensor_meta)
            self.assertFalse(patched_send_event.called)
