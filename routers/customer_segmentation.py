from fastapi import APIRouter,Request
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from model.base_model import Customer_Segmentation
import numpy as np
import pickle
router=APIRouter()
@router.post("/get_customer_segmentation")
async def get_segmentation(data: Customer_Segmentation):
    with open('kmeans_model.pkl', 'rb') as f:
        kmeans_model = pickle.load(f)
    with open('scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    with open('pca.pkl', 'rb') as f:
        pca = pickle.load(f)
    new_customer = np.array([[data.age, data.experience, data.income, data.family, data.ccavg]])
    # Apply transformations
    new_customer_scaled = scaler.transform(new_customer)
    # convert features into principal components
    new_customer_pca = pca.transform(new_customer_scaled)
    # Predict cluster
    # cluster_id = kmeans_model.predict(new_customer_pca)
    cluster_id = int(kmeans_model.predict(new_customer_pca)[0])
    cluster_info = {
        0: {
            "segment": "High-Value",
            "characteristics": "High income, multiple products, older age, high campaign response",
            "marketing_strategy": "Offer premium investment plans",
            "potential_roi_growth": "15–20% revenue growth from high-margin products"
        },
        1: {
            "segment": "At-Risk",
            "characteristics": "Low balance, declining engagement, younger customers",
            "marketing_strategy": "Personalized reactivation campaigns",
            "potential_roi_growth": "Retention improved by 10% per quarter"
        },
        2: {
            "segment": "Dormant",
            "characteristics": "Moderate balance but no recent transactions",
            "marketing_strategy": "Cashback or reward-based revival offers",
            "potential_roi_growth": "Campaign efficiency up by 12%"
        }
    }
    # Get details for the assigned cluster
    segment_data = cluster_info.get(cluster_id,
                                    {"segment": "Unknown", "characteristics": "N/A", "marketing_strategy": "N/A",
                                     "potential_roi_growth": "N/A"})
    # Return enriched response
    return {
        "cluster_id": cluster_id,
        "segment": segment_data["segment"],
        "characteristics": segment_data["characteristics"],
        "marketing_strategy": segment_data["marketing_strategy"],
        "potential_roi_growth": segment_data["potential_roi_growth"],
        "message": f"Customer belongs to the '{segment_data['segment']}' segment"
    }


