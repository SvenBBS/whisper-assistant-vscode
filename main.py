from fastapi import FastAPI, UploadFile, File
import whisper
import tempfile
import os
import torch

app = FastAPI(title="Whisper Assistant API")

def try_use_mps():
    """Try to use MPS, return device type and fp16 status"""
    if not torch.backends.mps.is_available():
        return "cpu", False

    try:
        # Test basic tensor operations
        test_tensor = torch.zeros(1).to("mps")
        return "mps", True
    except Exception as e:
        print(f"Basic MPS test failed: {str(e)}")
        return "cpu", False

# Initialize device settings
device, fp16_enabled = try_use_mps()
print(f"Initial device setup: {device}")

# Initialize model and move components to device
model = whisper.load_model("turbo")
if device == "mps":
    try:
        print("Moving encoder to MPS...")
        model.encoder = model.encoder.to("mps")
        
        print("Moving decoder to MPS...")
        model.decoder = model.decoder.to("mps")
        
        print("Successfully moved model components to MPS")
    except Exception as e:
        print(f"Failed to move components to MPS: {str(e)}")
        device = "cpu"
        fp16_enabled = False
        model = model.to("cpu")

# Store MPS availability info for health check
mps_status = {
    "is_available": torch.backends.mps.is_available(),
    "is_built": torch.backends.mps.is_built()
}

@app.post("/v1/audio/transcriptions")
async def transcribe_audio(
    file: UploadFile = File(...),
    model_name: str = "whisper-1",  # Renamed parameter to avoid conflict
    language: str = "en"
):
    """Transcribe audio file to text"""
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
        content = await file.read()
        temp_file.write(content)
        temp_file.flush()
        
        try:
            # Model is already on the correct device, just transcribe
            result = model.transcribe(
                temp_file.name,
                language="de",
                fp16=fp16_enabled
            )
        except Exception as e:
            print(f"Transcription error: {str(e)}")
            raise
        
        # Format response to match OpenAI API
        formatted_segments = []
        for i, segment in enumerate(result["segments"]):
            formatted_segments.append({
                "id": i,
                "seek": segment["seek"],
                "start": segment["start"],
                "end": segment["end"],
                "text": segment["text"],
                "tokens": [],
                "temperature": 0.0,
            })
        
        # Clean up temp file
        os.unlink(temp_file.name)
        
        # Console output for transcription results
        print("\n=== Transkriptionsergebnisse ===")
        print(f"\nErkannter Text:\n{result['text']}")
        print(f"\nErkannte Sprache: {result['language']}")
        print("\nSegmente:")
        for segment in formatted_segments:
            print(f"\nSegment {segment['id']}:")
            print(f"  Start: {segment['start']:.2f}s")
            print(f"  Ende: {segment['end']:.2f}s")
            print(f"  Text: {segment['text']}")
        
        return {
            "text": result["text"],
            "segments": formatted_segments,
            "language": result["language"]
        }

@app.get("/v1/health")
async def health_check():
    """Check if the API is running"""
    return {
        "status": "ok",
        "device": device,
        "mps_support": {
            "is_available": mps_status["is_available"],
            "is_built": mps_status["is_built"]
        },
        "fp16": fp16_enabled,
        "torch_version": torch.__version__
    }

@app.get("/")
async def root():
    """Get API information and available endpoints"""
    return {
        "message": "Whisper Assistant API",
        "docs": "/docs",
        "health_check": "/v1/health",
        "transcribe": "/v1/audio/transcriptions"
    }
