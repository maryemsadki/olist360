
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.sales import router as sales_router
from routes.customers import router as customers_router
from routes.products import router as products_router
from routes.delivery import router as delivery_router
from routes.ml import router as ml_router
from routes.api import router as api_router
from routes import analytics 


app = FastAPI(
    title="Olist360 API",
    description=(
        "API pour analyser les ventes, les clients, les produits, "
        "les livraisons et les résultats du Machine Learning."
    ),
    version="1.0.0"
)


# Configuration CORS pour autoriser le frontend React
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enregistrement des routes
app.include_router(sales_router)
app.include_router(customers_router)
app.include_router(products_router)
app.include_router(delivery_router)
app.include_router(ml_router)
app.include_router(api_router)
app.include_router(analytics.router)

@app.get("/")
def home():
    return {
        "message": "Bienvenue dans Olist360",
        "status": "API opérationnelle"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}
