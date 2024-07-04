class DataFetcher:
  def __init__(self)

  def getData(self)-> None:
    self.openConnection()
    self.extractData()
    self.parseData()
    self.formatData()
    self.closeConnection()
    self.updateDB()


  def parseData(self) -> None:

  def formatData(self) -> None:

  def updateDB(self) -> None:

  @abstractmethod
  def openConnection(self) -> None:
    pass
    
  @abstractmethod 
  def extractData(self) -> None:
    pass
    
  @abstractmethod 
  def closeConnection(self) -> None:
    pass
