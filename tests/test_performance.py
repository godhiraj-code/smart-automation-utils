import unittest
from smart_automation.performance import monitor
import time

class TestPerformanceMonitor(unittest.TestCase):
    def test_timer(self):
        monitor.start_timer("test_op")
        time.sleep(0.1)
        duration = monitor.stop_timer("test_op")
        self.assertGreaterEqual(duration, 0.1)

    def test_memory_logging(self):
        mem = monitor.log_memory_usage()
        self.assertGreater(mem, 0)

if __name__ == "__main__":
    unittest.main()
