from fastapi import FastAPI, UploadFile, HTTPException, File, Request
from fastapi.responses import FileResponse
import pandas as pd

from classifier_processors.classify import classify

app = FastAPI()

@app.get("/")
def home():
    # Basic health-check endpoint for quick API verification.
    return {"message": "Log Classification API is running"}

@app.get("/classify")
def classify_log():
    # Sample endpoint for GET request.
    return {
        "message": "Use POST /classify with a CSV file upload.",
        "form_field_name": "file",
        "required_columns": ["source", "log_message"],
    }

@app.post("/classify")
async def classify_logs(request: Request, file: UploadFile | None = File(default=None)):
    
    # Reject requests where the multipart upload does not include a file.
    if file is None:
        raise HTTPException(status_code=400, detail="No file uploaded.")

    # Only CSV uploads are supported by this endpoint.
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a CSV file.")

    try:
        # Read the uploaded CSV file into a DataFrame
        df = pd.read_csv(file.file)

        # Ensure the uploaded data matches the classifier's expected schema.
        if 'source' not in df.columns or 'log_message' not in df.columns:
            raise HTTPException(status_code=400, detail="CSV file must contain 'source' and 'log_message' columns.")

        # Convert rows into classifier input tuples and attach predicted labels.
        csv_logs = list(zip(df['source'], df['log_message']))
        df["target_label"] = [label for _, _, label in classify(csv_logs)]

        # Save the classified output so it can be returned as a downloadable file.
        output_file = "./resources/test_split_classified_output.csv"
        df.to_csv(output_file, index=False)
        print("Classified logs saved to test_split_classified_output.csv")
        return FileResponse(output_file, media_type='text/csv', filename="classified_logs.csv")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        file.file.close()
