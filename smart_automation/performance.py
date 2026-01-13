import time
import psutil
import os
from .logger import logger

class PerformanceMonitor:
    def __init__(self):
        self.start_times = {}
        self.metrics = []

    def start_timer(self, label):
        self.start_times[label] = time.time()
        logger.debug(f"Performance: Started timer for '{label}'")

    def stop_timer(self, label):
        if label in self.start_times:
            duration = time.time() - self.start_times[label]
            self.metrics.append({
                "type": "timer",
                "label": label,
                "value": duration,
                "timestamp": time.time()
            })
            logger.info(f"Performance: '{label}' took {duration:.4f}s")
            del self.start_times[label]
            return duration
        return None

    def log_memory_usage(self):
        process = psutil.Process(os.getpid())
        mem_info = process.memory_info().rss / (1024 * 1024)  # MB
        self.metrics.append({
            "type": "memory",
            "label": "rss",
            "value": mem_info,
            "timestamp": time.time()
        })
        logger.info(f"Performance: Current memory usage: {mem_info:.2f} MB")
        return mem_info

    def get_summary(self):
        return self.metrics

# Global monitor instance
monitor = PerformanceMonitor()
