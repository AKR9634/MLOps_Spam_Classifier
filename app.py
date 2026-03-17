from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse, RedirectResponse
from uvicorn import run as app_run
from typing import Optional

APP_HOST = "0.0.0.0"
APP_PORT = 5000

from src.pipeline.prediction_pipeline import SpamData, SpamDataClassifier
from src.pipeline.training_pipeline import TrainingPipeline


app = FastAPI()

# Mount the "static" directory for serving static files (like CSS)
app.mount("/static", StaticFiles(directory="static"), name = "static")

# Set up Jinja2 template engine for rendering HTML templates
templates = Jinja2Templates(directory="templates")

# Allow all origins for Cross-Origin Resource Sharing(CORS)
origins = ["*"]

# Configure middleware to handle CORS, allowing requests from any origin
app.add_middleware(CORSMiddleware, allow_origins = origins, allow_credentials = True, allow_methods = ["*"], allow_headers = ["*"])

class DataForm:

    """ 
    DataForm class to handle and process incoming form data.
    This class defines the spam related attributes expected from the form...
    """

    def __init__(self, request: Request):
        self.request: Request = request
        self.message: Optional[str] = None

    async def get_spam_data(self):
    
        """
        Method to retrieve and assign form data to class attributes.
        This method is asynchornous to handle form data fetching without blocking...
        """

        form = await self.request.form()
        self.message = form.get("Message")

# Route to render the main page with the form
@app.get("/", tags=["authentication"])
async def index(request : Request):    
    """
    Render the main HTML form page for vehicle data input.
    """

    return templates.TemplateResponse("spam_data.html", {"request":request, "context":"Rendering"})

# Route to trigger the model training process
@app.get("/train")
async def trainRouteClient():
    """
    Endpoint to initiate the model training pipeline.
    """

    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Training Successful!!!")
    except Exception as e:
        return Response(f"Error Occured!!! {e}")
    

# Route to handle form submission and make predictions
@app.post("/")
async def predictRouteClient(request : Request):
    """
    Endpoint to receive form data, process it, and make a prediction.
    """

    try:
        form = DataForm(request)
        await form.get_spam_data()

        spam_data = SpamData(message= form.message)

        # Convert form data into a DataFrame for the model
        spam_df = spam_data.get_spam_input_data_frame()

        # Initialize the prediction pipeline
        model_predictor = SpamDataClassifier()

        # Make a prediction and retrieve the result
        value = model_predictor.predict(dataframe=spam_df)[0]

        # Interpret the prediction result as "Response-Yes" or "Response-No"
        status = "Response-Yes" if value == 1 else "Response-No"

        # Render the same HTML page with the prediction result
        return templates.TemplateResponse("spam_data.html", {"request":request, "context":status})
    
    except Exception as e:
        return {"status":False, "error":f"{e}"}
    
# Main entry point to start the FastAPI server
if __name__ == "__main__":
    app_run(app, host = APP_HOST, port = APP_PORT)