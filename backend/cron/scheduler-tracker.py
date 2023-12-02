# import schedule
# from .tasks import pricetracker_tasks

# class ScheduleTrackerCron:

#     def __init__(self):
#         self.tasks = pricetracker_tasks

#     def run_scheduler(self):
#         schedule.every(2).days.at("12:00").do(self.tasks.track_prices)

#         while True:
#             schedule.run_pending()

# if __name__ == "__main__":
#     price_tracker_cron = ScheduleTrackerCron()

#     price_tracker_cron.run_scheduler()