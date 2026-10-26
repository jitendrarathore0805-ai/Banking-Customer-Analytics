from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.customer_segmentation import router as customer_segmentation
from routers.loan_classification import router as predict_personal_loan
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(customer_segmentation)
app.include_router(predict_personal_loan)


