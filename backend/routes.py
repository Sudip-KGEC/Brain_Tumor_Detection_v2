from fastapi import APIRouter, UploadFile, File, HTTPException
from predict import process_image_pipeline

router = APIRouter()

@router.get("/")
def api_root():
    return {"message": "Brain Tumor Detection API"}

@router.get("/test")
def test():
    return {"success": True, "message": "Routes are working."}

@router.post("/predict")
async def predict(file: UploadFile = File(...)):
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are allowed.")

    try:
        # Read file into memory asynchronously
        image_bytes = await file.read()
        
        # Pass bytes directly to the pipeline
        result = process_image_pipeline(image_bytes)
        return result

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")