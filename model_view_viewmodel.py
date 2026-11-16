from collections.abc import Callable


# MODEL
class Job:
    def __init__(self, job_id: str, status: str):
        self.id = job_id
        self.status = status

    def complete(self):
        if self.status != "running":
            raise ValueError("Only running jobs can be completed")
        self.status = "completed"


# VIEWMODEL
class JobDashboardViewModel:
    def __init__(self, job: Job):
        # hide outside access to job
        self._job = job
        # notification to UI elements
        self._listeners: list[Callable[[], None]] = []

    @property
    # access the model information
    def job_id(self):
        return self._job.id

    @property
    # access the model information
    def status_label(self):
        return self._job.status.upper()

    @property
    # access the model information
    def can_complete(self):
        return self._job.status == "running"

    def subscribe(self, listener: Callable[[], None]):
        self._listeners.append(listener)

    def _notify(self):
        for listener in self._listeners:
            listener()

    # access and update the model
    def complete_job(self):
        if not self.can_complete:
            return

        self._job.complete()
        # notify to all subscribers
        self._notify()


# VIEW
class JobDashboardView:
    def __init__(self, view_model: JobDashboardViewModel):
        # have access to the view_model only, NOT model
        # subscribe to the view_model to notify for UI update, calling render()
        self.vm = view_model
        self.vm.subscribe(self.render)

    def render(self):
        button_state = "enabled" if self.vm.can_complete else "disabled"

        print(f"Job: {self.vm.job_id}")
        print(f"Status: {self.vm.status_label}")
        print(f"Complete button: {button_state}")
        print("---")

    def click_complete(self):
        self.vm.complete_job()


def main():
    job = Job("job-1", "running")

    vm = JobDashboardViewModel(job)
    view = JobDashboardView(vm)

    view.render()
    view.click_complete()


if __name__ == "__main__":
    main()
