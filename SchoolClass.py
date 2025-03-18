from Reports import BullyingReport

class School:
    def __init__(self, schoolID: str, name: str, address: str):
        self.schoolID = schoolID
        self.name = name
        self.address = address
        self.users = []        # List of User objects
        self.reports = []      # List of BullyingReport objects

    def registerReport(self, report: BullyingReport) -> None:
        self.reports.append(report)
        print(f"[REGISTER] Report {report.reportID} registered in {self.name}.")