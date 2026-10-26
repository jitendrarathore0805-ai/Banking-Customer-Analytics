from pydantic import BaseModel
class Customer_Segmentation(BaseModel):
    age:int
    experience: int
    income: int
    family: int
    ccavg : float
    mortgage: int
class LoanPrediction(BaseModel):
    age: float
    experience: float
    income: float
    family: int
    zip_code: int
    ccavg: float
    education: int
    mortgage: float
    securities_account: int
    cd_account: int
    online: int
    creditcard: int