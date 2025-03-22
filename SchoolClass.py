class School:
    _instance = None  

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(School, cls).__new__(cls)
            cls._instance.reports = []
            cls._instance.users = []
        return cls._instance
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls()
        return cls._instance if cls._instance else cls()
        
    def __init__(self, schoolID: str, name: str, address: str):
        self.schoolID = schoolID
        self.name = name
        self.address = address
        self.users = []        # List of User objects
        self.reports = []      # List of BullyingReport objects

    def registerReport(self, report) -> None:
        self.reports.append(report)
        print(f"[REGISTER] Report {report.reportID} registered in {self.name}.")
