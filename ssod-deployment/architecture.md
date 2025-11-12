```mermaid
graph TD
    A[User] --> B[Streamlit UI]
    B --> C[YOLOv8 Model]
    C --> D[Falcon API]
    D --> E[New Model Weights]
    E --> F[Auto-Update Logic]
    F --> C
```
